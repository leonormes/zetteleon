#!/usr/bin/env python3
"""
verify_quote.py - checks that a quotation appears verbatim in a book of the Calibre
library, and reports where: the EPUB spine file and chapter, and the PDF page.

Why: a quote in an Evidence section is only citable if it is the author's exact words.
This script reads the book files themselves (never the search index), so it is the check
to run before a quote goes into a note.

Read-only. It opens the Calibre database in read-only mode and never writes to the library.

Verdicts (strongest first):
    verbatim      the quote matches the book text after collapsing whitespace only
    normalised    it matches once curly/straight quotes, dash types, soft hyphens and
                  line-break hyphenation are ignored (the characters differ, the words do not)
    elided        the quote has ... or [...] gaps and every part is found, in order,
                  close together (each part checked as above)
    not_found     no match. The output shows the longest leading and trailing part of the
                  quote that does appear, and what the book says next, so a changed word
                  is easy to see.

Usage (run from anywhere):
    uv run --with pymupdf python3 10_System/scripts/verify_quote.py --id 1575 --quote "Ludwig Wittgenstein was a philosopher."
    uv run --with pymupdf python3 10_System/scripts/verify_quote.py --title "Grayling" --quote-file quotes.txt
    echo "some quote" | uv run --with pymupdf python3 10_System/scripts/verify_quote.py --id 1575
    uv run --with pymupdf python3 10_System/scripts/verify_quote.py --path "/path/to/book.epub" --quote "..."
    uv run --with pymupdf python3 10_System/scripts/verify_quote.py --self-test

Options:
    --id N | --title TEXT | --path FILE   which book (Calibre id, title/author substring, or a file)
    --quote TEXT                          repeatable; or --quote-file (quotes separated by blank lines);
                                          or standard input (quotes separated by blank lines)
    --format any|epub|pdf                 which file(s) to search (default: both, if present)
    --library DIR                         Calibre library (default: $ARCHILLES_LIBRARY_PATH, else
                                          ~/My Drive/GCcalibreBooks)
    --json                                machine-readable output
    --context N                           characters of context to show (default 70)

PDF support needs pymupdf (uv run --with pymupdf). Without it the PDF is skipped with a note.
EPUB support is standard library only.

Exit code: 0 if every quote was found (any verdict but not_found), 1 if any was not found,
2 on a usage or file error.

Output: for each found quote a paste-ready citation line, for example
    (Simler and Hanson 2018, ch. 5, PDF p. 88) · [open in Calibre](calibre://view-book/GCcalibreBooks/1594/EPUB?open_at=toc:5%20Self-Deception)
and, once per book, a full reference for a Further Reading list. The link opens the chapter in
the desktop Calibre viewer (it does not work on a phone).

Limits: an EPUB has no fixed pages, so the locator is the spine file plus the chapter title
from the book's table of contents. A PDF gives the physical page (1-based); the printed page
number is reported only when the PDF carries page labels, which many scanned or converted
files do not. The script finds words, not meaning: it cannot tell you that a quote is fair.
"""

import argparse
import bisect
import glob
import html
import json
import os
import re
import sqlite3
import sys
import unicodedata
import zipfile
from xml.etree import ElementTree as ET

try:
    import pymupdf  # type: ignore
except Exception:  # pragma: no cover
    try:
        import fitz as pymupdf  # type: ignore
    except Exception:
        pymupdf = None

DEFAULT_LIBRARIES = [
    "~/My Drive/GCcalibreBooks",
    "/Volumes/DAL/GCcalibreBooks/GCcalibreBooks",
]
GAP_RE = re.compile(r"\s*(?:\[\s*(?:\.\.\.|…)\s*\]|\.\.\.|…)\s*")
BLOCK_TAGS = r"(?:p|div|br|li|ul|ol|h[1-6]|tr|td|th|table|blockquote|section|article|header|footer|aside|figure|figcaption|dt|dd|pre|hr)"
MIN_SEGMENT = 12          # shortest part of an elided quote that is checked on its own
MAX_GAP_CHARS = 4000      # parts of an elided quote must lie within this distance


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

_QUOTES = {"‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'",
           "“": '"', "”": '"', "„": '"', "‟": '"', "″": '"'}
_DASHES = {"‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-",
           "―": "-", "−": "-"}


def collapse(s):
    """Whitespace-only normalisation: the 'verbatim' level."""
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


def fold(s, dehyphenate=False):
    """Character-level normalisation: the 'normalised' level."""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("­", "")
    s = "".join(_QUOTES.get(c, _DASHES.get(c, c)) for c in s)
    s = collapse(s)
    if dehyphenate:
        s = re.sub(r"(?<=[A-Za-z])- (?=[a-z])", "", s)
    return s


# ---------------------------------------------------------------------------
# Text sources: each yields (label, text) units, then joined with offset maps
# ---------------------------------------------------------------------------

class Corpus:
    """A book as one string with a map from character offset to a unit (file or page)."""

    def __init__(self, units, kind):
        self.kind = kind
        self.units = units                      # list of dict(label, ...)
        self.text = ""
        self.starts = []
        for u in units:
            self.starts.append(len(self.text))
            self.text += u["text"] + " "
        self.starts_arr = self.starts

    def unit_at(self, offset):
        i = bisect.bisect_right(self.starts_arr, offset) - 1
        return self.units[max(i, 0)]


def _strip_html(raw):
    raw = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<" + BLOCK_TAGS + r"\b[^>]*/?>", " ", raw, flags=re.I)
    raw = re.sub(r"</" + BLOCK_TAGS + r"\s*>", " ", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", "", raw)
    return html.unescape(raw)


def _xml(zf, name):
    return ET.fromstring(zf.read(name))


def _strip_ns(tag):
    return tag.split("}", 1)[-1]


def epub_corpus(path):
    zf = zipfile.ZipFile(path)
    container = _xml(zf, "META-INF/container.xml")
    opf_path = None
    for el in container.iter():
        if _strip_ns(el.tag) == "rootfile":
            opf_path = el.attrib.get("full-path")
            break
    if not opf_path:
        raise ValueError("EPUB has no rootfile in META-INF/container.xml")
    base = os.path.dirname(opf_path)
    opf = _xml(zf, opf_path)

    manifest, spine, nav_href, ncx_href = {}, [], None, None
    for el in opf.iter():
        t = _strip_ns(el.tag)
        if t == "item":
            manifest[el.attrib["id"]] = (el.attrib["href"], el.attrib.get("media-type", ""),
                                         el.attrib.get("properties", ""))
            if "nav" in el.attrib.get("properties", "").split():
                nav_href = el.attrib["href"]
            if el.attrib.get("media-type") == "application/x-dtbncx+xml":
                ncx_href = el.attrib["href"]
        elif t == "itemref":
            spine.append(el.attrib["idref"])

    def full(href):
        href = href.split("#", 1)[0]
        return os.path.normpath(os.path.join(base, href)).replace("\\", "/")

    toc = {}   # spine file (full path) -> first TOC title that points at it

    def add_toc(href, title):
        key = full(href)
        title = collapse(html.unescape(re.sub(r"<[^>]+>", "", title)))
        if title and key not in toc:
            toc[key] = title

    try:
        if nav_href:
            nav_raw = zf.read(full(nav_href)).decode("utf-8", "ignore")
            nav_dir = os.path.dirname(full(nav_href))
            for m in re.finditer(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', nav_raw, re.S | re.I):
                target = os.path.normpath(os.path.join(nav_dir, m.group(1).split("#", 1)[0])).replace("\\", "/")
                title = collapse(html.unescape(re.sub(r"<[^>]+>", "", m.group(2))))
                if title and target not in toc:
                    toc[target] = title
        elif ncx_href:
            ncx = _xml(zf, full(ncx_href))
            ncx_dir = os.path.dirname(full(ncx_href))
            for np in ncx.iter():
                if _strip_ns(np.tag) == "navPoint":
                    label = src = None
                    for ch in np:
                        if _strip_ns(ch.tag) == "navLabel":
                            label = "".join(ch.itertext())
                        elif _strip_ns(ch.tag) == "content":
                            src = ch.attrib.get("src")
                    if label and src:
                        target = os.path.normpath(os.path.join(ncx_dir, src.split("#", 1)[0])).replace("\\", "/")
                        t = collapse(label)
                        if t and target not in toc:
                            toc[target] = t
    except Exception:
        pass  # chapter titles are a convenience; text matching must not depend on them

    units = []
    last_title = None
    for idref in spine:
        href, mtype, _props = manifest.get(idref, (None, "", ""))
        if not href or "html" not in mtype:
            continue
        name = full(href)
        try:
            raw = zf.read(name).decode("utf-8", "ignore")
        except KeyError:
            continue
        text = collapse(_strip_html(raw))
        if not text:
            continue
        title = toc.get(name)
        if title:
            last_title = title
        else:
            m = re.search(r"<h[1-3]\b[^>]*>(.*?)</h[1-3]>", raw, re.S | re.I)
            if m:
                guess = collapse(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))))
                if guess:
                    title = guess
        units.append({"label": name, "chapter": title or last_title, "text": text})
    return Corpus(units, "epub")


def pdf_corpus(path):
    if pymupdf is None:
        raise RuntimeError("pymupdf is not installed (run with: uv run --with pymupdf ...)")
    doc = pymupdf.open(path)
    toc = doc.get_toc(simple=True) or []        # [level, title, page(1-based)]
    toc_by_page = sorted((p, t) for _lvl, t, p in toc if p and p > 0)
    units = []
    for i, page in enumerate(doc):
        text = collapse(page.get_text())
        try:
            printed = page.get_label() or None
        except Exception:
            printed = None
        chapter = None
        for p, t in toc_by_page:
            if p <= i + 1:
                chapter = collapse(t)
            else:
                break
        if chapter is None:
            first = [l.strip() for l in page.get_text().splitlines() if l.strip()][:2]
            if first and re.match(r"(?i)^(chapter|part|section)\b", first[0]):
                chapter = collapse(" ".join(first))
        units.append({"label": f"p. {i + 1}", "page": i + 1, "printed": printed,
                      "chapter": chapter, "text": text})
    return Corpus(units, "pdf")


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def find_all(hay, needle, limit=50):
    out, i = [], hay.find(needle)
    while i != -1 and len(out) < limit:
        out.append(i)
        i = hay.find(needle, i + 1)
    return out


def locate(corpus, quote):
    """Return (level, [offsets in the corpus text], hay_for_offsets) or (None, [], None)."""
    raw_hay = corpus.text
    q1 = collapse(quote)
    hits = find_all(raw_hay, q1)
    if hits:
        return "verbatim", hits, raw_hay
    folded_hay = fold(raw_hay, dehyphenate=(corpus.kind == "pdf"))
    q2 = fold(quote)
    hits = find_all(folded_hay, q2)
    if hits:
        return "normalised", hits, folded_hay
    return None, [], folded_hay


def unit_for_folded(corpus, folded_hay, offset):
    """Offsets in the folded text drift from the raw text; map by proportion, then correct
    by searching the raw units for the matched words. Used only for the 'normalised' level."""
    # Rebuild the per-unit folded text so the offset maps exactly.
    pos = 0
    for u in corpus.units:
        ft = fold(u["text"], dehyphenate=(corpus.kind == "pdf"))
        end = pos + len(ft) + 1
        if offset < end:
            return u
        pos = end
    return corpus.units[-1]


def occurrences(corpus, level, hits, hay, qlen):
    out = []
    for off in hits[:5]:
        if level == "verbatim":
            u = corpus.unit_at(off)
        else:
            u = unit_for_folded(corpus, hay, off)
        out.append((off, u))
    return out


def context(hay, off, qlen, n):
    a, b = max(0, off - n), min(len(hay), off + qlen + n)
    return ("…" if a else "") + hay[a:off] + "⟦" + hay[off:off + qlen] + "⟧" + hay[off + qlen:b] + ("…" if b < len(hay) else "")


def split_parts(quote):
    parts = [p for p in GAP_RE.split(quote) if collapse(p)]
    return parts


def check_elided(corpus, quote):
    parts = split_parts(quote)
    if len(parts) < 2:
        return None
    if any(len(collapse(p)) < MIN_SEGMENT for p in parts):
        return {"error": f"each part around an ellipsis must be at least {MIN_SEGMENT} characters"}
    found, prev_end = [], None
    for p in parts:
        lvl, hits, hay = locate(corpus, p)
        if not hits:
            return {"missing": collapse(p)}
        pick = None
        for h in hits:
            if prev_end is None or (0 <= h - prev_end <= MAX_GAP_CHARS):
                pick = h
                break
        if pick is None:
            return {"out_of_order": collapse(p)}
        found.append((lvl, pick, len(fold(p) if lvl == "normalised" else collapse(p)), hay))
        prev_end = pick + found[-1][2]
    return {"parts": found}


def longest_prefix(hay, q, floor=12):
    """Longest leading part of q that occurs in hay (monotone, so binary search)."""
    lo, hi, best = floor, len(q), 0
    if q[:floor] not in hay:
        return 0, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if q[:mid] in hay:
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return best, hay.find(q[:best])


def diagnose(corpus, quote):
    hay = fold(corpus.text, dehyphenate=(corpus.kind == "pdf"))
    q = fold(quote)
    out = {}
    n, off = longest_prefix(hay, q)
    if n:
        out["leading_match"] = {"chars": n, "of": len(q), "quote_next": q[n:n + 50],
                                "book_next": hay[off + n:off + n + 50]}
    rq, rhay = q[::-1], hay[::-1]
    n2, off2 = longest_prefix(rhay, rq)
    if n2:
        start = len(hay) - off2 - n2
        out["trailing_match"] = {"chars": n2, "of": len(q), "quote_before": q[max(0, len(q) - n2 - 50):len(q) - n2],
                                 "book_before": hay[max(0, start - 50):start]}
    return out


# ---------------------------------------------------------------------------
# Calibre lookup
# ---------------------------------------------------------------------------

def find_library(arg):
    cands = [arg] if arg else [os.environ.get("ARCHILLES_LIBRARY_PATH")] + DEFAULT_LIBRARIES
    for c in cands:
        if c:
            p = os.path.expanduser(c)
            if os.path.exists(os.path.join(p, "metadata.db")):
                return p
    return None


def calibre_rows(lib, book_id=None, title=None):
    con = sqlite3.connect(f"file:{os.path.join(lib, 'metadata.db')}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    q = ("select b.id, b.title, b.path, substr(b.pubdate,1,10) as pubdate, "
         "(select group_concat(a.name, ' & ') from books_authors_link l join authors a on a.id=l.author where l.book=b.id) as authors, "
         "(select p.name from books_publishers_link l join publishers p on p.id=l.publisher where l.book=b.id) as publisher, "
         "(select val from identifiers i where i.book=b.id and i.type='isbn' limit 1) as isbn, "
         "(select group_concat(format) from data d where d.book=b.id) as formats from books b ")
    if book_id is not None:
        rows = con.execute(q + "where b.id=?", (book_id,)).fetchall()
    else:
        like = f"%{title}%"
        rows = con.execute(q + "where b.title like ? or b.id in (select l.book from books_authors_link l "
                           "join authors a on a.id=l.author where a.name like ?)", (like, like)).fetchall()
    con.close()
    return [dict(r) for r in rows]


def book_files(lib, row, fmt):
    d = os.path.join(lib, row["path"])
    out = []
    for ext in ("epub", "pdf"):
        if fmt in ("any", ext):
            out += sorted(glob.glob(os.path.join(d, "*." + ext)))
    return out


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def year_of(row):
    pd = (row or {}).get("pubdate") or ""
    return pd[:4] if pd[:4].isdigit() and pd[:4] != "0101" else None


LIB_NAME = "GCcalibreBooks"
_WORD_NUMS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
    "sixteen seventeen eighteen nineteen twenty".split())}


def _surnames(row):
    names = [n for n in (row.get("authors") or "").split(" & ") if n]
    last = [n.rsplit(" ", 1)[-1] for n in names]
    if not last:
        return "Unknown"
    if len(last) == 1:
        return last[0]
    if len(last) == 2:
        return f"{last[0]} and {last[1]}"
    return f"{last[0]} et al."


def chapter_ref(title):
    """'5 Self-Deception' -> 'ch. 5'; 'CHAPTER 21' -> 'ch. 21'; 'EIGHT Thinking...' -> 'ch. 8';
    otherwise the title in quotes."""
    if not title:
        return None
    t = collapse(title)
    m = re.match(r"(?i)^(?:chapter|ch\.?)\s*(\d+)\b", t) or re.match(r"^(\d+)(?:[.\s]|$)", t)
    if m:
        return f"ch. {m.group(1)}"
    first = t.split(" ", 1)[0].lower().strip(".")
    if first in _WORD_NUMS and len(t.split()) > 1:
        return f"ch. {_WORD_NUMS[first]}"
    return f'"{t}"'


def calibre_link(row, matches):
    epub = next((m for m in matches if m["kind"] == "epub"), None)
    base = f"calibre://view-book/{LIB_NAME}/{row['id']}/"
    if epub and epub.get("chapter"):
        return base + "EPUB?open_at=" + quote_url("toc:" + epub["chapter"])
    if epub:
        return base + "EPUB"
    return base + "PDF"


def quote_url(s):
    from urllib.parse import quote
    return quote(s, safe=":-")


def cite_string(row, matches):
    """Paste-ready citation line: (Author Year, ch. N, PDF p. M) · [open in Calibre](link)."""
    if not row or not matches:
        return None
    y = year_of(row) or "n.d."
    epub = next((m for m in matches if m["kind"] == "epub"), None)
    pdf = next((m for m in matches if m["kind"] == "pdf"), None)
    chap = chapter_ref((epub or pdf or {}).get("chapter"))
    parts = [f"{_surnames(row)} {y}"]
    if chap:
        parts.append(chap)
    if pdf:
        parts.append(f"p. {pdf['printed']}" if pdf.get("printed") else f"PDF p. {pdf['page']}")
    return f"({', '.join(parts)}) \u00b7 [open in Calibre]({calibre_link(row, matches)})"


def reference_string(row):
    """Full reference for Further Reading: Last, First, and First Last. Year. *Title*. Publisher. link."""
    names = [n for n in (row.get("authors") or "").split(" & ") if n]
    if names:
        bits = names[0].rsplit(" ", 1)
        who = f"{bits[-1]}, {bits[0]}" if len(bits) == 2 else names[0]
        if len(names) == 2:
            who += f", and {names[1]}"
        elif len(names) > 2:
            who += " et al."
    else:
        who = "Unknown"
    y = year_of(row) or "n.d."
    pub = (row.get("publisher") or "").strip()
    fmt = "EPUB" if "EPUB" in (row.get("formats") or "") else "PDF"
    return (f"{who.rstrip('.')}. {y}. *{row['title']}*." + (f" {pub}." if pub else "")
            + f" [Open in Calibre](calibre://view-book/{LIB_NAME}/{row['id']}/{fmt})")


def verify_one(quote, corpora, ctx):
    result = {"quote": quote, "verdict": "not_found", "matches": [], "diagnostics": {}}
    levels = []
    for corpus in corpora:
        level, hits, hay = locate(corpus, quote)
        if hits:
            levels.append(level)
            for off, u in occurrences(corpus, level, hits, hay, len(quote)):
                m = {"kind": corpus.kind, "level": level, "count": len(hits),
                     "context": context(hay, off, len(fold(quote) if level == "normalised" else collapse(quote)), ctx)}
                if corpus.kind == "epub":
                    m.update(file=u["label"], chapter=u.get("chapter"))
                else:
                    m.update(page=u["page"], printed=u.get("printed"), chapter=u.get("chapter"))
                result["matches"].append(m)
                break  # first occurrence per source; the count shows ambiguity
            continue
        el = check_elided(corpus, quote)
        if el and "parts" in el:
            levels.append("elided")
            lvl, pick, ln, hay2 = el["parts"][0]
            u = corpus.unit_at(pick) if lvl == "verbatim" else unit_for_folded(corpus, hay2, pick)
            m = {"kind": corpus.kind, "level": "elided", "count": 1,
                 "context": context(hay2, pick, ln, ctx)}
            if corpus.kind == "epub":
                m.update(file=u["label"], chapter=u.get("chapter"))
            else:
                m.update(page=u["page"], printed=u.get("printed"), chapter=u.get("chapter"))
            result["matches"].append(m)
        elif el and ("missing" in el or "out_of_order" in el or "error" in el):
            result["diagnostics"][corpus.kind + "_elision"] = el
    if levels:
        order = ["verbatim", "normalised", "elided"]
        result["verdict"] = min(levels, key=order.index)
    else:
        for corpus in corpora:
            d = diagnose(corpus, quote)
            if d:
                result["diagnostics"][corpus.kind] = d
    return result


def read_quotes(args):
    quotes = list(args.quote or [])
    texts = []
    if args.quote_file:
        texts.append(open(args.quote_file, encoding="utf-8").read())
    if not quotes and not texts and not sys.stdin.isatty():
        texts.append(sys.stdin.read())
    for t in texts:
        quotes += [collapse(b) for b in re.split(r"\n\s*\n", t) if collapse(b)]
    return [q for q in (collapse(x) for x in quotes) if q]


def print_human(book, res_list, files, notes):
    if book:
        y = year_of(book)
        print(f"{book['title']} - {book.get('authors') or '?'}" + (f" ({y})" if y else "") + f"  [calibre {book['id']}]")
    for n in notes:
        print(f"  note: {n}")
    print(f"  searched: {', '.join(os.path.basename(f) for f in files)}")
    if book:
        print(f"  reference: {reference_string(book)}")
    for r in res_list:
        q = r["quote"]
        shown = q if len(q) <= 90 else q[:87] + "..."
        print(f"\n{r['verdict'].upper():10} \"{shown}\"")
        for m in r["matches"]:
            if m["kind"] == "epub":
                loc = f"{m['file']}" + (f"  chapter: \"{m['chapter']}\"" if m.get("chapter") else "")
            else:
                label = f"p. {m['page']} (physical" + (f", printed {m['printed']}" if m.get("printed") else ", no printed label") + ")"
                loc = label + (f"  chapter: \"{m['chapter']}\"" if m.get("chapter") else "")
            extra = f"  [{m['count']} occurrences]" if m.get("count", 1) > 1 else ""
            print(f"  {m['kind'].upper():5} {m['level']:10} {loc}{extra}")
            print(f"        {m['context']}")
        for kind, d in r["diagnostics"].items():
            if kind.endswith("_elision"):
                print(f"  {kind.split('_')[0].upper()}: elision check failed: {d}")
                continue
            lm, tm = d.get("leading_match"), d.get("trailing_match")
            if lm:
                print(f"  {kind.upper()}: first {lm['chars']} of {lm['of']} characters match. Quote goes on: \"{lm['quote_next']}\"  Book says: \"{lm['book_next']}\"")
            if tm:
                print(f"  {kind.upper()}: last {tm['chars']} of {tm['of']} characters match. Quote has before: \"{tm['quote_before']}\"  Book has: \"{tm['book_before']}\"")
        if r["verdict"] != "not_found" and book:
            c = cite_string(book, r["matches"])
            if c:
                print(f"  paste: {c}")


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def _make_epub(path):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("mimetype", "application/epub+zip")
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">'
                   '<rootfiles><rootfile full-path="OPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        z.writestr("OPS/content.opf",
                   '<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0"><manifest>'
                   '<item id="n" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
                   '<item id="c1" href="ch1.xhtml" media-type="application/xhtml+xml"/>'
                   '<item id="c2" href="ch2.xhtml" media-type="application/xhtml+xml"/></manifest>'
                   '<spine><itemref idref="c1"/><itemref idref="c2"/></spine></package>')
        z.writestr("OPS/nav.xhtml", '<html><body><nav><ol><li><a href="ch1.xhtml">One</a></li>'
                                    '<li><a href="ch2.xhtml">Two</a></li></ol></nav></body></html>')
        z.writestr("OPS/ch1.xhtml", "<html><body><h1>One</h1><p>It doesn’t demonstrate loyalty to be<i>lie</i>ve the truth, "
                                    "which we have every incentive to believe anyway.</p><p>A second paragraph about badges "
                                    "and tribes follows here.</p></body></html>")
        z.writestr("OPS/ch2.xhtml", "<html><body><h1>Two</h1><p>Elsewhere the book argues that group interests shape "
                                    "party allegiances, and later adds a long aside before it concludes plainly.</p></body></html>")


def self_test():
    import tempfile
    failures = []

    def expect(name, cond):
        if not cond:
            failures.append(name)

    with tempfile.TemporaryDirectory() as d:
        ep = os.path.join(d, "t.epub")
        _make_epub(ep)
        c = [epub_corpus(ep)]
        r = verify_one("A second paragraph about badges and tribes follows here.", c, 40)
        expect("verbatim found", r["verdict"] == "verbatim")
        expect("verbatim chapter", r["matches"] and r["matches"][0]["chapter"] == "One")
        r = verify_one("It doesn't demonstrate loyalty to believe the truth", c, 40)
        expect("curly apostrophe is normalised, not verbatim", r["verdict"] == "normalised")
        r = verify_one("It doesn’t demonstrate loyalty to believe the truth", c, 40)
        expect("inline tag split word is joined", r["verdict"] == "verbatim")
        r = verify_one("A second paragraph about badges and tribes follows there.", c, 40)
        expect("changed word is not found", r["verdict"] == "not_found")
        expect("diagnostic names the divergence", "epub" in r["diagnostics"] and
               r["diagnostics"]["epub"].get("leading_match", {}).get("book_next", "").startswith("here"))
        r = verify_one("group interests shape party allegiances ... before it concludes plainly", c, 40)
        expect("elided found", r["verdict"] == "elided")
        expect("elided chapter", r["matches"] and r["matches"][0]["chapter"] == "Two")
        r = verify_one("group interests shape party allegiances ... before it concludes loudly", c, 40)
        expect("elided with a wrong part fails", r["verdict"] == "not_found")
        r = verify_one("loyalty to believe the truth, which we have every incentive to believe anyway. A second paragraph", c, 40)
        expect("quote spanning two paragraphs found", r["verdict"] == "verbatim")
        if pymupdf is not None:
            pdf = os.path.join(d, "t.pdf")
            doc = pymupdf.open()
            p1 = doc.new_page()
            p1.insert_text((72, 72), "Chapter 1")
            p1.insert_text((72, 100), "First page text about loyalty and the popu-")
            p2 = doc.new_page()
            p2.insert_text((72, 72), "lation of tribes continues on the second page.")
            doc.save(pdf)
            pc = [pdf_corpus(pdf)]
            r = verify_one("loyalty and the population of tribes continues on the second page", pc, 40)
            expect("pdf cross-page hyphenated quote found", r["verdict"] in ("normalised", "verbatim"))
            r = verify_one("First page text about loyalty", pc, 40)
            expect("pdf page located", r["matches"] and r["matches"][0]["page"] == 1)
        else:
            print("note: pymupdf not installed, PDF self-tests skipped")
    expect("chapter ref numeric", chapter_ref("5 Self-Deception") == "ch. 5")
    expect("chapter ref CHAPTER", chapter_ref("CHAPTER 21") == "ch. 21")
    expect("chapter ref word number", chapter_ref("EIGHT Thinking About Science") == "ch. 8")
    expect("chapter ref dotted", chapter_ref("10. REPRESENTATION, ELECTIONS AND VOTING") == "ch. 10")
    expect("chapter ref title fallback", chapter_ref("Aims and background") == '"Aims and background"')
    row = {"id": 9, "title": "T", "authors": "Ann Lee & Bo Kim", "pubdate": "2018-01-01", "publisher": "P", "formats": "EPUB"}
    c = cite_string(row, [{"kind": "epub", "chapter": "3 Foo bar"}, {"kind": "pdf", "page": 40, "printed": None, "chapter": "3 Foo bar"}])
    expect("cite string", c == "(Lee and Kim 2018, ch. 3, PDF p. 40) \u00b7 [open in Calibre](calibre://view-book/GCcalibreBooks/9/EPUB?open_at=toc:3%20Foo%20bar)")
    if failures:
        print("self-test FAILED: " + ", ".join(failures))
        return 1
    print("self-test passed")
    return 0


# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="Verify a quote verbatim against a Calibre book (EPUB/PDF).")
    ap.add_argument("--id", type=int)
    ap.add_argument("--title")
    ap.add_argument("--path")
    ap.add_argument("--quote", action="append")
    ap.add_argument("--quote-file")
    ap.add_argument("--format", choices=["any", "epub", "pdf"], default="any")
    ap.add_argument("--library")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--context", type=int, default=70)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    book, files, notes = None, [], []
    if args.path:
        if not os.path.exists(args.path):
            print(f"error: no such file: {args.path}", file=sys.stderr)
            return 2
        files = [args.path]
    elif args.id is not None or args.title:
        lib = find_library(args.library)
        if not lib:
            print("error: Calibre library not found; pass --library or set ARCHILLES_LIBRARY_PATH", file=sys.stderr)
            return 2
        rows = calibre_rows(lib, args.id, args.title)
        if not rows:
            print("error: no matching book in the Calibre library", file=sys.stderr)
            return 2
        if len(rows) > 1:
            print("error: more than one match; pass --id:", file=sys.stderr)
            for r in rows[:15]:
                print(f"  {r['id']:>5}  {r['title']}  ({r.get('authors')})", file=sys.stderr)
            return 2
        book = rows[0]
        global LIB_NAME
        LIB_NAME = os.path.basename(lib.rstrip("/")).replace(" ", "_")
        files = book_files(lib, book, args.format)
        if not files:
            print(f"error: no {args.format} file for calibre {book['id']} (formats: {book.get('formats')})", file=sys.stderr)
            return 2
    else:
        print("error: give --id, --title or --path", file=sys.stderr)
        return 2

    quotes = read_quotes(args)
    if not quotes:
        print("error: no quote given (--quote, --quote-file or standard input)", file=sys.stderr)
        return 2

    corpora = []
    for f in files:
        try:
            if f.lower().endswith(".epub"):
                corpora.append(epub_corpus(f))
            elif f.lower().endswith(".pdf"):
                corpora.append(pdf_corpus(f))
        except Exception as e:
            notes.append(f"skipped {os.path.basename(f)}: {e}")
    if not corpora:
        print("error: could not read any book file: " + "; ".join(notes), file=sys.stderr)
        return 2

    results = [verify_one(q, corpora, args.context) for q in quotes]
    if args.json:
        out = {"book": book, "files": files, "notes": notes, "results": results}
        for r in results:
            c = cite_string(book, r["matches"]) if r["verdict"] != "not_found" else None
            r["cite"] = c
        out["reference"] = reference_string(book) if book else None
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        print_human(book, results, files, notes)
    return 1 if any(r["verdict"] == "not_found" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
