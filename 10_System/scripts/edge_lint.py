#!/usr/bin/env python3
"""
edge_lint.py — the link/edge half of the ProdOS knowledge compiler.

Implements the compiler contract from
  30_Library/SoT/SoT - Typed Edge Vocabulary (Knowledge Graph Relations).md  (§6)

It extracts every typed edge  %%[<rel>:: [[<target>]][, attrs]]%%  from the vault,
checks each against the controlled vocabulary and attribute rules, resolves every
target, and prints a report.

The edge interior is a Dataview inline field, so the same on-disk encoding serves
two readers: Dataview answers single-hop questions interactively inside Obsidian
("LIST WHERE contradicts"), and this compiler answers what DQL structurally
cannot — vocabulary validation, gap/foundation audit, cycle detection, and
multi-hop provenance.

Note targets are wikilinks, so Obsidian's own rename refactoring keeps them
correct. Bare (non-wikilink) targets are reserved for content-block ids, which
are not notes and so cannot be linked.

It is REPORT-ONLY. It never edits a note (mirrors the dry-run/UNSURE discipline in
Protocol - Typed Answer Contract (TAC) for Vault Agents). Exit code is non-zero if
any ERROR is found (0 warnings still exit 0), so it can gate CI or a pre-commit hook.

Usage:
    python3 edge_lint.py                # lint the whole vault (auto-detected root)
    python3 edge_lint.py --path .       # lint a specific folder
    python3 edge_lint.py --quiet        # only print files that have findings + summary
    python3 edge_lint.py --audit        # + C1 gaps, C2 foundations, C3 conflicts
    python3 edge_lint.py --why TITLE    # C4: what a claim rests on
    python3 edge_lint.py --impact TITLE # C4: what rests on a claim

Dependencies: PyYAML — REQUIRED. Frontmatter carries `title` (edge resolution)
and `type` (claim detection for C1), so without it the tool reports false
danglers and a false-empty gap audit. It refuses to run rather than mislead.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Spec constants — keep in lockstep with the SoT §2 / §3. Editing this list IS
# the sanctioned route to add a relationship type (per the SoT).
# ---------------------------------------------------------------------------
VOCABULARY = {
    "extends",
    "synthesizes",
    "implements",
    "contradicts",
    "supports",
    "depends_on",
    "revises",
}
CONFIDENCE_VALUES = {"high", "medium", "low"}
STRENGTH_MIN, STRENGTH_MAX = 1, 5

# Directories never scanned (sealed / non-TAC / machinery). See Frontmatter
# Contract §8 for the governance rationale.
EXCLUDE_DIRS = {
    ".git", ".obsidian", ".trash", ".claude", ".shale", ".antigravitycli",
    "raw", "output", "outputs", "assets", "Excalidraw", "node_modules",
}

# ---------------------------------------------------------------------------
# Regexes
# ---------------------------------------------------------------------------
# %%[relationship:: [[Target]]]%%   or   %%[relationship:: [[Target]], k=v, k=v]%%
# The interior is a Dataview inline field, so Dataview indexes the same edge
# the compiler reads (SoT - Typed Edge Vocabulary §1). Non-greedy up to `]%%`
# terminates correctly on the `]]` of a wikilink.
EDGE_RE = re.compile(r"%%\[\s*([A-Za-z][\w-]*)\s*::\s*(.*?)\s*\]%%")
# A wikilink target: [[Note]], [[Note|Alias]], [[Note#Heading]], [[Note#^block]]
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
# <!--content-block-start type="concept" id="user-namespace"-->
BLOCK_ID_RE = re.compile(r"<!--\s*content-block-start[^>]*\bid=\"([^\"]+)\"")
# Inline code span, for masking documentation examples.
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def mask_code(text: str) -> str:
    """Blank out fenced code blocks and inline code spans so documentation
    examples of the edge syntax are not linted as real edges. Preserves the
    exact line count so reported line numbers stay accurate."""
    out = []
    in_fence = False
    fence_marker = None
    for line in text.split("\n"):
        stripped = line.lstrip()
        if not in_fence and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_fence, fence_marker = True, stripped[:3]
            out.append("")
            continue
        if in_fence:
            if stripped.startswith(fence_marker):
                in_fence, fence_marker = False, None
            out.append("")
            continue
        out.append(INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line))
    return "\n".join(out)


@dataclass
class Finding:
    level: str          # "ERROR" or "WARN"
    line: int
    message: str


@dataclass
class Index:
    """Everything a target id can resolve to, built over the whole scan."""
    block_ids: dict[str, list[str]] = field(default_factory=dict)   # id -> [files]
    note_ids: dict[str, list[str]] = field(default_factory=dict)    # prodos.id -> [files]
    titles: dict[str, list[str]] = field(default_factory=dict)      # title/filename -> [files]
    aliases: dict[str, list[str]] = field(default_factory=dict)     # alias -> [files]

    def _all_maps(self):
        return (self.block_ids, self.note_ids, self.titles, self.aliases)

    def resolve(self, target: str, is_link: bool = False):
        """Return (matches, kind) following SoT §4 priority order.

        A wikilink target ([[…]]) names a note, so note maps are consulted
        first; a bare target names a content-block id, so blocks come first."""
        note_maps = (
            (self.note_ids, "prodos.id"),
            (self.titles, "title"),
            (self.aliases, "alias"),
        )
        block_map = ((self.block_ids, "block"),)
        order = note_maps + block_map if is_link else block_map + note_maps
        for mp, kind in order:
            if target in mp:
                return mp[target], kind
        return [], None

    def near_miss(self, target: str):
        """Case-insensitive hint when an exact match fails."""
        low = target.lower()
        for mp in self._all_maps():
            for key in mp:
                if key.lower() == low:
                    return key
        return None


def require_yaml():
    """PyYAML is mandatory, not optional.

    Without it no frontmatter is read, so `title:` never registers (every
    title-targeted edge false-flags as dangling) and `type:` is always empty
    (so is_claim() never matches and the C1 gap audit silently reports zero
    gaps). A report-only tool that prints confident wrong answers is worse
    than one that refuses to run, so this is a hard failure."""
    try:
        import yaml  # noqa
        return yaml
    except ImportError:
        sys.exit(
            "edge_lint: PyYAML is required but not installed.\n"
            "  Without it, frontmatter titles and types are invisible: edges "
            "resolve\n  incorrectly and the argument audit reports false "
            "results.\n\n"
            "  Install it:      python3 -m pip install pyyaml\n"
            "  Or run via uv:   uv run --with pyyaml python3 "
            "10_System/scripts/edge_lint.py\n"
        )


def split_frontmatter(text: str):
    """Return (frontmatter_str, body_offset_lines). Body starts after 2nd '---'."""
    if not text.startswith("---"):
        return "", 0
    end = text.find("\n---", 3)
    if end == -1:
        return "", 0
    fm = text[3:end]
    body_start_line = text[: end + 4].count("\n") + 1
    return fm, body_start_line


def register(mp: dict, key, filepath):
    if key is None:
        return
    key = str(key).strip()
    if not key:
        return
    mp.setdefault(key, [])
    if filepath not in mp[key]:
        mp[key].append(filepath)


def build_index(files, yaml_mod) -> Index:
    idx = Index()
    for fp in files:
        try:
            text = open(fp, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue

        # Block ids (body, code-masked so example blocks don't register).
        for m in BLOCK_ID_RE.finditer(mask_code(text)):
            register(idx.block_ids, m.group(1), fp)

        # Note identifiers (frontmatter).
        register(idx.titles, os.path.splitext(os.path.basename(fp))[0], fp)
        fm, _ = split_frontmatter(text)
        if fm and yaml_mod:
            try:
                data = yaml_mod.safe_load(fm) or {}
            except Exception:
                data = {}
            if isinstance(data, dict):
                register(idx.titles, data.get("title"), fp)
                prodos = data.get("prodos")
                if isinstance(prodos, dict):
                    register(idx.note_ids, prodos.get("id"), fp)
                register(idx.note_ids, data.get("id"), fp)  # legacy top-level id
                al = data.get("aliases")
                if isinstance(al, list):
                    for a in al:
                        register(idx.aliases, a, fp)
                elif isinstance(al, str):
                    register(idx.aliases, al, fp)
    return idx


@dataclass
class Edge:
    """One parsed %%[rel:: target, attrs]%% marker."""
    rel: str
    target: str          # normalised: wikilink stripped to its note name
    is_link: bool        # True if written as [[…]] (a note), False if a bare id
    attrs_raw: str
    line: int


def parse_edge(rel: str, payload: str, line: int) -> Edge:
    """Split `[[Some, Note]], strength=4` into target + attribute remainder.

    A wikilink is consumed whole before commas are treated as separators, so
    note titles containing commas survive (several exist in this vault)."""
    payload = payload.strip()
    m = WIKILINK_RE.match(payload)
    if m:
        inner, rest = m.group(1), payload[m.end():]
        # [[Note|Alias]] -> Note ; [[Note#Heading]] / [[Note#^id]] -> Note
        target = inner.split("|", 1)[0]
        if "#" in target:
            head = target.split("#", 1)[0].strip()
            target = head or target
        is_link = True
    else:
        target, _, rest = payload.partition(",")
        is_link = False
    return Edge(rel, target.strip(), is_link, rest.lstrip(" ,").strip(), line)


def iter_edges(masked: str):
    """Yield every Edge in already-code-masked text, with 1-based line numbers."""
    for m in EDGE_RE.finditer(masked):
        yield m, parse_edge(m.group(1), m.group(2),
                            masked[: m.start()].count("\n") + 1)


def parse_attrs(raw: str):
    """'strength=4,confidence=high' -> ({'strength':'4',...}, [malformed parts])."""
    attrs, bad = {}, []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            bad.append(part)
            continue
        k, v = part.split("=", 1)
        attrs[k.strip()] = v.strip()
    return attrs, bad


def lint_file(fp: str, idx: Index) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    try:
        text = open(fp, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        return findings, 0

    text = mask_code(text)
    edge_count = 0
    for _m, e in iter_edges(text):
        edge_count += 1
        line, rel, target, attr_raw = e.line, e.rel, e.target, e.attrs_raw

        # (§6.2) vocabulary
        if rel not in VOCABULARY:
            findings.append(Finding(
                "ERROR", line,
                f"unknown relationship '{rel}' (not in vocabulary) "
                f"in %%[{rel}:: {target}]%%"))

        # (§6.4) attributes
        if attr_raw:
            attrs, bad = parse_attrs(attr_raw)
            for b in bad:
                findings.append(Finding("ERROR", line,
                    f"malformed attribute '{b}' (expected key=value) on target '{target}'"))
            if "strength" in attrs:
                s = attrs["strength"]
                if not (s.isdigit() and STRENGTH_MIN <= int(s) <= STRENGTH_MAX):
                    findings.append(Finding("ERROR", line,
                        f"strength '{s}' out of range {STRENGTH_MIN}-{STRENGTH_MAX} on target '{target}'"))
            if "confidence" in attrs and attrs["confidence"] not in CONFIDENCE_VALUES:
                findings.append(Finding("ERROR", line,
                    f"confidence '{attrs['confidence']}' not in {sorted(CONFIDENCE_VALUES)} on target '{target}'"))
            for k in attrs:
                if k not in ("strength", "confidence"):
                    findings.append(Finding("WARN", line,
                        f"unknown attribute '{k}' (only strength, confidence defined) on target '{target}'"))

        # (§6.3) target resolution
        matches, kind = idx.resolve(target, e.is_link)
        # de-dup by file for the count
        distinct = list(dict.fromkeys(matches))
        if len(distinct) == 0:
            hint = idx.near_miss(target)
            extra = f" — did you mean '{hint}'? (case mismatch)" if hint else ""
            findings.append(Finding("ERROR", line,
                f"dangling edge: target '{target}' resolves to nothing{extra}"))
        elif not e.is_link and kind != "block":
            # Resolved, but written bare. Only content-block ids may be bare;
            # a note target must be a wikilink so renames stay safe (§4).
            findings.append(Finding("WARN", line,
                f"note target '{target}' is written bare — use [[{target}]] "
                f"so Obsidian rewrites it on rename"))
        elif len(distinct) > 1:
            findings.append(Finding("WARN", line,
                f"ambiguous edge: target '{target}' ({kind}) matches "
                f"{len(distinct)} locations: {', '.join(os.path.basename(x) for x in distinct)}"))

    return findings, edge_count


# ---------------------------------------------------------------------------
# v1 ARGUMENT AUDIT  (SoT - Knowledge Compiler, capabilities C1 + C2)
# ---------------------------------------------------------------------------
# Justification edges carry the argument; contradicts is the conflict edge
# (SoT - Knowledge Compiler §4). GRAPH_RELS = everything the audit ingests.
JUSTIFICATION = {"supports", "depends_on"}
CONFLICT = {"contradicts"}
GRAPH_RELS = JUSTIFICATION | CONFLICT

BLOCK_START_FULL_RE = re.compile(r"<!--\s*content-block-start([^>]*?)-->")
BLOCK_END_RE = re.compile(r"<!--\s*content-block-end\s*-->")
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


@dataclass
class Node:
    type: str            # frontmatter/block type (e.g. "claim")
    axiom: bool
    label: str
    file: str


def _truthy(v) -> bool:
    return str(v).strip().lower() == "true" if v is not None else False


def note_meta(text: str, yaml_mod, filepath: str):
    """(type, axiom, title) for a note from its frontmatter."""
    ntype, axiom, title = "", False, os.path.splitext(os.path.basename(filepath))[0]
    fm, _ = split_frontmatter(text)
    if fm and yaml_mod:
        try:
            data = yaml_mod.safe_load(fm) or {}
        except Exception:
            data = {}
        if isinstance(data, dict):
            ntype = str(data.get("type", "") or "")
            axiom = _truthy(data.get("axiom"))
            title = data.get("title") or title
    return ntype, axiom, str(title)


def parse_blocks(masked: str):
    """Return content-block regions: [{id,type,axiom,start,end}] (non-nested)."""
    starts = [(m.start(), m.end(), dict(ATTR_RE.findall(m.group(1))))
              for m in BLOCK_START_FULL_RE.finditer(masked)]
    ends = sorted(m.start() for m in BLOCK_END_RE.finditer(masked))
    blocks = []
    for s_start, s_end, attrs in starts:
        bid = attrs.get("id")
        if not bid:
            continue
        region_end = next((e for e in ends if e > s_end), len(masked))
        blocks.append({
            "id": bid,
            "type": attrs.get("type", ""),
            "axiom": _truthy(attrs.get("axiom")),
            "start": s_start,
            "end": region_end,
        })
    return blocks


def resolve_to_node(target: str, idx: Index, is_link: bool = False):
    """Map an edge target to a unique node key, or None if unresolved/ambiguous."""
    matches, kind = idx.resolve(target, is_link)
    distinct = list(dict.fromkeys(matches))
    if len(distinct) != 1:
        return None
    if kind == "block":
        return ("block", target)
    return ("note", distinct[0])


def build_graph(files, idx: Index, yaml_mod):
    """Build the argument graph. Returns (nodes, edges) where an edge is
    (src_key, rel, tgt_key) for supports/depends_on/contradicts. src/tgt keys
    are ('note', filepath) or ('block', id)."""
    nodes: dict = {}
    edges = []
    for fp in files:
        try:
            raw = open(fp, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        masked = mask_code(raw)

        ntype, naxiom, ntitle = note_meta(raw, yaml_mod, fp)
        note_key = ("note", fp)
        nodes[note_key] = Node(ntype, naxiom, ntitle, fp)

        blocks = parse_blocks(masked)
        for b in blocks:
            nodes[("block", b["id"])] = Node(b["type"], b["axiom"], b["id"], fp)

        for m, e in iter_edges(masked):
            if e.rel not in GRAPH_RELS:
                continue
            pos = m.start()
            src = note_key
            for b in blocks:
                if b["start"] <= pos < b["end"]:
                    src = ("block", b["id"])
                    break
            tgt = resolve_to_node(e.target, idx, e.is_link)
            if tgt is None:
                continue  # dangling/ambiguous already flagged by the linter
            edges.append((src, e.rel, tgt))
    return nodes, edges


def find_cycles(just_edges):
    """Return a list of cycles (each a list of node keys) in the directed
    justification graph. DFS with a recursion stack."""
    adj: dict = {}
    for src, tgt in just_edges:
        adj.setdefault(src, []).append(tgt)
    cycles, seen_sigs = [], set()
    WHITE, GREY, BLACK = 0, 1, 2
    colour: dict = {}

    def dfs(node, stack):
        colour[node] = GREY
        stack.append(node)
        for nxt in adj.get(node, []):
            if colour.get(nxt, WHITE) == GREY:      # back-edge → cycle
                cyc = stack[stack.index(nxt):] + [nxt]
                sig = frozenset(cyc)
                if sig not in seen_sigs:
                    seen_sigs.add(sig)
                    cycles.append(cyc)
            elif colour.get(nxt, WHITE) == WHITE:
                dfs(nxt, stack)
        stack.pop()
        colour[node] = BLACK

    for n in list(adj.keys()):
        if colour.get(n, WHITE) == WHITE:
            dfs(n, [])
    return cycles


def run_audit(files, idx: Index, yaml_mod, root: str):
    from collections import Counter
    nodes, edges = build_graph(files, idx, yaml_mod)

    # Split edges by kind and count degrees per relation.
    sup_out, sup_in = Counter(), Counter()   # supports
    dep_out, dep_in = Counter(), Counter()    # depends_on
    contra = Counter()                        # contradiction-degree (symmetric)
    just_edges, contra_edges = [], []
    for src, rel, tgt in edges:
        if rel == "supports":
            sup_out[src] += 1; sup_in[tgt] += 1
            just_edges.append((src, tgt))
        elif rel == "depends_on":
            dep_out[src] += 1; dep_in[tgt] += 1
            just_edges.append((src, tgt))
        elif rel == "contradicts":
            contra[src] += 1; contra[tgt] += 1
            contra_edges.append((src, tgt))

    participating = {k for e in edges for k in (e[0], e[2])}
    label = lambda k: nodes[k].label if k in nodes else k[1]
    is_claim = lambda k: bool(nodes.get(k)) and nodes[k].type == "claim"
    is_axiom = lambda k: bool(nodes.get(k)) and nodes[k].axiom

    # A node is GROUNDED if something supports it, or it's a declared axiom.
    grounded = lambda k: sup_in[k] >= 1 or is_axiom(k)
    # A node is LOAD-BEARING if it supports something OR something depends on it.
    load_bearing = lambda k: sup_out[k] >= 1 or dep_in[k] >= 1

    print("\n" + "=" * 60)
    print("ARGUMENT AUDIT  (v2: gaps · foundations · conflicts)")
    print("=" * 60)
    print(f"graph: {len(just_edges)} justification + {len(contra_edges)} contradiction "
          f"edge(s) among {len(participating)} node(s)")

    # C1 — gaps: load-bearing claims that aren't grounded and aren't axioms.
    gaps = [k for k in participating if is_claim(k) and load_bearing(k) and not grounded(k)]

    print("\n[C1] Unsupported claims (gaps)")
    print("     claims that carry weight but nothing grounds them, not marked axiom:")
    if gaps:
        for k in sorted(gaps, key=label):
            role = []
            if sup_out[k]:
                role.append(f"supports {sup_out[k]}")
            if dep_in[k]:
                role.append(f"depended-on by {dep_in[k]}")
            print(f"  ✗ {label(k)}  ({', '.join(role)})")
            print(f"      → add support, or set `axiom: true` if this is a chosen premise")
    else:
        print("  none")

    # C2 — foundations.
    declared = [k for k in participating if is_axiom(k)]
    bedrock = [k for k in participating
               if not is_claim(k) and not is_axiom(k) and sup_out[k] >= 1]

    print("\n[C2] Foundations (what everything rests on)")
    print(f"  declared axioms ({len(declared)}):")
    for k in sorted(declared, key=label):
        print(f"    • {label(k)}")
    if not declared:
        print("    none")
    print(f"  undeclared load-bearing claims ({len(gaps)}): "
          + ("see C1 gaps above" if gaps else "none"))
    print(f"  non-claim bedrock ({len(bedrock)}) — legitimate leaves (evidence, journals, SoTs):")
    for k in sorted(bedrock, key=label):
        print(f"    • {label(k)}  [{nodes[k].type or '?'}] supports {sup_out[k]}")
    if not bedrock:
        print("    none")

    # C3 — conflicts.
    print("\n[C3] Conflicts")
    print(f"  contradiction edges ({len(contra_edges)}):")
    if contra_edges:
        for src, tgt in sorted(contra_edges, key=lambda e: (label(e[0]), label(e[1]))):
            print(f"    ⚔  {label(src)}")
            print(f"        ✗ contradicts → {label(tgt)}")
    else:
        print("    none")

    # Live tensions: a supported claim that is also contradicted — you hold
    # something you have both argued for and argued against.
    tensions = [k for k in participating
                if is_claim(k) and sup_in[k] >= 1 and contra[k] >= 1]
    print(f"  live tensions ({len(tensions)}) — supported claims that are also in conflict:")
    if tensions:
        for k in sorted(tensions, key=lambda k: -sup_in[k]):
            print(f"    ⚠  {label(k)}  (supported by {sup_in[k]}, in conflict with {contra[k]})")
    else:
        print("    none")

    # Circular reasoning: cycles in the justification graph.
    cycles = find_cycles(just_edges)
    print(f"  circular reasoning ({len(cycles)}):")
    if cycles:
        for cyc in cycles:
            print("    ↻  " + " → ".join(label(k) for k in cyc))
    else:
        print("    none")

    print("\n" + "-" * 60)
    print(f"{len(gaps)} gap(s), {len(declared)} axiom(s), {len(bedrock)} bedrock, "
          f"{len(contra_edges)} contradiction(s), {len(tensions)} live tension(s), "
          f"{len(cycles)} cycle(s)")


def resolve_query(nodes, participating, query: str):
    """Resolve a title query to a single participating node key, else None.
    Tries exact, then case-insensitive, then substring match."""
    cands = [k for k in participating if nodes.get(k)]
    q = query.lower()
    for pred in (lambda n: n.label == query,
                 lambda n: n.label.lower() == q,
                 lambda n: q in n.label.lower()):
        hits = [k for k in cands if pred(nodes[k])]
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            print(f"ambiguous query '{query}' — {len(hits)} matches:", file=sys.stderr)
            for k in sorted(hits, key=lambda k: nodes[k].label)[:12]:
                print(f"  - {nodes[k].label}", file=sys.stderr)
            return None
    print(f"no node found matching '{query}'.", file=sys.stderr)
    return None


def run_thread(files, idx: Index, yaml_mod, query: str, mode: str):
    """C4 provenance. mode='why' walks what the node rests on (incoming supports
    + outgoing depends_on); mode='impact' walks what rests on it (the duals)."""
    nodes, edges = build_graph(files, idx, yaml_mod)
    sup_pred, sup_succ, dep_pred, dep_succ = {}, {}, {}, {}
    for src, rel, tgt in edges:
        if rel == "supports":
            sup_succ.setdefault(src, []).append(tgt)
            sup_pred.setdefault(tgt, []).append(src)
        elif rel == "depends_on":
            dep_succ.setdefault(src, []).append(tgt)
            dep_pred.setdefault(tgt, []).append(src)

    participating = {k for e in edges for k in (e[0], e[2])}
    label = lambda k: nodes[k].label if k in nodes else k[1]
    def tag(k):
        if nodes.get(k) and nodes[k].axiom:
            return "[axiom]"
        return f"[{nodes[k].type or '?'}]" if nodes.get(k) else "[?]"

    def neighbours(k):
        if mode == "why":
            res = [(a, "supported by") for a in sup_pred.get(k, [])]
            res += [(y, "rests on premise") for y in dep_succ.get(k, [])]
        else:
            res = [(b, "supports") for b in sup_succ.get(k, [])]
            res += [(a, "depended on by") for a in dep_pred.get(k, [])]
        seen, out = set(), []
        for c, rl in sorted(res, key=lambda x: label(x[0])):
            if c not in seen:
                seen.add(c)
                out.append((c, rl))
        return out

    root = resolve_query(nodes, participating, query)
    if root is None:
        return 2

    header = "WHY (what it rests on)" if mode == "why" else "IMPACT (what rests on it)"
    print("=" * 60)
    print(f"{header}: {label(root)}  {tag(root)}")
    print("=" * 60)

    leaves = []
    def walk(k, prefix, on_path, depth):
        kids = neighbours(k)
        if not kids:
            leaves.append(k)
        for i, (c, rl) in enumerate(kids):
            last = i == len(kids) - 1
            branch = "└─ " if last else "├─ "
            cont = "   " if last else "│  "
            if c in on_path:
                print(f"{prefix}{branch}{label(c)}  ({rl}) ↻ cycle")
                continue
            if depth >= 25:
                print(f"{prefix}{branch}… (max depth)")
                continue
            print(f"{prefix}{branch}{label(c)}  ({rl}) {tag(c)}")
            walk(c, prefix + cont, on_path | {c}, depth + 1)

    if not neighbours(root):
        print(f"  (no {'grounds' if mode=='why' else 'dependents'} recorded)")
    else:
        walk(root, "", {root}, 0)
        # terminals = axioms / evidence the thread bottoms out on (why mode)
        if mode == "why" and leaves:
            print("\nbottoms out on:")
            for k in sorted(set(leaves), key=label):
                print(f"  • {label(k)}  {tag(k)}")
    return 0


def run_route(files, idx: Index, yaml_mod, proposition: str, max_hits: int) -> int:
    """Find nearest existing claims by token overlap, with grounding status.
    
    Tokenises the proposition into words, scores each claim title by word
    overlap (Jaccard-like), and returns the top N hits with their grounding
    status: grounded / axiom / gap.
    """
    nodes, edges = build_graph(files, idx, yaml_mod)
    from collections import Counter

    sup_in, sup_out = Counter(), Counter()
    for src, rel, tgt in edges:
        if rel == "supports":
            sup_out[src] += 1; sup_in[tgt] += 1
        elif rel == "depends_on":
            sup_out[src] += 1; sup_in[tgt] += 1

    participating = {k for e in edges for k in (e[0], e[2])}
    label = lambda k: nodes[k].label if k in nodes else k[1]
    is_axiom = lambda k: bool(nodes.get(k)) and nodes[k].axiom
    grounded = lambda k: sup_in[k] >= 1 or is_axiom(k)
    is_claim = lambda k: bool(nodes.get(k)) and nodes[k].type == "claim"

    # Tokenise the query
    query_tokens = set(re.findall(r"[a-z0-9]+", proposition.lower()))

    # Score every claim participating in the graph
    scores = []
    for k in participating:
        if not is_claim(k):
            continue
        title = label(k)
        title_tokens = set(re.findall(r"[a-z0-9]+", title.lower()))
        if not title_tokens:
            continue
        overlap = len(query_tokens & title_tokens)
        if overlap == 0:
            continue
        jaccard = overlap / len(query_tokens | title_tokens)
        scores.append((jaccard, overlap, k, title))

    scores.sort(key=lambda x: (-x[0], -x[1], x[3]))
    scores = scores[:max_hits]

    print("=" * 60)
    print(f"ROUTE: {proposition}")
    print("=" * 60)
    print(f"  {len(scores)} claim(s) matched in graph\n")

    if not scores:
        print("  No graph-participating claims matched. Try --audit for C1 gaps.")
        return 0

    print(f"  {'Score':>6}  {'Status':>10}  {'Title'}")
    print(f"  {'-'*6}  {'-'*10}  {'-'*50}")
    for jaccard, overlap, k, title in scores:
        if grounded(k):
            status = "grounded"
        elif is_axiom(k):
            status = "axiom"
        else:
            status = "GAP"
        print(f"  {jaccard:>5.2f}  {status:>10}  {title}")

    # Also show unmatched claim titles from the vault (those not in graph)
    # by scanning the full vault
    print("\n--- Claims not yet in the graph (no edges) ---")
    unmatched = 0
    for fp in files:
        try:
            text = open(fp, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        ntype, naxiom, ntitle = note_meta(text, yaml_mod, fp)
        if ntype != "claim":
            continue
        if ("note", fp) in participating:
            continue
        title_tokens = set(re.findall(r"[a-z0-9]+", ntitle.lower()))
        if not title_tokens:
            continue
        overlap = len(query_tokens & title_tokens)
        if overlap == 0:
            continue
        jaccard = overlap / len(query_tokens | title_tokens)
        if jaccard < 0.15:
            continue
        unmatched += 1
        if unmatched <= max_hits:
            print(f"  • {ntitle}  (score={jaccard:.2f})")

    return 0


def collect_files(root: str):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if fn.endswith(".md"):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def default_root() -> str:
    # 10_System/scripts/edge_lint.py -> vault root is two dirs up.
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint typed edges (%%type.rel{target}%%) across the vault.")
    ap.add_argument("--path", default=None, help="folder to lint (default: auto-detected vault root)")
    ap.add_argument("--quiet", action="store_true", help="only show files with findings")
    ap.add_argument("--audit", action="store_true",
                    help="also print the argument audit (C1 gaps + C2 foundations + C3 conflicts)")
    ap.add_argument("--route", metavar="PROPOSITION",
                    help="find nearest existing claims for a proposition, with grounding status")
    ap.add_argument("--max-route-hits", default=12, type=int, metavar="N",
                    help="max results for --route (default 12)")
    ap.add_argument("--why", metavar="TITLE",
                    help="print the justification tree for a claim (what it rests on)")
    ap.add_argument("--impact", metavar="TITLE",
                    help="print the impact tree for a claim (what rests on it)")
    args = ap.parse_args()

    root = os.path.abspath(args.path) if args.path else default_root()
    yaml_mod = require_yaml()

    files = collect_files(root)
    idx = build_index(files, yaml_mod)

    # Focused queries skip the lint report entirely.
    if args.route:
        return run_route(files, idx, yaml_mod, args.route, args.max_route_hits)
    if args.why:
        return run_thread(files, idx, yaml_mod, args.why, "why")
    if args.impact:
        return run_thread(files, idx, yaml_mod, args.impact, "impact")

    total_edges = 0
    n_err = n_warn = n_files_with_edges = 0
    reported = []

    for fp in files:
        findings, edges_here = lint_file(fp, idx)
        if edges_here:
            n_files_with_edges += 1
            total_edges += edges_here
        if findings:
            reported.append((fp, findings))
            n_err += sum(1 for f in findings if f.level == "ERROR")
            n_warn += sum(1 for f in findings if f.level == "WARN")

    rel = lambda p: os.path.relpath(p, root)
    for fp, findings in reported:
        print(f"\n{rel(fp)}")
        for f in sorted(findings, key=lambda x: (x.line, x.level)):
            print(f"  {f.level:5} L{f.line}: {f.message}")

    if not args.quiet and not reported:
        print("No edge violations found.")

    print("\n" + "-" * 60)
    print(f"scanned {len(files)} notes · {total_edges} edges in {n_files_with_edges} notes")
    print(f"{n_err} error(s), {n_warn} warning(s)")

    if args.audit:
        run_audit(files, idx, yaml_mod, root)

    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
