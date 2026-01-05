---
aliases: []
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2026-01-05T16:14:19+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
title: Custom RAG for Obsidian Notes
source: "https://gemini.google.com/share/7ab24d640ad0"
author:
  - "[[Gemini]]"
published:
created: 2026-01-05T15:58:44+00:00
description: "Created with Gemini"
tags:
  - "input"
---

I have a lot of markdown notes on an obsidian vault. I use a plugin called smart connections to embed them so I can get LLM to search semantically through the notes. Is there any advantage to crafting a custom LLM system that creates the vector dB of my notes? Can I improve the outcomes? I use Gemini cli on my notes and often search them semantically

Building a custom vector database for your Obsidian notes represents a shift from a **black-box plugin architecture** to a **modular Retrieval-Augmented Generation (RAG) pipeline**. While plugins like *Smart Connections* offer convenience, they often use generic chunking and retrieval logic that may not align with a high-density, conceptual note-taking style.

### Architectural Advantages of a Custom System

Developing your own system allows you to decouple the three core components of the RAG stack, enabling fine-grained optimisation at each layer:

- **Ingestion Logic (The "How"):** Plugins typically use fixed-size character or token chunking. A custom pipeline allows for **Semantic Chunking**, where breaks occur based on changes in meaning or heading structures, preserving the conceptual integrity of your notes.
- **Vector Engine Control:** You can select specific embedding models (e.g., `text-embedding-004` from Google) that are tuned for the technical or conceptual density of your specific vault.
- **Context Injection:** You can implement **Hybrid Search**, combining semantic vector results with traditional BM25 keyword matching to ensure that specific technical terms (which vectors sometimes "blur") are retrieved accurately.

---

### Improving Outcomes: Beyond Basic Vector Search

To significantly improve outcomes over a standard plugin, a custom system can implement advanced retrieval strategies:

| Strategy | Mechanism | Impact on Outcomes |
| --- | --- | --- |
| **Reranking** | Passing the top 20 vector results through a Cross-Encoder model. | Re-orders results based on actual relevance to the query, filtering out "semantically near but irrelevant" noise. |
| **HyDE (Hypothetical Document Embeddings)** | The LLM generates a "fake" answer first, then searches for notes similar to that answer. | Bridges the gap between a short query and a long, descriptive note. |
| **Metadata Filtering** | Injecting Obsidian YAML frontmatter (tags, dates, status) into the vector metadata. | Allows you to scope searches (e.g., "Search only within `#concept` and `#architecture` tags"). |
| **Recursive Retrieval** | Storing small chunks for search but returning the entire parent document to the LLM. | Provides the LLM with the full context of a concept rather than a fragmented snippet. |

---

### Why Move to a Custom CLI/Python Stack?

As a "software architect" of your own knowledge, the primary advantage is **observability**.

1. **Context Window Management:** With Gemini’s massive context window, a custom script can retrieve far more related notes than a plugin sidebar, allowing the LLM to synthesise connections across dozens of files simultaneously.
2. **Graph-Aware Retrieval:** You can programmatically follow `[[wikilinks]]`. If a retrieved note is a high-level concept, your script can automatically pull in all linked "implementation detail" notes before passing them to the Gemini CLI.
3. **Prompt Engineering:** You can bypass the plugin's hidden system prompt and define your own, ensuring the LLM maintains your preferred abstract-conceptual tone and avoids "flowery" filler.

### Recommended Workflow for Your Style

Instead of a full database, consider a **"Long-Context RAG"** approach:

1. Use a Python script to index your vault into a local **ChromaDB** or **LanceDB** instance.
2. Use a **Reranker** (like BGE-Reranker) to refine results.
3. Pipe the aggregated markdown content directly into the Gemini CLI with a system instruction that enforces "concept density" and "logical structure."

Would you like me to provide a Python boilerplate for a basic semantic search script using Gemini embeddings and a local vector store?

---

[Obsidian RAG: Private AI or Cloud Power (Complete Setup Guide)](https://www.youtube.com/watch?v=e_CCEAiGJpA) This video provides a practical walkthrough of setting up a RAG system within Obsidian, illustrating the difference between simple local embeddings and more powerful cloud-integrated retrieval methods.

i also have calibre library of epub and pdf books. It would be ideal to build a modular Retrieval-Augmented Generation (RAG) pipeline of all the content in those books. I could do semantic search over all the content and fin relevant info. How could i do this

Building a modular RAG pipeline for a Calibre library shifts the task from "searching notes" to "querying a structured knowledge base." For long-form content like epubs and PDFs, a standard semantic search often fails because the "concept density" is spread across hundreds of pages.

To improve outcomes, you must move from **flat indexing** to a **hierarchical, metadata-enriched architecture**.

### The Modular RAG Architecture

A robust pipeline for a Calibre library consists of four discrete layers:

---

### 1\. The Ingestion Layer: Calibre Decoupling

You should not interact with the ebook files directly. Instead, use Calibre’s CLI to extract both content and context.

- **Metadata Extraction:** Use `calibredb list` to pull the `metadata.db` info (Author, Series, Tags, ISBN). This metadata will be injected into every vector to allow for scoped queries (e.g., "Search only in books by \[Author\]").
- **Format Normalisation:** Convert EPUB/PDF to **Markdown** using Calibre’s `ebook-convert` or a high-fidelity tool like **Marker**. Markdown is the "gold standard" for RAG because it preserves structural hierarchy (`#`, `##`) which informs the chunking logic.

### 2\. The Processing Layer: Structural Chunking

In a book, 500-token fixed chunks are often meaningless. You need **Structural-Semantic Chunking**:

- **Chapter-Aware Splits:** Split the Markdown by H1 or H2 headers. This ensures a chunk doesn't bridge two unrelated chapters.
- **Parent-Child Indexing:** \* **Child Chunks:** Small, dense snippets (~256 tokens) used for the initial semantic match.
	- **Parent Chunks:** The full chapter or section. When a "Child" is found, the "Parent" is what gets sent to Gemini. This provides the LLM with the full "conceptual environment" of the book.

### 3\. The Retrieval Layer: Hybrid & Scoped Search

Standard semantic search often hallucinates proximity. A modular system allows for **Hybrid Retrieval**:

- **Vector Search:** For "vibes" and broad concepts (e.g., "theories on systems thinking").
- **Keyword (BM25) Search:** For specific technical terms or names that embeddings might "smooth over."
- **Metadata Filtering:** Before the search, you can programmatically filter the vector DB based on your Calibre tags.

	> **Example Query:** "Search for 'asymmetric encryption' but only in books tagged with '#cryptography' or '#security'."

### 4\. The Generation Layer: Long-Context Synthesis

Since you use the Gemini CLI, you can take advantage of its massive context window. A custom pipeline can retrieve the top 5 chapters across 3 different books and pass all of them to Gemini.

- **System Prompting:** Define a prompt that instructs the LLM to synthesise information across different authors, looking for contradictions or consensus—something a basic Obsidian plugin cannot do effectively.

---

### Implementation Strategy

### Why This Improves Outcomes

1. **Reduced Noise:** By chunking based on book structure, you avoid retrieving "half-ideas" that start at the end of one page and finish on another.
2. **Referential Integrity:** You can force the LLM to cite the *exact* book and chapter, creating a "traceable" knowledge system.
3. **Cross-Pollination:** You can query your Obsidian notes and your Calibre library simultaneously by using a unified vector space.

Would you like a Python blueprint for a script that uses `calibredb` to auto-index new additions to your library into a vector store?

i have struggle converting my epub to markdown. It always retains lots of epub markup. how do i use marker that you mentioned above?

The struggle with `epub-convert` or standard libraries is that they often treat the EPUB as a raw HTML dump, preserving CSS classes, span tags, and fragmented `<div>` structures that clutter the LLM's context.

**Marker** (developed by VikParuchuri) is a high-accuracy document-to-markdown converter that uses a series of deep learning models to strip away noise while preserving logical structure. It is particularly effective because it handles OCR, table detection, and formula conversion, which are common pain points in EPUB and PDF workflows.

### 1\. Architectural Setup

Marker is more resource-intensive than a simple Python script because it runs layout segmenters and OCR models. It is best used as a **preprocessing batch job** for your Calibre library.

#### Installation

You will need a Python environment (3.9+) and, ideally, a GPU for speed (though CPU works for smaller libraries).

Bash

```markdown
pip install marker-pdf
```

### 2\. The Conversion Logic: From EPUB/PDF to Clean MD

Marker excels at identifying "logical blocks." Unlike generic converters, it detects headers, lists, and tables and outputs clean, standard Markdown.

**To convert a single file:**

Bash

```markdown
marker_single /path/to/book.epub /output/folder --languages English
```

**To batch convert your entire Calibre Library:**You can point Marker at your Calibre folder. It will traverse the subdirectories, convert the files, and save the `.md` outputs.

Bash

```markdown
marker /path/to/Calibre_Library /output/markdown_vault --languages English --max_pages 500
```

---

### 3\. Cleaning the "Noise": Post-Marker Processing

Even with Marker, EPUBs can contain "artefacts" like page numbers, headers/footers, or publisher metadata. To ensure **high concept density** for your RAG system, I recommend a simple Python post-processing script to "sanitise" the output before it hits your vector database.

**The "Architectural" approach to cleaning:**

1. **Regex Stripping:** Remove CSS-like patterns (e.g., `{.class-name}`) that sometimes linger.
2. **Breadcrumb Injection:** Prepend the book Title and Author (from Calibre metadata) to the top of every Markdown file. This ensures that when a "chunk" is retrieved later, the LLM knows exactly which book it came from.
3. **Frontmatter Synthesis:** Convert Calibre’s `metadata.db` info into Obsidian-style YAML frontmatter.

---

### 4\. Integration Strategy for Your RAG Pipeline

Once Marker has generated clean Markdown files, you should structure them for your vector database as follows:

### Why Marker is Superior for your Top-Down Style

Standard EPUB converters produce **"noisy text"** which lowers the signal-to-noise ratio in your embeddings. Marker focuses on **structural recovery**. When your vector database searches through "structured" Markdown (where headers are clearly defined), the semantic "distance" between related concepts becomes much clearer, leading to significantly better synthesis from the Gemini CLI.

Would you like a Python script that bridges the gap—extracting the file path from your `metadata.db` and passing it to Marker for automated processing?

~/.local/share/chezmoi$ pip install marker-pdf

error: externally-managed-environment

× This environment is externally managed

╰─> To install Python packages system-wide, try apt install

python3-xyz, where xyz is the package you are trying to

install.

If you wish to install a non-Debian-packaged Python package,

create a virtual environment using python3 -m venv path/to/venv.

Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make

sure you have python3-full installed.

If you wish to install a non-Debian packaged Python application,

it may be easiest to use pipx install xyz, which will manage a

virtual environment for you. Make sure you have pipx installed.

See /usr/share/doc/python3.12/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.

hint: See PEP 668 for the detailed specification.

The error you are encountering is due to **PEP 668**, which prevents `pip` from installing packages globally to avoid breaking the system's package manager (like `apt`). Since you are building a modular pipeline, the architecturally sound approach is to isolate **Marker** in its own environment.

For your specific use case, **`pipx`** is the most efficient solution. It installs the application in an isolated environment but adds the binary to your global path, allowing you to run `marker_single` from anywhere without manually activating a virtual environment.

### 1\. The Immediate Fix: Using pipx

If you don't have `pipx` installed, get it first:

Bash

```markdown
sudo apt update
sudo apt install pipx
pipx ensurepath
```

*Note: You may need to restart your terminal after `ensurepath`.*

Then, install **Marker**:

Bash

```markdown
pipx install marker-pdf
```

### 2\. Implementation: The Pipeline Logic

Once installed via `pipx`, you can invoke the CLI directly. Given your Top-Down style, here is the logic for a clean conversion process that avoids the "metadata noise" you previously struggled with.

#### The "Clean" Conversion Command

Run this to convert an EPUB into a structured Markdown directory:

Bash

```markdown
marker_single /path/to/your/book.epub /output/folder --languages English
```

### 3\. Improving Outcomes: The Post-Conversion "Sanitiser"

Marker is excellent, but to truly optimise for a Vector DB/Gemini CLI workflow, you should run a simple Python script over the output. This script should perform two architectural tasks:

1. **Inject Context:** Prepend the book's Title and Author to the Markdown file.
2. **Strip Artefacts:** Remove any remaining CSS-like identifiers or page number strings.

#### Minimalist Sanitisation Script

### 4\. Integration with Calibre

Since you are already using `calibredb`, you can automate the discovery phase. A high-level framework for your custom pipeline would look like this:

1. **Extract:** Query `calibredb` for the file path of a specific book.
2. **Convert:** Pass that path to `marker_single`.
3. **Sanitise:** Run the script above to ensure **concept density**.
4. **Embed:** Load the clean Markdown into your vector store (e.g., LanceDB).

### Next Step

Would you like me to provide a **LlamaIndex** -based Python script that takes these "cleaned" Markdown files and indexes them into a vector store for your semantic searches?

/.local/share/chezmoi$ sudo apt update

sudo apt install pipx

pipx ensurepath

Hit:1 http://gb.archive.ubuntu.com/ubuntu noble InRelease

Hit:2 http://gb.archive.ubuntu.com/ubuntu noble-updates InRelease

Hit:3 http://gb.archive.ubuntu.com/ubuntu noble-backports InRelease

Hit:4 http://security.ubuntu.com/ubuntu noble-security InRelease

Get:5 https://apt.releases.hashicorp.com noble InRelease \[12.9 kB\]

Hit:6 https://ppa.launchpadcontent.net/neovim-ppa/unstable/ubuntu noble InRelease

Hit:7 https://dl.google.com/linux/chrome/deb stable InRelease

Fetched 12.9 kB in 1s (23.6 kB/s)

Reading package lists... Done

Building dependency tree... Done

Reading state information... Done

2 packages can be upgraded. Run 'apt list --upgradable' to see them.

Reading package lists... Done

Building dependency tree... Done

Reading state information... Done

The following additional packages will be installed:

python3-argcomplete python3-pip-whl python3-platformdirs python3-psutil python3-setuptools-whl python3-userpath python3-venv python3.12-venv

The following NEW packages will be installed

pipx python3-argcomplete python3-pip-whl python3-platformdirs python3-psutil python3-setuptools-whl python3-userpath python3-venv python3.12-venv

0 to upgrade, 9 to newly install, 0 to remove and 2 not to upgrade.

Need to get 3,471 kB of archives.

After this operation, 7,648 kB of additional disk space will be used.

Do you want to continue? \[Y/n\]

Get:1 http://gb.archive.ubuntu.com/ubuntu noble-updates/universe amd64 python3-pip-whl all 24.0+dfsg-1ubuntu1.3 \[1,707 kB\]

Get:2 http://gb.archive.ubuntu.com/ubuntu noble-updates/universe amd64 python3-setuptools-whl all 68.1.2-2ubuntu1.2 \[716 kB\]

Get:3 http://gb.archive.ubuntu.com/ubuntu noble-updates/universe amd64 python3.12-venv amd64 3.12.3-1ubuntu0.9 \[5,674 B\]

Get:4 http://gb.archive.ubuntu.com/ubuntu noble-updates/universe amd64 python3-venv amd64 3.12.3-0ubuntu2.1 \[1,032 B\]

Get:5 http://gb.archive.ubuntu.com/ubuntu noble-updates/universe amd64 python3-argcomplete all 3.1.4-1ubuntu0.1 \[33.8 kB\]

Get:6 http://gb.archive.ubuntu.com/ubuntu noble/main amd64 python3-platformdirs all 4.2.0-1 \[16.1 kB\]

Get:7 http://gb.archive.ubuntu.com/ubuntu noble/universe amd64 python3-userpath all 1.9.1-1 \[9,416 B\]

Get:8 http://gb.archive.ubuntu.com/ubuntu noble/universe amd64 pipx all 1.4.3-1 \[787 kB\]

Get:9 http://gb.archive.ubuntu.com/ubuntu noble/main amd64 python3-psutil amd64 5.9.8-2build2 \[195 kB\]

Fetched 3,471 kB in 0s (14.2 MB/s)

Selecting previously unselected package python3-pip-whl.

(Reading database... 225551 files and directories currently installed.)

Preparing to unpack.../0-python3-pip-whl\_24.0+dfsg-1ubuntu1.3\_all.deb...

Unpacking python3-pip-whl (24.0+dfsg-1ubuntu1.3)...

Selecting previously unselected package python3-setuptools-whl.

Preparing to unpack.../1-python3-setuptools-whl\_68.1.2-2ubuntu1.2\_all.deb...

Unpacking python3-setuptools-whl (68.1.2-2ubuntu1.2)...

Selecting previously unselected package python3.12-venv.

Preparing to unpack.../2-python3.12-venv\_3.12.3-1ubuntu0.9\_amd64.deb...

Unpacking python3.12-venv (3.12.3-1ubuntu0.9)...

Selecting previously unselected package python3-venv.

Preparing to unpack.../3-python3-venv\_3.12.3-0ubuntu2.1\_amd64.deb...

Unpacking python3-venv (3.12.3-0ubuntu2.1)...

Selecting previously unselected package python3-argcomplete.

Preparing to unpack.../4-python3-argcomplete\_3.1.4-1ubuntu0.1\_all.deb...

Unpacking python3-argcomplete (3.1.4-1ubuntu0.1)...

Selecting previously unselected package python3-platformdirs.

Preparing to unpack.../5-python3-platformdirs\_4.2.0-1\_all.deb...

Unpacking python3-platformdirs (4.2.0-1)...

Selecting previously unselected package python3-userpath.

Preparing to unpack.../6-python3-userpath\_1.9.1-1\_all.deb...

Unpacking python3-userpath (1.9.1-1)...

Selecting previously unselected package pipx.

Preparing to unpack.../7-pipx\_1.4.3-1\_all.deb...

Unpacking pipx (1.4.3-1)...

Selecting previously unselected package python3-psutil.

Preparing to unpack.../8-python3-psutil\_5.9.8-2build2\_amd64.deb...

Unpacking python3-psutil (5.9.8-2build2)...

Setting up python3-setuptools-whl (68.1.2-2ubuntu1.2)...

Setting up python3-pip-whl (24.0+dfsg-1ubuntu1.3)...

Setting up python3-platformdirs (4.2.0-1)...

Setting up python3-psutil (5.9.8-2build2)...

Setting up python3-argcomplete (3.1.4-1ubuntu0.1)...

Setting up python3-userpath (1.9.1-1)...

Setting up python3.12-venv (3.12.3-1ubuntu0.9)...

Setting up python3-venv (3.12.3-0ubuntu2.1)...

Setting up pipx (1.4.3-1)...

Processing triggers for man-db (2.12.0-4build2)...

/home/leon/.local/bin is already in PATH.

⚠️ All pipx binary directories have been added to PATH. If you are sure you want to proceed, try again with the '--force' flag.

Since you have successfully configured `pipx`, you can now install **Marker** in an isolated environment. This ensures that its complex dependencies (like PyTorch and Surya OCR) do not conflict with your system-level Python or other tools.

### 1\. Finalise Marker Installation

Execute the following to install the core package. If you intend to process a variety of complex document types beyond standard PDFs, I recommend the `[full]` version which includes additional OCR and layout engines.

Bash

```markdown
pipx install "marker-pdf[full]"
```

*Note: This may take a few minutes as it downloads several large machine learning models (approx. 2-3GB) required for high-fidelity structural analysis.*

---

### 2\. High-Fidelity Conversion Framework

Marker is architecturally superior for your Top-Down style because it uses **vision-based layout analysis** rather than basic text extraction. It identifies headers, tables, and lists as discrete logical blocks, preventing the "markup soup" common in standard EPUB-to-Markdown conversions.

#### Single File Execution

To convert a specific book from your Calibre library:

Bash

```markdown
marker_single /path/to/calibre/book.epub /output/path/ --languages English
```

#### Batch Processing for Calibre

To process your entire library, use the `marker` command. This will traverse your Calibre directory structure and output a mirrored directory of clean Markdown files:

Bash

```markdown
marker /path/to/Calibre_Library /your/rag_vault/ --languages English
```

---

### 3\. Integrating with your RAG Pipeline

To maximise **concept density** for the Gemini CLI, your custom system should follow this structural logic once Marker has finished the conversion:

1. **Metadata Injection:** Marker creates a `.json` metadata file for each conversion. Your script should read this (and your Calibre `metadata.db`) to inject YAML frontmatter into the Markdown. This allows your LLM to "know" the source context during semantic search.
2. **Chunking by Header:** Since Marker preserves headers (`#`, `##`), you should use a **Header-Based Splitter**. This ensures that the logical units defined by the author remain intact, rather than being sliced at arbitrary token counts.
3. **The "Long-Context" Advantage:** Using Gemini 1.5 or 2.0 via CLI allows you to pass significantly larger chunks (entire chapters) than the Obsidian *Smart Connections* plugin typically allows. This results in more coherent, architecturally sound responses.

---

### Suggested High-Level Logic for your Automation

Python

```markdown
# Conceptual logic for a Calibre-to-RAG bridge
def process_library(calibre_path, vault_path):
    # 1. Discover new files in Calibre
    # 2. Run 'marker' CLI on the directory
    # 3. Post-process: Add Calibre tags to Markdown YAML
    # 4. Upsert to Vector DB (e.g., LanceDB or Chroma)
    pass
```

Would you like me to provide a Python script that specifically interacts with the **Calibre SQLite database** (`metadata.db`) to automate the batch conversion of only your most recently added books?

---

[High Fidelity Document Parsing](https://www.youtube.com/watch?v=ROqpVzEzRIQ) This video demonstrates the local installation and performance of Marker, showing how it successfully handles complex document layouts that standard tools often fail to parse correctly.

marker\_single Making\_Habits\_\_Breaking\_Habits\_\_How\_to\_Mak\_-\_Jeremy\_Dean.epub./ --languages English

Usage: marker\_single \[OPTIONS\] FPATH

Try 'marker\_single --help' for help.

Error: No such option: --languages

leon@leon-XPS-13-9360:~/Downloads$ marker\_single --help

Usage: marker\_single \[OPTIONS\] FPATH

Convert a single PDF to markdown.

Options:

\--llm\_service TEXT LLM service to use - should be full import

path, like

marker.services.gemini.GoogleGeminiService

\--converter\_cls TEXT Converter class to use. Defaults to PDF

converter.

\--page\_range TEXT Page range to convert, specify comma

separated page numbers or ranges. Example:

0,5-10,20

\--disable\_image\_extraction Disable image extraction.

\--disable\_multiprocessing Disable multiprocessing.

\--config\_json TEXT Path to JSON file with additional

configuration.

\--processors TEXT Comma separated list of processors to use.

Must use full module path.

\--output\_format \[markdown|json|html|chunks\]

Format to output results in.

\-d, --debug Enable debug mode.

\--output\_dir PATH Directory to save output.

\--lowres\_image\_dpi INTEGER DPI setting for low-resolution page images

used for Layout and Line Detection. Default

is 96. (Applies to: DocumentBuilder)

\--highres\_image\_dpi INTEGER DPI setting for high-resolution page images

used for OCR. Default is 192. (Applies to:

DocumentBuilder)

\--disable\_ocr Disable OCR processing. Default is False.

(Applies to: DocumentBuilder, LineBuilder,

TableProcessor)

\--layout\_batch\_size INTEGER The batch size to use for the layout model.

Default is None, which will use the default

batch size for the model. (Applies to:

LayoutBuilder)

\--force\_layout\_block TEXT Skip layout and force every page to be

treated as a specific block type. Default is

None. (Applies to: LayoutBuilder)

\--disable\_tqdm Disable tqdm progress bars. Default is

False. (Applies to: LayoutBuilder,

LineBuilder, OcrBuilder, EquationProcessor,

LLMComplexRegionProcessor,

LLMEquationProcessor, LLMFormProcessor,

LLMHandwritingProcessor,

LLMImageDescriptionProcessor,

LLMMathBlockProcessor,

LLMSimpleBlockMetaProcessor,

LLMPageCorrectionProcessor,

LLMSectionHeaderProcessor,

LLMTableProcessor, LLMTableMergeProcessor,

TableProcessor, DocumentExtractor,

PageExtractor)

\--max\_expand\_frac FLOAT The maximum fraction to expand the layout

box bounds by Default is 0.05. (Applies to:

LayoutBuilder)

\--detection\_batch\_size INTEGER The batch size to use for the detection

model. Default is None, which will use the

default batch size for the model. (Applies

to: LineBuilder, TableProcessor)

\--ocr\_error\_batch\_size INTEGER The batch size to use for the ocr error

detection model. Default is None, which will

use the default batch size for the model.

(Applies to: LineBuilder)

\--layout\_coverage\_min\_lines INTEGER

The minimum number of PdfProvider lines that

must be covered by the layout model to

consider the lines from the PdfProvider

valid. Default is 1. (Applies to:

LineBuilder)

\--layout\_coverage\_threshold FLOAT

The minimum coverage ratio required for the

layout model to consider the lines from the

PdfProvider valid. Default is 0.25. (Applies

to: LineBuilder)

\--min\_document\_ocr\_threshold FLOAT

If less pages than this threshold are good,

OCR will happen in the document. Otherwise

it will not. Default is 0.85. (Applies to:

LineBuilder)

\--provider\_line\_provider\_line\_min\_overlap\_pct FLOAT

The percentage of a provider line that has

to be covered by a detected line Default is

0.1. (Applies to: LineBuilder)

\--keep\_chars Keep individual characters. Default is

False. (Applies to: LineBuilder, OcrBuilder,

DocumentProvider, PdfProvider, EpubProvider,

HTMLProvider, PowerPointProvider,

SpreadSheetProvider)

\--detection\_line\_min\_confidence FLOAT

Minimum confidence for a detected line to be

included Default is 0.8. (Applies to:

LineBuilder)

\--recognition\_batch\_size INTEGER

The batch size to use for the recognition

model. Default is None, which will use the

default batch size for the model. (Applies

to: OcrBuilder, TableProcessor)

\--ocr\_task\_name TEXT The OCR mode to use, see surya for details.

Set to 'ocr\_without\_boxes' for potentially

better performance, at the expense of

formatting. Default is ocr\_with\_boxes.

(Applies to: OcrBuilder)

\--disable\_ocr\_math Disable inline math recognition in OCR

Default is False. (Applies to: OcrBuilder,

TableProcessor)

\--drop\_repeated\_text Drop repeated text in OCR results. Default

is False. (Applies to: OcrBuilder,

EquationProcessor)

\--block\_mode\_intersection\_thresh FLOAT

Max intersection before falling back to line

mode Default is 0.5. (Applies to:

OcrBuilder)

\--block\_mode\_max\_lines INTEGER Max lines within a block before falling back

to line mode Default is 15. (Applies to:

OcrBuilder)

\--block\_mode\_max\_height\_frac FLOAT

Max height of a block as a percentage of the

page before falling back to line mode

Default is 0.5. (Applies to: OcrBuilder)

\--gap\_threshold FLOAT The minimum gap between blocks to consider

them part of the same group. Default is

0.05. (Applies to: StructureBuilder)

\--list\_gap\_threshold FLOAT The minimum gap between list items to

consider them part of the same group.

Default is 0.1. (Applies to:

StructureBuilder)

\--full\_page\_block\_intersection\_threshold FLOAT

Threshold to detect blank pages at Default

is 0.8. (Applies to: BlankPageProcessor)

\--filter\_blank\_pages Remove blank pages detected as images.

Default is False. (Applies to:

BlankPageProcessor)

\--block\_relabel\_str TEXT Comma-separated relabeling rules in the

format '<original\_label>:<new\_label>:<confid

ence\_threshold>'. Each rule defines how

blocks of a certain type should be relabeled

when the confidence exceeds the threshold.

Example:

'Table:Picture:0.85,Form:Picture:0.9'

Default is. (Applies to:

BlockRelabelProcessor)

\--min\_x\_indent FLOAT The minimum horizontal indentation required

to consider a block as part of a blockquote.

Expressed as a percentage of the block

width. Default is 0.1. (Applies to:

BlockquoteProcessor, ListProcessor)

\--x\_start\_tolerance FLOAT The maximum allowable difference between the

starting x-coordinates of consecutive blocks

to consider them aligned. Expressed as a

percentage of the block width. Default is

0.01. (Applies to: BlockquoteProcessor)

\--x\_end\_tolerance FLOAT The maximum allowable difference between the

ending x-coordinates of consecutive blocks

to consider them aligned. Expressed as a

percentage of the block width. Default is

0.01. (Applies to: BlockquoteProcessor)

\--debug\_data\_folder TEXT The folder to dump debug data to. Default is

debug\_data. (Applies to: DebugProcessor)

\--debug\_layout\_images Whether to dump layout debug images. Default

is False. (Applies to: DebugProcessor)

\--debug\_pdf\_images Whether to dump PDF debug images. Default is

False. (Applies to: DebugProcessor)

\--debug\_json Whether to dump block debug data. Default is

False. (Applies to: DebugProcessor)

\--model\_max\_length INTEGER The maximum number of tokens to allow for

the Recognition model. Default is 1024.

(Applies to: EquationProcessor)

\--equation\_batch\_size INTEGER The batch size to use for the recognition

model while processing equations. Default is

None, which will use the default batch size

for the model. (Applies to:

EquationProcessor)

\--common\_element\_threshold FLOAT

The minimum ratio of pages a text block must

appear on to be considered a common element.

Blocks that meet or exceed this threshold

are marked as common elements. Default is

0.2. (Applies to: IgnoreTextProcessor)

\--common\_element\_min\_blocks INTEGER

The minimum number of occurrences of a text

block within a document to consider it a

common element. This ensures that rare

blocks are not mistakenly flagged. Default

is 3. (Applies to: IgnoreTextProcessor)

\--max\_streak INTEGER The maximum number of consecutive

occurrences of a text block allowed before

it is classified as a common element. Helps

to identify patterns like repeated headers

or footers. Default is 3. (Applies to:

IgnoreTextProcessor)

\--text\_match\_threshold INTEGER The minimum fuzzy match score (0-100)

required to classify a text block as similar

to a common element. Higher values enforce

stricter matching. Default is 90. (Applies

to: IgnoreTextProcessor)

\--min\_merge\_pct FLOAT The minimum percentage of intersection area

to consider merging. Default is 0.015.

(Applies to: LineMergeProcessor)

\--block\_expand\_threshold FLOAT The percentage of the block width to expand

the bounding box. Default is 0.05. (Applies

to: LineMergeProcessor)

\--min\_merge\_ydist FLOAT The minimum y distance between lines to

consider merging. Default is 5. (Applies to:

LineMergeProcessor)

\--intersection\_pct\_threshold FLOAT

The total amount of intersection area

concentrated in the max intersection block.

Default is 0.5. (Applies to:

LineMergeProcessor)

\--vertical\_overlap\_pct\_threshold FLOAT

The minimum percentage of vertical overlap

to consider merging. Default is 0.8.

(Applies to: LineMergeProcessor)

\--use\_llm Whether to use LLMs to improve accuracy.

Default is False. (Applies to:

LineMergeProcessor,

LLMComplexRegionProcessor,

LLMEquationProcessor, LLMFormProcessor,

LLMHandwritingProcessor,

LLMImageDescriptionProcessor,

LLMMathBlockProcessor,

LLMSimpleBlockMetaProcessor,

LLMPageCorrectionProcessor,

LLMSectionHeaderProcessor,

LLMTableProcessor, LLMTableMergeProcessor,

ExtractionConverter, PdfConverter,

OCRConverter, TableConverter)

\--strip\_numbers\_threshold FLOAT

The fraction of lines or tokens in a block

that must be numeric to consider them as

line numbers. Default is 0.6. (Applies to:

LineNumbersProcessor)

\--min\_lines\_in\_block INTEGER The minimum number of lines required in a

block for it to be considered during

processing. Ensures that small blocks are

ignored as they are unlikely to contain

meaningful line numbers. Default is 4.

(Applies to: LineNumbersProcessor)

\--min\_line\_length INTEGER The minimum length of a line (in characters)

to consider it significant when checking for

numeric prefixes or suffixes. Prevents false

positives for short lines. Default is 10.

(Applies to: LineNumbersProcessor)

\--min\_line\_number\_span\_ratio FLOAT

The minimum ratio of detected line number

spans to total lines required to treat them

as line numbers. Default is 0.6. (Applies

to: LineNumbersProcessor)

\--max\_concurrency INTEGER The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

(Applies to: LLMComplexRegionProcessor,

LLMEquationProcessor, LLMFormProcessor,

LLMHandwritingProcessor,

LLMImageDescriptionProcessor,

LLMMathBlockProcessor,

LLMSimpleBlockMetaProcessor,

LLMPageCorrectionProcessor,

LLMSectionHeaderProcessor,

LLMTableProcessor, LLMTableMergeProcessor,

DocumentExtractor, PageExtractor)

\--image\_expansion\_ratio FLOAT The ratio to expand the image by when

cropping. Default is 0.01. (Applies to:

LLMComplexRegionProcessor,

LLMEquationProcessor, LLMFormProcessor,

LLMHandwritingProcessor,

LLMImageDescriptionProcessor,

LLMMathBlockProcessor,

LLMSimpleBlockMetaProcessor,

LLMPageCorrectionProcessor,

LLMSectionHeaderProcessor,

LLMTableProcessor, LLMTableMergeProcessor)

\--min\_equation\_height FLOAT The minimum ratio between equation height

and page height to consider for processing.

Default is 0.06. (Applies to:

LLMEquationProcessor)

\--redo\_inline\_math Whether to redo inline math blocks. Default

is False. (Applies to: LLMEquationProcessor,

LLMMathBlockProcessor)

\--equation\_latex\_prompt TEXT The prompt to use for generating LaTeX from

equations. Default is a string containing

the Gemini prompt. (Applies to:

LLMEquationProcessor)

\--handwriting\_generation\_prompt TEXT

The prompt to use for OCRing handwriting.

Default is a string containing the Gemini

prompt. (Applies to:

LLMHandwritingProcessor)

\--extract\_images BOOLEAN Extract images from the document. Default is

True. (Applies to:

LLMImageDescriptionProcessor, ChunkRenderer,

JSONRenderer, ExtractionRenderer,

HTMLRenderer, MarkdownRenderer,

OCRJSONRenderer)

\--image\_description\_prompt TEXT

The prompt to use for generating image

descriptions. Default is a string containing

the Gemini prompt. (Applies to:

LLMImageDescriptionProcessor)

\--inlinemath\_min\_ratio FLOAT If more than this ratio of blocks are

inlinemath blocks, assume everything has

math. Default is 0.4. (Applies to:

LLMMathBlockProcessor)

\--block\_correction\_prompt TEXT The user prompt to guide the block

correction process. Default is None.

(Applies to: LLMPageCorrectionProcessor)

\--max\_rows\_per\_batch INTEGER If the table has more rows than this, chunk

the table. (LLMs can be inaccurate with a

lot of rows) Default is 60. (Applies to:

LLMTableProcessor)

\--max\_table\_rows INTEGER The maximum number of rows in a table to

process with the LLM processor. Beyond this

will be skipped. Default is 175. (Applies

to: LLMTableProcessor)

\--table\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0. (Applies to:

LLMTableProcessor)

\--rotation\_max\_wh\_ratio FLOAT The maximum width/height ratio for table

cells for a table to be considered rotated.

Default is 0.6. (Applies to:

LLMTableProcessor)

\--max\_table\_iterations INTEGER The maximum number of iterations to attempt

rewriting a table. Default is 2. (Applies

to: LLMTableProcessor)

\--table\_rewriting\_prompt TEXT The prompt to use for rewriting text.

Default is a string containing the Gemini

rewriting prompt. (Applies to:

LLMTableProcessor)

\--table\_height\_threshold FLOAT The minimum height ratio relative to the

page for the first table in a pair to be

considered for merging. Default is 0.6.

(Applies to: LLMTableMergeProcessor)

\--table\_start\_threshold FLOAT The maximum percentage down the page the

second table can start to be considered for

merging. Default is 0.2. (Applies to:

LLMTableMergeProcessor)

\--vertical\_table\_height\_threshold FLOAT

The height tolerance for 2 adjacent tables

to be merged into one. Default is 0.25.

(Applies to: LLMTableMergeProcessor)

\--vertical\_table\_distance\_threshold INTEGER

The maximum distance between table edges for

adjacency. Default is 20. (Applies to:

LLMTableMergeProcessor)

\--horizontal\_table\_width\_threshold FLOAT

The width tolerance for 2 adjacent tables to

be merged into one. Default is 0.25.

(Applies to: LLMTableMergeProcessor)

\--horizontal\_table\_distance\_threshold INTEGER

The maximum distance between table edges for

adjacency. Default is 10. (Applies to:

LLMTableMergeProcessor)

\--column\_gap\_threshold INTEGER The maximum gap between columns to merge

tables Default is 50. (Applies to:

LLMTableMergeProcessor)

\--no\_merge\_tables\_across\_pages Whether to disable merging tables across

pages and keep page delimiters. Default is

False. (Applies to: LLMTableMergeProcessor)

\--table\_merge\_prompt TEXT The prompt to use for rewriting text.

Default is a string containing the Gemini

rewriting prompt. (Applies to:

LLMTableMergeProcessor)

\--level\_count INTEGER The number of levels to use for headings.

Default is 4. (Applies to:

SectionHeaderProcessor)

\--merge\_threshold FLOAT The minimum gap between headings to consider

them part of the same group. Default is

0.25. (Applies to: SectionHeaderProcessor)

\--default\_level INTEGER The default heading level to use if no

heading level is detected. Default is 2.

(Applies to: SectionHeaderProcessor)

\--height\_tolerance FLOAT The minimum height of a heading to consider

it a heading. Default is 0.99. (Applies to:

SectionHeaderProcessor)

\--table\_rec\_batch\_size INTEGER The batch size to use for the table

recognition model. Default is None, which

will use the default batch size for the

model. (Applies to: TableProcessor)

\--row\_split\_threshold FLOAT The percentage of rows that need to be split

across the table before row splitting is

active. Default is 0.5. (Applies to:

TableProcessor)

\--pdftext\_workers INTEGER The number of workers to use for pdftext.

Default is 1. (Applies to: TableProcessor,

DocumentProvider, PdfProvider, EpubProvider,

HTMLProvider, PowerPointProvider,

SpreadSheetProvider)

\--drop\_repeated\_table\_text Drop repeated text in OCR results. Default

is False. (Applies to: TableProcessor)

\--column\_gap\_ratio FLOAT The minimum ratio of the page width to the

column gap to consider a column break.

Default is 0.02. (Applies to: TextProcessor)

\--pattern TEXT Default is {\\d+\\}-{48}\\n\\n. (Applies to:

ExtractionConverter)

\--existing\_markdown TEXT Markdown that was already converted for

extraction. Default is None. (Applies to:

ExtractionConverter)

\--flatten\_pdf BOOLEAN Whether to flatten the PDF structure.

Default is True. (Applies to:

DocumentProvider, PdfProvider, EpubProvider,

HTMLProvider, PowerPointProvider,

SpreadSheetProvider)

\--force\_ocr Whether to force OCR on the whole document.

Default is False. (Applies to:

DocumentProvider, PdfProvider, EpubProvider,

HTMLProvider, PowerPointProvider,

SpreadSheetProvider)

\--ocr\_space\_threshold FLOAT The minimum ratio of spaces to non-spaces to

detect bad text. Default is 0.7. (Applies

to: DocumentProvider, PdfProvider,

EpubProvider, HTMLProvider,

PowerPointProvider, SpreadSheetProvider)

\--ocr\_newline\_threshold FLOAT The minimum ratio of newlines to non-

newlines to detect bad text. Default is 0.6.

(Applies to: DocumentProvider, PdfProvider,

EpubProvider, HTMLProvider,

PowerPointProvider, SpreadSheetProvider)

\--ocr\_alphanum\_threshold FLOAT The minimum ratio of alphanumeric characters

to non-alphanumeric characters to consider

an alphanumeric character. Default is 0.3.

(Applies to: DocumentProvider, PdfProvider,

EpubProvider, HTMLProvider,

PowerPointProvider, SpreadSheetProvider)

\--image\_threshold FLOAT The minimum coverage ratio of the image to

the page to consider skipping the page.

Default is 0.65. (Applies to:

DocumentProvider, PdfProvider, EpubProvider,

HTMLProvider, PowerPointProvider,

SpreadSheetProvider)

\--strip\_existing\_ocr Whether to strip existing OCR text from the

PDF. Default is False. (Applies to:

DocumentProvider, PdfProvider, EpubProvider,

HTMLProvider, PowerPointProvider,

SpreadSheetProvider)

\--disable\_links Whether to disable links. Default is False.

(Applies to: DocumentProvider, PdfProvider,

EpubProvider, HTMLProvider,

PowerPointProvider, SpreadSheetProvider)

\--image\_count INTEGER Default is 1. (Applies to: ImageProvider)

\--include\_slide\_number Default is False. (Applies to:

PowerPointProvider)

\--keep\_pageheader\_in\_output Keep the page header in the output HTML.

Default is False. (Applies to:

ChunkRenderer, JSONRenderer,

ExtractionRenderer, HTMLRenderer,

MarkdownRenderer, OCRJSONRenderer)

\--keep\_pagefooter\_in\_output Keep the page footer in the output HTML.

Default is False. (Applies to:

ChunkRenderer, JSONRenderer,

ExtractionRenderer, HTMLRenderer,

MarkdownRenderer, OCRJSONRenderer)

\--add\_block\_ids Whether to add block IDs to the output HTML.

Default is False. (Applies to:

ChunkRenderer, JSONRenderer,

ExtractionRenderer, HTMLRenderer,

MarkdownRenderer, OCRJSONRenderer)

\--paginate\_output Whether to paginate the output. Default is

False. (Applies to: HTMLRenderer,

MarkdownRenderer)

\--page\_separator TEXT The separator to use between pages. Default

is '-' \* 48. (Applies to: MarkdownRenderer)

\--html\_tables\_in\_markdown Return tables formatted as HTML, instead of

in markdown Default is False. (Applies to:

MarkdownRenderer)

\--timeout INTEGER The timeout to use for the service. Default

is 30. (Applies to: AzureOpenAIService,

ClaudeService, GoogleGeminiService,

OllamaService, OpenAIService,

GoogleVertexService)

\--max\_retries INTEGER The maximum number of retries to use for the

service. Default is 2. (Applies to:

AzureOpenAIService, ClaudeService,

GoogleGeminiService, OllamaService,

OpenAIService, GoogleVertexService)

\--retry\_wait\_time INTEGER The wait time between retries. Default is 3.

(Applies to: AzureOpenAIService,

ClaudeService, GoogleGeminiService,

OllamaService, OpenAIService,

GoogleVertexService)

\--max\_output\_tokens INTEGER The maximum number of output tokens to

generate. Default is None. (Applies to:

AzureOpenAIService, ClaudeService,

GoogleGeminiService, OllamaService,

OpenAIService, GoogleVertexService)

\--azure\_endpoint TEXT The Azure OpenAI endpoint URL. No trailing

slash. Default is None. (Applies to:

AzureOpenAIService)

\--azure\_api\_key TEXT The API key to use for the Azure OpenAI

service. Default is None. (Applies to:

AzureOpenAIService)

\--azure\_api\_version TEXT The Azure OpenAI API version to use. Default

is None. (Applies to: AzureOpenAIService)

\--deployment\_name TEXT The deployment name for the Azure OpenAI

model. Default is None. (Applies to:

AzureOpenAIService)

\--claude\_model\_name TEXT The name of the Google model to use for the

service. Default is

claude-3-7-sonnet-20250219. (Applies to:

ClaudeService)

\--claude\_api\_key TEXT The Claude API key to use for the service.

Default is None. (Applies to: ClaudeService)

\--max\_claude\_tokens INTEGER The maximum number of tokens to use for a

single Claude request. Default is 8192.

(Applies to: ClaudeService)

\--gemini\_model\_name TEXT The name of the Google model to use for the

service. Default is gemini-2.0-flash.

(Applies to: GoogleGeminiService,

GoogleVertexService)

\--thinking\_budget INTEGER The thinking token budget to use for the

service. Default is None. (Applies to:

GoogleGeminiService, GoogleVertexService)

\--gemini\_api\_key TEXT The Google API key to use for the service.

Default is None. (Applies to:

GoogleGeminiService)

\--ollama\_base\_url TEXT The base url to use for ollama. No trailing

slash. Default is http://localhost:11434.

(Applies to: OllamaService)

\--ollama\_model TEXT The model name to use for ollama. Default is

llama3.2-vision. (Applies to: OllamaService)

\--openai\_base\_url TEXT The base url to use for OpenAI-like models.

No trailing slash. Default is

https://api.openai.com/v1. (Applies to:

OpenAIService)

\--openai\_model TEXT The model name to use for OpenAI-like model.

Default is gpt-4o-mini. (Applies to:

OpenAIService)

\--openai\_api\_key TEXT The API key to use for the OpenAI-like

service. Default is None. (Applies to:

OpenAIService)

\--openai\_image\_format TEXT The image format to use for the OpenAI-like

service. Use 'png' for better compatability

Default is webp. (Applies to: OpenAIService)

\--vertex\_project\_id TEXT Google Cloud Project ID for Vertex AI.

Default is None. (Applies to:

GoogleVertexService)

\--vertex\_location TEXT Google Cloud Location for Vertex AI. Default

is us-central1. (Applies to:

GoogleVertexService)

\--vertex\_dedicated Whether to use a dedicated Vertex AI

instance. Default is False. (Applies to:

GoogleVertexService)

\--page\_schema TEXT The JSON schema to be extracted from the

page. Default is. (Applies to:

DocumentExtractor, PageExtractor)

\--extraction\_page\_chunk\_size INTEGER

The number of pages to chunk together for

extraction. Default is 3. (Applies to:

PageExtractor)

\--DocumentBuilder\_lowres\_image\_dpi INTEGER

DPI setting for low-resolution page images

used for Layout and Line Detection. Default

is 96.

\--DocumentBuilder\_highres\_image\_dpi INTEGER

DPI setting for high-resolution page images

used for OCR. Default is 192.

\--DocumentBuilder\_disable\_ocr Disable OCR processing. Default is False.

\--LayoutBuilder\_layout\_batch\_size INTEGER

The batch size to use for the layout model.

Default is None, which will use the default

batch size for the model.

\--LayoutBuilder\_force\_layout\_block TEXT

Skip layout and force every page to be

treated as a specific block type. Default is

None.

\--LayoutBuilder\_disable\_tqdm Disable tqdm progress bars. Default is

False.

\--LayoutBuilder\_max\_expand\_frac FLOAT

The maximum fraction to expand the layout

box bounds by Default is 0.05.

\--LineBuilder\_detection\_batch\_size INTEGER

The batch size to use for the detection

model. Default is None, which will use the

default batch size for the model.

\--LineBuilder\_ocr\_error\_batch\_size INTEGER

The batch size to use for the ocr error

detection model. Default is None, which will

use the default batch size for the model.

\--LineBuilder\_layout\_coverage\_min\_lines INTEGER

The minimum number of PdfProvider lines that

must be covered by the layout model to

consider the lines from the PdfProvider

valid. Default is 1.

\--LineBuilder\_layout\_coverage\_threshold FLOAT

The minimum coverage ratio required for the

layout model to consider the lines from the

PdfProvider valid. Default is 0.25.

\--LineBuilder\_min\_document\_ocr\_threshold FLOAT

If less pages than this threshold are good,

OCR will happen in the document. Otherwise

it will not. Default is 0.85.

\--LineBuilder\_provider\_line\_provider\_line\_min\_overlap\_pct FLOAT

The percentage of a provider line that has

to be covered by a detected line Default is

0.1.

\--LineBuilder\_disable\_tqdm Disable tqdm progress bars. Default is

False.

\--LineBuilder\_disable\_ocr Disable OCR for the document. This will only

use the lines from the provider. Default is

False.

\--LineBuilder\_keep\_chars Keep individual characters. Default is

False.

\--LineBuilder\_detection\_line\_min\_confidence FLOAT

Minimum confidence for a detected line to be

included Default is 0.8.

\--OcrBuilder\_recognition\_batch\_size INTEGER

The batch size to use for the recognition

model. Default is None, which will use the

default batch size for the model.

\--OcrBuilder\_disable\_tqdm Disable tqdm progress bars. Default is

False.

\--OcrBuilder\_ocr\_task\_name TEXT

The OCR mode to use, see surya for details.

Set to 'ocr\_without\_boxes' for potentially

better performance, at the expense of

formatting. Default is ocr\_with\_boxes.

\--OcrBuilder\_keep\_chars Keep individual characters. Default is

False.

\--OcrBuilder\_disable\_ocr\_math Disable inline math recognition in OCR

Default is False.

\--OcrBuilder\_drop\_repeated\_text

Drop repeated text in OCR results. Default

is False.

\--OcrBuilder\_block\_mode\_intersection\_thresh FLOAT

Max intersection before falling back to line

mode Default is 0.5.

\--OcrBuilder\_block\_mode\_max\_lines INTEGER

Max lines within a block before falling back

to line mode Default is 15.

\--OcrBuilder\_block\_mode\_max\_height\_frac FLOAT

Max height of a block as a percentage of the

page before falling back to line mode

Default is 0.5.

\--StructureBuilder\_gap\_threshold FLOAT

The minimum gap between blocks to consider

them part of the same group. Default is

0.05.

\--StructureBuilder\_list\_gap\_threshold FLOAT

The minimum gap between list items to

consider them part of the same group.

Default is 0.1.

\--BlankPageProcessor\_full\_page\_block\_intersection\_threshold FLOAT

Threshold to detect blank pages at Default

is 0.8.

\--BlankPageProcessor\_filter\_blank\_pages

Remove blank pages detected as images.

Default is False.

\--BlockRelabelProcessor\_block\_relabel\_str TEXT

Comma-separated relabeling rules in the

format '<original\_label>:<new\_label>:<confid

ence\_threshold>'. Each rule defines how

blocks of a certain type should be relabeled

when the confidence exceeds the threshold.

Example:

'Table:Picture:0.85,Form:Picture:0.9'

Default is.

\--BlockquoteProcessor\_min\_x\_indent FLOAT

The minimum horizontal indentation required

to consider a block as part of a blockquote.

Expressed as a percentage of the block

width. Default is 0.1.

\--BlockquoteProcessor\_x\_start\_tolerance FLOAT

The maximum allowable difference between the

starting x-coordinates of consecutive blocks

to consider them aligned. Expressed as a

percentage of the block width. Default is

0.01.

\--BlockquoteProcessor\_x\_end\_tolerance FLOAT

The maximum allowable difference between the

ending x-coordinates of consecutive blocks

to consider them aligned. Expressed as a

percentage of the block width. Default is

0.01.

\--DebugProcessor\_debug\_data\_folder TEXT

The folder to dump debug data to. Default is

debug\_data.

\--DebugProcessor\_debug\_layout\_images

Whether to dump layout debug images. Default

is False.

\--DebugProcessor\_debug\_pdf\_images

Whether to dump PDF debug images. Default is

False.

\--DebugProcessor\_debug\_json Whether to dump block debug data. Default is

False.

\--EquationProcessor\_model\_max\_length INTEGER

The maximum number of tokens to allow for

the Recognition model. Default is 1024.

\--EquationProcessor\_equation\_batch\_size INTEGER

The batch size to use for the recognition

model while processing equations. Default is

None, which will use the default batch size

for the model.

\--EquationProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--EquationProcessor\_drop\_repeated\_text

Drop repeated text in OCR results. Default

is False.

\--IgnoreTextProcessor\_common\_element\_threshold FLOAT

The minimum ratio of pages a text block must

appear on to be considered a common element.

Blocks that meet or exceed this threshold

are marked as common elements. Default is

0.2.

\--IgnoreTextProcessor\_common\_element\_min\_blocks INTEGER

The minimum number of occurrences of a text

block within a document to consider it a

common element. This ensures that rare

blocks are not mistakenly flagged. Default

is 3.

\--IgnoreTextProcessor\_max\_streak INTEGER

The maximum number of consecutive

occurrences of a text block allowed before

it is classified as a common element. Helps

to identify patterns like repeated headers

or footers. Default is 3.

\--IgnoreTextProcessor\_text\_match\_threshold INTEGER

The minimum fuzzy match score (0-100)

required to classify a text block as similar

to a common element. Higher values enforce

stricter matching. Default is 90.

\--LineMergeProcessor\_min\_merge\_pct FLOAT

The minimum percentage of intersection area

to consider merging. Default is 0.015.

\--LineMergeProcessor\_block\_expand\_threshold FLOAT

The percentage of the block width to expand

the bounding box. Default is 0.05.

\--LineMergeProcessor\_min\_merge\_ydist FLOAT

The minimum y distance between lines to

consider merging. Default is 5.

\--LineMergeProcessor\_intersection\_pct\_threshold FLOAT

The total amount of intersection area

concentrated in the max intersection block.

Default is 0.5.

\--LineMergeProcessor\_vertical\_overlap\_pct\_threshold FLOAT

The minimum percentage of vertical overlap

to consider merging. Default is 0.8.

\--LineMergeProcessor\_use\_llm Whether to use LLMs to improve accuracy.

Default is False.

\--LineNumbersProcessor\_strip\_numbers\_threshold FLOAT

The fraction of lines or tokens in a block

that must be numeric to consider them as

line numbers. Default is 0.6.

\--LineNumbersProcessor\_min\_lines\_in\_block INTEGER

The minimum number of lines required in a

block for it to be considered during

processing. Ensures that small blocks are

ignored as they are unlikely to contain

meaningful line numbers. Default is 4.

\--LineNumbersProcessor\_min\_line\_length INTEGER

The minimum length of a line (in characters)

to consider it significant when checking for

numeric prefixes or suffixes. Prevents false

positives for short lines. Default is 10.

\--LineNumbersProcessor\_min\_line\_number\_span\_ratio FLOAT

The minimum ratio of detected line number

spans to total lines required to treat them

as line numbers. Default is 0.6.

\--ListProcessor\_min\_x\_indent FLOAT

The minimum horizontal indentation required

to consider a block as a nested list item.

This is expressed as a percentage of the

page width and is used to determine

hierarchical relationships within a list.

Default is 0.01.

\--LLMComplexRegionProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMComplexRegionProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.01.

\--LLMComplexRegionProcessor\_use\_llm

Whether to use the LLM model. Default is

False.

\--LLMComplexRegionProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMEquationProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMEquationProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.05.

\--LLMEquationProcessor\_use\_llm Whether to use the LLM model. Default is

False.

\--LLMEquationProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMEquationProcessor\_min\_equation\_height FLOAT

The minimum ratio between equation height

and page height to consider for processing.

Default is 0.06.

\--LLMEquationProcessor\_redo\_inline\_math

Whether to redo inline math blocks. Default

is False.

\--LLMEquationProcessor\_equation\_latex\_prompt TEXT

The prompt to use for generating LaTeX from

equations. Default is a string containing

the Gemini prompt.

\--LLMFormProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMFormProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.01.

\--LLMFormProcessor\_use\_llm Whether to use the LLM model. Default is

False.

\--LLMFormProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMHandwritingProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMHandwritingProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.01.

\--LLMHandwritingProcessor\_use\_llm

Whether to use the LLM model. Default is

False.

\--LLMHandwritingProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMHandwritingProcessor\_handwriting\_generation\_prompt TEXT

The prompt to use for OCRing handwriting.

Default is a string containing the Gemini

prompt.

\--LLMImageDescriptionProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMImageDescriptionProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.01.

\--LLMImageDescriptionProcessor\_use\_llm

Whether to use the LLM model. Default is

False.

\--LLMImageDescriptionProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMImageDescriptionProcessor\_extract\_images BOOLEAN

Extract images from the document. Default is

True.

\--LLMImageDescriptionProcessor\_image\_description\_prompt TEXT

The prompt to use for generating image

descriptions. Default is a string containing

the Gemini prompt.

\--LLMMathBlockProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMMathBlockProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.01.

\--LLMMathBlockProcessor\_use\_llm

Whether to use the LLM model. Default is

False.

\--LLMMathBlockProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMMathBlockProcessor\_redo\_inline\_math

If True, the inline math will be re-done,

otherwise it will be left as is. Default is

False.

\--LLMMathBlockProcessor\_inlinemath\_min\_ratio FLOAT

If more than this ratio of blocks are

inlinemath blocks, assume everything has

math. Default is 0.4.

\--LLMSimpleBlockMetaProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMSimpleBlockMetaProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.01.

\--LLMSimpleBlockMetaProcessor\_use\_llm

Whether to use the LLM model. Default is

False.

\--LLMSimpleBlockMetaProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMPageCorrectionProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMPageCorrectionProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.01.

\--LLMPageCorrectionProcessor\_use\_llm

Whether to use the LLM model. Default is

False.

\--LLMPageCorrectionProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMPageCorrectionProcessor\_block\_correction\_prompt TEXT

The user prompt to guide the block

correction process. Default is None.

\--LLMSectionHeaderProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMSectionHeaderProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.01.

\--LLMSectionHeaderProcessor\_use\_llm

Whether to use the LLM model. Default is

False.

\--LLMSectionHeaderProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMTableProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMTableProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.01.

\--LLMTableProcessor\_use\_llm Whether to use the LLM model. Default is

False.

\--LLMTableProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMTableProcessor\_max\_rows\_per\_batch INTEGER

If the table has more rows than this, chunk

the table. (LLMs can be inaccurate with a

lot of rows) Default is 60.

\--LLMTableProcessor\_max\_table\_rows INTEGER

The maximum number of rows in a table to

process with the LLM processor. Beyond this

will be skipped. Default is 175.

\--LLMTableProcessor\_table\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.

\--LLMTableProcessor\_rotation\_max\_wh\_ratio FLOAT

The maximum width/height ratio for table

cells for a table to be considered rotated.

Default is 0.6.

\--LLMTableProcessor\_max\_table\_iterations INTEGER

The maximum number of iterations to attempt

rewriting a table. Default is 2.

\--LLMTableProcessor\_table\_rewriting\_prompt TEXT

The prompt to use for rewriting text.

Default is a string containing the Gemini

rewriting prompt.

\--LLMTableMergeProcessor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--LLMTableMergeProcessor\_image\_expansion\_ratio FLOAT

The ratio to expand the image by when

cropping. Default is 0.01.

\--LLMTableMergeProcessor\_use\_llm

Whether to use the LLM model. Default is

False.

\--LLMTableMergeProcessor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--LLMTableMergeProcessor\_table\_height\_threshold FLOAT

The minimum height ratio relative to the

page for the first table in a pair to be

considered for merging. Default is 0.6.

\--LLMTableMergeProcessor\_table\_start\_threshold FLOAT

The maximum percentage down the page the

second table can start to be considered for

merging. Default is 0.2.

\--LLMTableMergeProcessor\_vertical\_table\_height\_threshold FLOAT

The height tolerance for 2 adjacent tables

to be merged into one. Default is 0.25.

\--LLMTableMergeProcessor\_vertical\_table\_distance\_threshold INTEGER

The maximum distance between table edges for

adjacency. Default is 20.

\--LLMTableMergeProcessor\_horizontal\_table\_width\_threshold FLOAT

The width tolerance for 2 adjacent tables to

be merged into one. Default is 0.25.

\--LLMTableMergeProcessor\_horizontal\_table\_distance\_threshold INTEGER

The maximum distance between table edges for

adjacency. Default is 10.

\--LLMTableMergeProcessor\_column\_gap\_threshold INTEGER

The maximum gap between columns to merge

tables Default is 50.

\--LLMTableMergeProcessor\_no\_merge\_tables\_across\_pages

Whether to disable merging tables across

pages and keep page delimiters. Default is

False.

\--LLMTableMergeProcessor\_table\_merge\_prompt TEXT

The prompt to use for rewriting text.

Default is a string containing the Gemini

rewriting prompt.

\--SectionHeaderProcessor\_level\_count INTEGER

The number of levels to use for headings.

Default is 4.

\--SectionHeaderProcessor\_merge\_threshold FLOAT

The minimum gap between headings to consider

them part of the same group. Default is

0.25.

\--SectionHeaderProcessor\_default\_level INTEGER

The default heading level to use if no

heading level is detected. Default is 2.

\--SectionHeaderProcessor\_height\_tolerance FLOAT

The minimum height of a heading to consider

it a heading. Default is 0.99.

\--TableProcessor\_table\_rec\_batch\_size INTEGER

The batch size to use for the table

recognition model. Default is None, which

will use the default batch size for the

model.

\--TableProcessor\_detection\_batch\_size INTEGER

The batch size to use for the table

detection model. Default is None, which will

use the default batch size for the model.

\--TableProcessor\_recognition\_batch\_size INTEGER

The batch size to use for the table

recognition model. Default is None, which

will use the default batch size for the

model.

\--TableProcessor\_row\_split\_threshold FLOAT

The percentage of rows that need to be split

across the table before row splitting is

active. Default is 0.5.

\--TableProcessor\_pdftext\_workers INTEGER

The number of workers to use for pdftext.

Default is 1.

\--TableProcessor\_disable\_tqdm Whether to disable the tqdm progress bar.

Default is False.

\--TableProcessor\_drop\_repeated\_table\_text

Drop repeated text in OCR results. Default

is False.

\--TableProcessor\_disable\_ocr\_math

Disable inline math recognition in OCR

Default is False.

\--TableProcessor\_disable\_ocr Disable OCR entirely. Default is False.

\--TextProcessor\_column\_gap\_ratio FLOAT

The minimum ratio of the page width to the

column gap to consider a column break.

Default is 0.02.

\--ExtractionConverter\_use\_llm Enable higher quality processing with LLMs.

Default is False.

\--ExtractionConverter\_pattern TEXT

Default is {\\d+\\}-{48}\\n\\n.

\--ExtractionConverter\_existing\_markdown TEXT

Markdown that was already converted for

extraction. Default is None.

\--PdfConverter\_use\_llm Enable higher quality processing with LLMs.

Default is False.

\--OCRConverter\_use\_llm Enable higher quality processing with LLMs.

Default is False.

\--TableConverter\_use\_llm Enable higher quality processing with LLMs.

Default is False.

\--DocumentProvider\_pdftext\_workers INTEGER

The number of workers to use for pdftext.

Default is 4.

\--DocumentProvider\_flatten\_pdf BOOLEAN

Whether to flatten the PDF structure.

Default is True.

\--DocumentProvider\_force\_ocr Whether to force OCR on the whole document.

Default is False.

\--DocumentProvider\_ocr\_space\_threshold FLOAT

The minimum ratio of spaces to non-spaces to

detect bad text. Default is 0.7.

\--DocumentProvider\_ocr\_newline\_threshold FLOAT

The minimum ratio of newlines to non-

newlines to detect bad text. Default is 0.6.

\--DocumentProvider\_ocr\_alphanum\_threshold FLOAT

The minimum ratio of alphanumeric characters

to non-alphanumeric characters to consider

an alphanumeric character. Default is 0.3.

\--DocumentProvider\_image\_threshold FLOAT

The minimum coverage ratio of the image to

the page to consider skipping the page.

Default is 0.65.

\--DocumentProvider\_strip\_existing\_ocr

Whether to strip existing OCR text from the

PDF. Default is False.

\--DocumentProvider\_disable\_links

Whether to disable links. Default is False.

\--DocumentProvider\_keep\_chars Whether to keep character-level information

in the output. Default is False.

\--PdfProvider\_pdftext\_workers INTEGER

The number of workers to use for pdftext.

Default is 4.

\--PdfProvider\_flatten\_pdf BOOLEAN

Whether to flatten the PDF structure.

Default is True.

\--PdfProvider\_force\_ocr Whether to force OCR on the whole document.

Default is False.

\--PdfProvider\_ocr\_space\_threshold FLOAT

The minimum ratio of spaces to non-spaces to

detect bad text. Default is 0.7.

\--PdfProvider\_ocr\_newline\_threshold FLOAT

The minimum ratio of newlines to non-

newlines to detect bad text. Default is 0.6.

\--PdfProvider\_ocr\_alphanum\_threshold FLOAT

The minimum ratio of alphanumeric characters

to non-alphanumeric characters to consider

an alphanumeric character. Default is 0.3.

\--PdfProvider\_image\_threshold FLOAT

The minimum coverage ratio of the image to

the page to consider skipping the page.

Default is 0.65.

\--PdfProvider\_strip\_existing\_ocr

Whether to strip existing OCR text from the

PDF. Default is False.

\--PdfProvider\_disable\_links Whether to disable links. Default is False.

\--PdfProvider\_keep\_chars Whether to keep character-level information

in the output. Default is False.

\--EpubProvider\_pdftext\_workers INTEGER

The number of workers to use for pdftext.

Default is 4.

\--EpubProvider\_flatten\_pdf BOOLEAN

Whether to flatten the PDF structure.

Default is True.

\--EpubProvider\_force\_ocr Whether to force OCR on the whole document.

Default is False.

\--EpubProvider\_ocr\_space\_threshold FLOAT

The minimum ratio of spaces to non-spaces to

detect bad text. Default is 0.7.

\--EpubProvider\_ocr\_newline\_threshold FLOAT

The minimum ratio of newlines to non-

newlines to detect bad text. Default is 0.6.

\--EpubProvider\_ocr\_alphanum\_threshold FLOAT

The minimum ratio of alphanumeric characters

to non-alphanumeric characters to consider

an alphanumeric character. Default is 0.3.

\--EpubProvider\_image\_threshold FLOAT

The minimum coverage ratio of the image to

the page to consider skipping the page.

Default is 0.65.

\--EpubProvider\_strip\_existing\_ocr

Whether to strip existing OCR text from the

PDF. Default is False.

\--EpubProvider\_disable\_links Whether to disable links. Default is False.

\--EpubProvider\_keep\_chars Whether to keep character-level information

in the output. Default is False.

\--HTMLProvider\_pdftext\_workers INTEGER

The number of workers to use for pdftext.

Default is 4.

\--HTMLProvider\_flatten\_pdf BOOLEAN

Whether to flatten the PDF structure.

Default is True.

\--HTMLProvider\_force\_ocr Whether to force OCR on the whole document.

Default is False.

\--HTMLProvider\_ocr\_space\_threshold FLOAT

The minimum ratio of spaces to non-spaces to

detect bad text. Default is 0.7.

\--HTMLProvider\_ocr\_newline\_threshold FLOAT

The minimum ratio of newlines to non-

newlines to detect bad text. Default is 0.6.

\--HTMLProvider\_ocr\_alphanum\_threshold FLOAT

The minimum ratio of alphanumeric characters

to non-alphanumeric characters to consider

an alphanumeric character. Default is 0.3.

\--HTMLProvider\_image\_threshold FLOAT

The minimum coverage ratio of the image to

the page to consider skipping the page.

Default is 0.65.

\--HTMLProvider\_strip\_existing\_ocr

Whether to strip existing OCR text from the

PDF. Default is False.

\--HTMLProvider\_disable\_links Whether to disable links. Default is False.

\--HTMLProvider\_keep\_chars Whether to keep character-level information

in the output. Default is False.

\--ImageProvider\_image\_count INTEGER

Default is 1.

\--PowerPointProvider\_pdftext\_workers INTEGER

The number of workers to use for pdftext.

Default is 4.

\--PowerPointProvider\_flatten\_pdf BOOLEAN

Whether to flatten the PDF structure.

Default is True.

\--PowerPointProvider\_force\_ocr Whether to force OCR on the whole document.

Default is False.

\--PowerPointProvider\_ocr\_space\_threshold FLOAT

The minimum ratio of spaces to non-spaces to

detect bad text. Default is 0.7.

\--PowerPointProvider\_ocr\_newline\_threshold FLOAT

The minimum ratio of newlines to non-

newlines to detect bad text. Default is 0.6.

\--PowerPointProvider\_ocr\_alphanum\_threshold FLOAT

The minimum ratio of alphanumeric characters

to non-alphanumeric characters to consider

an alphanumeric character. Default is 0.3.

\--PowerPointProvider\_image\_threshold FLOAT

The minimum coverage ratio of the image to

the page to consider skipping the page.

Default is 0.65.

\--PowerPointProvider\_strip\_existing\_ocr

Whether to strip existing OCR text from the

PDF. Default is False.

\--PowerPointProvider\_disable\_links

Whether to disable links. Default is False.

\--PowerPointProvider\_keep\_chars

Whether to keep character-level information

in the output. Default is False.

\--PowerPointProvider\_include\_slide\_number

Default is False.

\--SpreadSheetProvider\_pdftext\_workers INTEGER

The number of workers to use for pdftext.

Default is 4.

\--SpreadSheetProvider\_flatten\_pdf BOOLEAN

Whether to flatten the PDF structure.

Default is True.

\--SpreadSheetProvider\_force\_ocr

Whether to force OCR on the whole document.

Default is False.

\--SpreadSheetProvider\_ocr\_space\_threshold FLOAT

The minimum ratio of spaces to non-spaces to

detect bad text. Default is 0.7.

\--SpreadSheetProvider\_ocr\_newline\_threshold FLOAT

The minimum ratio of newlines to non-

newlines to detect bad text. Default is 0.6.

\--SpreadSheetProvider\_ocr\_alphanum\_threshold FLOAT

The minimum ratio of alphanumeric characters

to non-alphanumeric characters to consider

an alphanumeric character. Default is 0.3.

\--SpreadSheetProvider\_image\_threshold FLOAT

The minimum coverage ratio of the image to

the page to consider skipping the page.

Default is 0.65.

\--SpreadSheetProvider\_strip\_existing\_ocr

Whether to strip existing OCR text from the

PDF. Default is False.

\--SpreadSheetProvider\_disable\_links

Whether to disable links. Default is False.

\--SpreadSheetProvider\_keep\_chars

Whether to keep character-level information

in the output. Default is False.

\--ChunkRenderer\_extract\_images BOOLEAN

Extract images from the document. Default is

True.

\--ChunkRenderer\_keep\_pageheader\_in\_output

Keep the page header in the output HTML.

Default is False.

\--ChunkRenderer\_keep\_pagefooter\_in\_output

Keep the page footer in the output HTML.

Default is False.

\--ChunkRenderer\_add\_block\_ids Whether to add block IDs to the output HTML.

Default is False.

\--JSONRenderer\_extract\_images BOOLEAN

Extract images from the document. Default is

True.

\--JSONRenderer\_keep\_pageheader\_in\_output

Keep the page header in the output HTML.

Default is False.

\--JSONRenderer\_keep\_pagefooter\_in\_output

Keep the page footer in the output HTML.

Default is False.

\--JSONRenderer\_add\_block\_ids Whether to add block IDs to the output HTML.

Default is False.

\--ExtractionRenderer\_extract\_images BOOLEAN

Extract images from the document. Default is

True.

\--ExtractionRenderer\_keep\_pageheader\_in\_output

Keep the page header in the output HTML.

Default is False.

\--ExtractionRenderer\_keep\_pagefooter\_in\_output

Keep the page footer in the output HTML.

Default is False.

\--ExtractionRenderer\_add\_block\_ids

Whether to add block IDs to the output HTML.

Default is False.

\--HTMLRenderer\_extract\_images BOOLEAN

Extract images from the document. Default is

True.

\--HTMLRenderer\_keep\_pageheader\_in\_output

Keep the page header in the output HTML.

Default is False.

\--HTMLRenderer\_keep\_pagefooter\_in\_output

Keep the page footer in the output HTML.

Default is False.

\--HTMLRenderer\_add\_block\_ids Whether to add block IDs to the output HTML.

Default is False.

\--HTMLRenderer\_paginate\_output Whether to paginate the output. Default is

False.

\--MarkdownRenderer\_extract\_images BOOLEAN

Extract images from the document. Default is

True.

\--MarkdownRenderer\_keep\_pageheader\_in\_output

Keep the page header in the output HTML.

Default is False.

\--MarkdownRenderer\_keep\_pagefooter\_in\_output

Keep the page footer in the output HTML.

Default is False.

\--MarkdownRenderer\_add\_block\_ids

Whether to add block IDs to the output HTML.

Default is False.

\--MarkdownRenderer\_paginate\_output

Whether to paginate the output. Default is

False.

\--MarkdownRenderer\_page\_separator TEXT

The separator to use between pages. Default

is '-' \* 48.

\--MarkdownRenderer\_html\_tables\_in\_markdown

Return tables formatted as HTML, instead of

in markdown Default is False.

\--OCRJSONRenderer\_extract\_images BOOLEAN

Extract images from the document. Default is

True.

\--OCRJSONRenderer\_keep\_pageheader\_in\_output

Keep the page header in the output HTML.

Default is False.

\--OCRJSONRenderer\_keep\_pagefooter\_in\_output

Keep the page footer in the output HTML.

Default is False.

\--OCRJSONRenderer\_add\_block\_ids

Whether to add block IDs to the output HTML.

Default is False.

\--AzureOpenAIService\_timeout INTEGER

The timeout to use for the service. Default

is 30.

\--AzureOpenAIService\_max\_retries INTEGER

The maximum number of retries to use for the

service. Default is 2.

\--AzureOpenAIService\_retry\_wait\_time INTEGER

The wait time between retries. Default is 3.

\--AzureOpenAIService\_max\_output\_tokens INTEGER

The maximum number of output tokens to

generate. Default is None.

\--AzureOpenAIService\_azure\_endpoint TEXT

The Azure OpenAI endpoint URL. No trailing

slash. Default is None.

\--AzureOpenAIService\_azure\_api\_key TEXT

The API key to use for the Azure OpenAI

service. Default is None.

\--AzureOpenAIService\_azure\_api\_version TEXT

The Azure OpenAI API version to use. Default

is None.

\--AzureOpenAIService\_deployment\_name TEXT

The deployment name for the Azure OpenAI

model. Default is None.

\--ClaudeService\_timeout INTEGER

The timeout to use for the service. Default

is 30.

\--ClaudeService\_max\_retries INTEGER

The maximum number of retries to use for the

service. Default is 2.

\--ClaudeService\_retry\_wait\_time INTEGER

The wait time between retries. Default is 3.

\--ClaudeService\_max\_output\_tokens INTEGER

The maximum number of output tokens to

generate. Default is None.

\--ClaudeService\_claude\_model\_name TEXT

The name of the Google model to use for the

service. Default is

claude-3-7-sonnet-20250219.

\--ClaudeService\_claude\_api\_key TEXT

The Claude API key to use for the service.

Default is None.

\--ClaudeService\_max\_claude\_tokens INTEGER

The maximum number of tokens to use for a

single Claude request. Default is 8192.

\--GoogleGeminiService\_timeout INTEGER

The timeout to use for the service. Default

is 30.

\--GoogleGeminiService\_max\_retries INTEGER

The maximum number of retries to use for the

service. Default is 2.

\--GoogleGeminiService\_retry\_wait\_time INTEGER

The wait time between retries. Default is 3.

\--GoogleGeminiService\_max\_output\_tokens INTEGER

The maximum number of output tokens to

generate. Default is None.

\--GoogleGeminiService\_gemini\_model\_name TEXT

The name of the Google model to use for the

service. Default is gemini-2.0-flash.

\--GoogleGeminiService\_thinking\_budget INTEGER

The thinking token budget to use for the

service. Default is None.

\--GoogleGeminiService\_gemini\_api\_key TEXT

The Google API key to use for the service.

Default is None.

\--OllamaService\_timeout INTEGER

The timeout to use for the service. Default

is 30.

\--OllamaService\_max\_retries INTEGER

The maximum number of retries to use for the

service. Default is 2.

\--OllamaService\_retry\_wait\_time INTEGER

The wait time between retries. Default is 3.

\--OllamaService\_max\_output\_tokens INTEGER

The maximum number of output tokens to

generate. Default is None.

\--OllamaService\_ollama\_base\_url TEXT

The base url to use for ollama. No trailing

slash. Default is http://localhost:11434.

\--OllamaService\_ollama\_model TEXT

The model name to use for ollama. Default is

llama3.2-vision.

\--OpenAIService\_timeout INTEGER

The timeout to use for the service. Default

is 30.

\--OpenAIService\_max\_retries INTEGER

The maximum number of retries to use for the

service. Default is 2.

\--OpenAIService\_retry\_wait\_time INTEGER

The wait time between retries. Default is 3.

\--OpenAIService\_max\_output\_tokens INTEGER

The maximum number of output tokens to

generate. Default is None.

\--OpenAIService\_openai\_base\_url TEXT

The base url to use for OpenAI-like models.

No trailing slash. Default is

https://api.openai.com/v1.

\--OpenAIService\_openai\_model TEXT

The model name to use for OpenAI-like model.

Default is gpt-4o-mini.

\--OpenAIService\_openai\_api\_key TEXT

The API key to use for the OpenAI-like

service. Default is None.

\--OpenAIService\_openai\_image\_format TEXT

The image format to use for the OpenAI-like

service. Use 'png' for better compatability

Default is webp.

\--GoogleVertexService\_timeout INTEGER

The timeout to use for the service. Default

is 30.

\--GoogleVertexService\_max\_retries INTEGER

The maximum number of retries to use for the

service. Default is 2.

\--GoogleVertexService\_retry\_wait\_time INTEGER

The wait time between retries. Default is 3.

\--GoogleVertexService\_max\_output\_tokens INTEGER

The maximum number of output tokens to

generate. Default is None.

\--GoogleVertexService\_gemini\_model\_name TEXT

The name of the Google model to use for the

service. Default is gemini-2.0-flash-001.

\--GoogleVertexService\_thinking\_budget INTEGER

The thinking token budget to use for the

service. Default is None.

\--GoogleVertexService\_vertex\_project\_id TEXT

Google Cloud Project ID for Vertex AI.

Default is None.

\--GoogleVertexService\_vertex\_location TEXT

Google Cloud Location for Vertex AI. Default

is us-central1.

\--GoogleVertexService\_vertex\_dedicated

Whether to use a dedicated Vertex AI

instance. Default is False.

\--DocumentExtractor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--DocumentExtractor\_disable\_tqdm

Whether to disable the tqdm progress bar.

Default is False.

\--DocumentExtractor\_page\_schema TEXT

The JSON schema to be extracted from the

page. Default is.

\--PageExtractor\_max\_concurrency INTEGER

The maximum number of concurrent requests to

make to the Gemini model. Default is 3.

\--PageExtractor\_disable\_tqdm Whether to disable the tqdm progress bar.

Default is False.

\--PageExtractor\_extraction\_page\_chunk\_size INTEGER

The number of pages to chunk together for

extraction. Default is 3.

\--PageExtractor\_page\_schema TEXT

The JSON schema to be extracted from the

page. Default is.

\--help Show this message and exit.

It appears you are using a more recent version of **Marker** where the CLI signature has been streamlined. In this version, `marker_single` is designed for high-precision single-file conversion and has moved the language and output logic into specific flags.

The error occurred because `--languages` is now primarily a feature of the batch `marker` command, and your command structure placed the output directory as a positional argument rather than a flagged one.

### 1\. Corrected marker\_single Syntax

Based on the `--help` output you provided, the correct logic for converting your book is:

Bash

```markdown
marker_single --output_dir ./ "Making_Habits__Breaking_Habits__How_to_Mak_-_Jeremy_Dean.epub"
```

**What changed in the logic:**

- **Flag Placement:** Options must precede the file path (`FPATH`).
- **Output Flag:** You must explicitly use `--output_dir` to define where the Markdown results should be saved.
- **Auto-Detection:** In the single-file utility, Marker now defaults to auto-detecting the language. If you need to force English via a configuration, you would pass a `--config_json` file, though auto-detection is generally sufficient for standard English texts.

---

### 2\. Batch Processing (The "Architectural" Way)

Since you mentioned having a full Calibre library, using `marker_single` repeatedly is inefficient. You should check the help output for the batch tool, which likely supports the `--languages` flag you were looking for:

Bash

```markdown
marker --help
```

If the batch tool is available in your path, the command for your entire library would look like this:

Bash

```markdown
marker /path/to/calibre/library /path/to/output/vault --languages English
```

---

### 3\. Improving Outcomes for your RAG Pipeline

Once you have the Markdown files from Marker, keep in mind that EPUBs often contain "back matter" (indices, bibliographies, and advertisements) that dilute **concept density**.

Since you are building a custom pipeline, I recommend adding a **post-conversion filter** before you embed the text into your vector database.

**Logic for a high-density filter:**

1. **Drop-Zone Detection:** Identify keywords like "Index," "Bibliography," or "About the Author" in the Markdown headers.
2. **Trimming:** Programmatically truncate the file after these sections appear. This ensures your Gemini CLI is only searching the "core logic" of the book, reducing token costs and increasing retrieval accuracy.

### 4\. Next Step

Now that you have the tool running, would you like me to show you how to use **LlamaIndex** or **LangChain** to take these Marker-generated files and index them into a local **LanceDB** instance for your semantic searches?

Google Account

Leon Ormes

leonormes@gmail.com
