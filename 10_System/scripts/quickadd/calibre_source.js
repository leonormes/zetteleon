// QuickAdd user script for the "Source" macro.
// Asks for a Calibre ID (or a plain title) and sets the variables that the
// "Source note (template)" choice uses to build the note.
//
// Read-only: for a Calibre ID it runs ONE fixed SELECT through /usr/bin/sqlite3
// in read-only mode. The ID is checked to be digits only before it reaches SQL.
// It never writes to Calibre and never writes to the vault itself.

const nodeRequire = typeof require === "function" ? require : window.require;
const { execFileSync } = nodeRequire("child_process");
const fs = nodeRequire("fs");

const SQLITE = "/usr/bin/sqlite3";
const LIBRARY_NAME = "GCcalibreBooks"; // used in calibre://view-book/<library>/<id>/<format>
const LIBRARY_DIRS = [
  "/Users/leon.ormes/My Drive/GCcalibreBooks",
  "/Volumes/DAL/GCcalibreBooks/GCcalibreBooks", // stale snapshot, fallback only
];

// Frontmatter-safe text: no colon-space, no double quotes, no straight apostrophes
// (the Obsidian Linter breaks on those in generated frontmatter values).
const clean = (s) =>
  String(s ?? "")
    .replace(/\s+/g, " ")
    .replace(/: /g, " - ")
    .replace(/"/g, "")
    .replace(/'/g, "’")
    .trim();

// File-name-safe text: also drop characters Obsidian does not allow or links dislike.
const fileSafe = (s) =>
  clean(s)
    .replace(/[\\/*<>|?:#^[\]]/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 120);

module.exports = async (params) => {
  const { app, quickAddApi, variables } = params;

  const raw = String((await quickAddApi.inputPrompt("Source: Calibre ID, or a title")) ?? "").trim();
  if (!raw) params.abort("No source given.");

  let meta = { title: raw, authors: "", year: "", id: "", link: "" };

  if (/^\d+$/.test(raw)) {
    // Already have a Source note for this book? Open it instead of making a duplicate.
    const existing = app.vault.getMarkdownFiles().find((f) => {
      const fm = app.metadataCache.getFileCache(f)?.frontmatter;
      return fm && fm.type === "source" && String(fm.calibre_id) === raw;
    });
    if (existing) {
      await app.workspace.getLeaf(false).openFile(existing);
      params.abort(`Source note already exists (${existing.basename}). Opened it.`);
    }

    const dir = LIBRARY_DIRS.find((d) => fs.existsSync(`${d}/metadata.db`));
    if (!dir) params.abort("Calibre library not found. Type a title instead.");

    const sql =
      "select b.title," +
      " coalesce((select group_concat(a.name, ' & ') from books_authors_link l" +
      " join authors a on a.id = l.author where l.book = b.id), '')," +
      " substr(b.pubdate, 1, 4)," +
      " coalesce((select group_concat(d.format) from data d where d.book = b.id), '')" +
      ` from books b where b.id = ${Number(raw)}`;

    let out = "";
    try {
      out = execFileSync(SQLITE, ["-readonly", "-separator", "\t", `${dir}/metadata.db`, sql], {
        encoding: "utf8",
        timeout: 5000,
      }).trim();
    } catch (e) {
      params.abort(`Calibre lookup failed: ${e.message}`);
    }
    if (!out) params.abort(`No Calibre book with id ${raw}.`);

    const [title, authors, year, formats] = out.split("\t");
    const fmts = (formats || "").split(",").filter(Boolean);
    const fmt = fmts.includes("EPUB") ? "EPUB" : fmts.includes("PDF") ? "PDF" : fmts[0];
    meta = {
      title,
      authors,
      year: /^\d{4}$/.test(year) && Number(year) > 1000 ? year : "",
      id: raw,
      link: fmt ? `calibre://view-book/${LIBRARY_NAME}/${raw}/${fmt}` : "",
    };
  }

  const citation = [
    meta.authors ? `${clean(meta.authors)},` : "",
    clean(meta.title),
    meta.year ? `(${meta.year})` : "",
    meta.id ? `- Calibre ${meta.id}` : "",
  ]
    .filter(Boolean)
    .join(" ")
    .replace(/, -/, " -");

  // Variables consumed by the "Source note (template)" choice.
  variables.title = fileSafe(meta.title); // becomes the file name: "Source - <title>"
  variables.citation = citation;
  variables.authors = clean(meta.authors);
  variables.year = meta.year;
  variables.calibre_id = meta.id;
  variables.calibre_link = meta.link;
};
