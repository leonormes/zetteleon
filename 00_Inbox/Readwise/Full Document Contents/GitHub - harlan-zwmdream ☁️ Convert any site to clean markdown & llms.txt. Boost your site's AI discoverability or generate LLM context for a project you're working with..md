# GitHub - harlan-zw/mdream: ☁️ Convert any site to clean markdown & llms.txt. Boost your site's AI discoverability or generate LLM context for a project you're working with.

![rw-book-cover](https://opengraph.githubassets.com/2f616b4040936f0b7d6e5c902227401424bbf66ceb3605eefb3a4e92ba1b907c/harlan-zw/mdream)

## Metadata
- Author: [[https://github.com/harlan-zw/]]
- Full Title: GitHub - harlan-zw/mdream: ☁️ Convert any site to clean markdown & llms.txt. Boost your site's AI discoverability or generate LLM context for a project you're working with.
- Category: #articles
- Summary: Mdream converts websites into clean, minimal Markdown optimized for AI language models. It offers tools and plugins to crawl sites, generate Markdown files, and create LLM context artifacts. Mdream works with many platforms like Vite, Nuxt, Docker, and GitHub Actions for easy integration.
- URL: https://github.com/harlan-zw/mdream

## Full Document
### harlan-zw/mdream

Open more actions menu

### mdream

[![npm version](https://camo.githubusercontent.com/66d65d97631f5beded638b9987e5c3140467f6513a9d0386de5055c53c459089/68747470733a2f2f696d672e736869656c64732e696f2f6e706d2f762f6d647265616d3f636f6c6f723d79656c6c6f77)](https://npmjs.com/package/mdream)
[![npm downloads](https://camo.githubusercontent.com/a59bb5badefbc13973758a6e2bce65ce8e2a3e95ad82f9cad84023db6d46d760/68747470733a2f2f696d672e736869656c64732e696f2f6e706d2f646d2f6d647265616d3f636f6c6f723d79656c6c6f77)](https://npm.chart.dev/mdream)
[![license](https://camo.githubusercontent.com/65660aca1cfd91aec28073204879d29b2af4782aa89ac8c1b145abce1539ec1f/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f6861726c616e2d7a772f6d647265616d3f636f6c6f723d79656c6c6f77)](https://github.com/harlan-zw/mdream/blob/main/LICENSE.md)

>  Convert any site to clean markdown & llms.txt. Boost your site's AI discoverability or generate LLM context for a project you're working with.
> 
>  

[![mdream logo](https://github.com/harlan-zw/mdream/raw/main/.github/logo.png)](https://github.com/harlan-zw/mdream/blob/main/.github/logo.png)

|  |
| --- |
| Made possible by my [Sponsor Program 💖](https://github.com/sponsors/harlan-zw) Follow me [@harlan\_zw](https://twitter.com/harlan_zw) 🐦 • Join [Discord](https://discord.gg/275MBUBvgP) for help |

#### Features

* 🧠 Custom built HTML to Markdown Convertor Optimized for LLMs (~50% fewer tokens)
* 🔍 Generates [Minimal](https://github.com/harlan-zw/mdream/blob/main/packages/mdream/src/preset/minimal.ts) GitHub Flavored Markdown: Frontmatter, Nested & HTML markup support.
* 🚀 Ultra Fast: Stream 1.4MB of HTML to markdown in ~50ms.
* ⚡ Tiny: 5kB gzip, zero dependency core.
* ⚙️ Run anywhere: [CLI Crawler](https://github.com/harlan-zw/mdream#mdream-crawl), [Docker](https://github.com/harlan-zw/mdream#docker-usage), [GitHub Actions](https://github.com/harlan-zw/mdream#github-actions-integration), [Vite](https://github.com/harlan-zw/mdream#vite-integration), & more.
* 🔌 Extensible: [Plugin system](https://github.com/harlan-zw/mdream#plugin-system) for customizing and extending functionality.

#### What is Mdream?

Traditional HTML to Markdown converters were not built for LLMs or humans. They tend to be slow and bloated and produce output that's poorly suited for LLMs token usage or for human readability.

Other LLM specific convertors focus on supporting *all* document formats, resulting in larger bundles and lower quality Markdown output.

Mdream core is a highly optimized primitive for producing Markdown from HTML that is optimized for LLMs.

Mdream ships several packages on top of this to generate LLM artifacts like `llms.txt` for your own sites or generate LLM context for any project you're working with.

##### Mdream Packages

Mdream is built to run anywhere for all projects and use cases and is available in the following packages:

| Package | Description |
| --- | --- |
|  [mdream](https://github.com/harlan-zw/mdream#installation) | HTML to Markdown converter with CLI for `stdin` conversion and package API. **Minimal: no dependencies** |
|  [@mdream/crawl](https://github.com/harlan-zw/mdream#mdreamcrawl) | Site-wide crawler to generate `llms.txt` artifacts from entire websites |
|  [Docker](https://github.com/harlan-zw/mdream#docker) | Pre-built Docker image with Playwright Chrome for containerized website crawling |
|  [@mdream/vite](https://github.com/harlan-zw/mdream#vite-integration) | Generate automatic `.md` for your own Vite sites |
|  [@mdream/nuxt](https://github.com/harlan-zw/mdream#nuxt-integration) | Generate automatic `.md` and `llms.txt` artifacts generation for Nuxt Sites |
|  [@mdream/action](https://github.com/harlan-zw/mdream#github-actions-integration) | Generate `.md` and `llms.txt` artifacts from your static `.html` output |

#### Mdream Crawl

The `@mdream/crawl` package crawls an entire site generating LLM artifacts using `mdream` for Markdown conversion.

* [llms.txt](https://llmstxt.org/): A consolidated text file optimized for LLM consumption.
* [llms-full.txt](https://llmstxt.org/): An extended format with comprehensive metadata and full content.
* Individual Markdown Files: Each crawled page is saved as a separate Markdown file in the `md/` directory.

##### Usage

```
# Interactive
npx @mdream/crawl
# Simple
npx @mdream/crawl https://harlanzw.com
# Glob patterns
npx @mdream/crawl "https://nuxt.com/docs/getting-started/**"
# Get help
npx @mdream/crawl -h
```

##### Examples

**Crawl Using Playwright**

```
npx -p playwright -p @mdream/crawl crawl -u example.com --driver playwright
pnpm --package=playwright --package=@mdream/crawl dlx crawl example.com --driver playwright
```

**Exclude Specific Paths**

```
npx @mdream/crawl -u example.com --exclude "/admin/*" --exclude "/api/*"
```

**Large Site Crawling with Limits**

```
npx @mdream/crawl -u https://large-site.com \
  --max-pages 100 \
  --depth 2
```

#### Stdin CLI Usage

Mdream is much more minimal than Mdream Crawl. It provides a CLI designed to work exclusively with Unix pipes, providing flexibility and freedom to integrate with other tools.

**Pipe Site to Markdown**

Fetches the [Markdown Wikipedia page](https://en.wikipedia.org/wiki/Markdown) and converts it to Markdown preserving the original links and images.

```
curl -s https://en.wikipedia.org/wiki/Markdown \
 | npx mdream --origin https://en.wikipedia.org --preset minimal \
  | tee streaming.md
```

*Tip: The `--origin` flag will fix relative image and link paths*

**Local File to Markdown**

Converts a local HTML file to a Markdown file, using `tee` to write the output to a file and display it in the terminal.

```
cat index.html \
 | npx mdream --preset minimal \
  | tee streaming.md
```

##### CLI Options

* `--origin <url>`: Base URL for resolving relative links and images
* `--preset <preset>`: Conversion presets: minimal
* `--help`: Display help information
* `--version`: Display version information

#### Docker

Run `@mdream/crawl` with Playwright Chrome pre-installed for website crawling in containerized environments.

```
# Quick start
docker run harlanzw/mdream:latest site.com/docs/**

# Interactive mode
docker run -it harlanzw/mdream:latest

# Using Playwright for JavaScript sites
docker run harlanzw/mdream:latest spa-site.com --driver playwright
```

**Available Images:**

* `harlanzw/mdream:latest` - Latest stable release
* `ghcr.io/harlan-zw/mdream:latest` - GitHub Container Registry

See [DOCKER.md](https://github.com/harlan-zw/mdream/blob/main/DOCKER.md) for complete usage, configuration, and building instructions.

#### GitHub Actions Integration

Mdream provides a GitHub Action that processes HTML files using glob patterns to generate `llms.txt` artifacts in CI/CD workflows.

This is useful for prerendered sites, it creates both condensed and comprehensive LLM-ready files that can be uploaded as artifacts or deployed with your site whenever you make changes.

##### Complete Workflow Example

```
name: Generate LLMs.txt

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  generate-llms-txt:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build documentation
        run: npm run build

      - name: Generate llms.txt artifacts
        uses: harlan-zw/mdream@main
        with:
          glob: 'dist/**/*.html'
          site-name: My Documentation
          description: Comprehensive technical documentation and guides
          origin: 'https://mydocs.com'
          output: dist

      - name: Upload llms.txt artifacts
        uses: actions/upload-artifact@v4
        with:
          name: llms-txt-artifacts
          path: |
            dist/llms.txt
            dist/llms-full.txt
            dist/md/

      - name: Deploy to GitHub Pages (optional)
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

For all available options and advanced configuration, see the complete [action.yml](https://github.com/harlan-zw/mdream/blob/main/action.yml) specification.

#### Vite Integration

Mdream provides a Vite plugin that enables on-demand HTML to Markdown conversion.

* **Automatic Markdown**: Access any route with `.md` extension (e.g., `/about.html` → `/about.md`)
* **Build-time Generation**: Automatically generates static markdown files alongside HTML files

##### Installation

```
pnpm install @mdream/vite
```

##### Usage

```
import MdreamVite from '@mdream/vite'
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    MdreamVite()
  ]
})
```

For more details and advanced configuration, see the [Vite README](https://github.com/harlan-zw/mdream/blob/main/packages/vite/README.md).

#### Nuxt Integration

The Mdream Nuxt module features:

* **On-Demand Generation**: Access any route with `.md` extension (e.g., `/about` → `/about.md`)
* **LLMs.txt Generation**: Creates `llms.txt` and `llms-full.txt` artifacts during prerendering

##### Installation

```
pnpm add @mdream/nuxt
```

##### Usage

Add the module to your `nuxt.config.ts`:

```
export default defineNuxtConfig({
  modules: [
    '@mdream/nuxt'
  ],
})
```

Done! Add the `.md` to any URL path to access the markdown.

When statically generating your site with `nuxi generate` it will create `llms.txt` artifacts.

For more details and advanced configuration, see the [Nuxt Module README](https://github.com/harlan-zw/mdream/blob/main/packages/nuxt/README.md).

#### API Usage

##### Installation

```
pnpm add mdream
```

##### Usage

Mdream provides two main functions for working with HTML:

* `htmlToMarkdown`: Useful if you already have the entire HTML payload you want to convert.
* `streamHtmlToMarkdown`: Best practice if you are fetching or reading from a local file.

**Convert existing HTML**

```
import { htmlToMarkdown } from 'mdream'

// Simple conversion
const markdown = htmlToMarkdown('<h1>Hello World</h1>')
console.log(markdown) // # Hello World
```

**Convert from Fetch**

```
import { streamHtmlToMarkdown } from 'mdream'

// Using fetch with streaming
const response = await fetch('https://example.com')
const htmlStream = response.body
const markdownGenerator = streamHtmlToMarkdown(htmlStream, {
  origin: 'https://example.com'
})

// Process chunks as they arrive
for await (const chunk of markdownGenerator) {
  console.log(chunk)
}
```

**Pure HTML Parser**

If you only need to parse HTML into a DOM-like AST without converting to Markdown, use `parseHtml`:

```
import { parseHtml } from 'mdream'

const html = '<div><h1>Title</h1><p>Content</p></div>'
const { events, remainingHtml } = parseHtml(html)

// Process the parsed events
events.forEach((event) => {
  if (event.type === 'enter' && event.node.type === 'element') {
    console.log('Entering element:', event.node.tagName)
  }
})
```

The `parseHtml` function provides:

* **Pure AST parsing** - No markdown generation overhead
* **DOM events** - Enter/exit events for each element and text node
* **Plugin support** - Can apply plugins during parsing
* **Streaming compatible** - Works with the same plugin system

##### Presets

Presets are pre-configured combinations of plugins for common use cases.

###### Minimal Preset

The `minimal` preset optimizes for token reduction and cleaner output by removing non-essential content:

```
import { withMinimalPreset } from 'mdream/preset/minimal'

const options = withMinimalPreset({
  origin: 'https://example.com'
})
```

**Plugins included:**

* `isolateMainPlugin()` - Extracts main content area
* `frontmatterPlugin()` - Generates YAML frontmatter from meta tags
* `tailwindPlugin()` - Converts Tailwind classes to Markdown
* `filterPlugin()` - Excludes forms, navigation, buttons, footers, and other non-content elements

**CLI Usage:**

```
curl -s https://example.com | npx mdream --preset minimal --origin https://example.com
```

##### Plugin System

The plugin system allows you to customize HTML to Markdown conversion by hooking into the processing pipeline. Plugins can filter content, extract data, transform nodes, or add custom behavior.

###### Built-in Plugins

Mdream includes several built-in plugins that can be used individually or combined:

* **[`extractionPlugin`](https://github.com/harlan-zw/mdream/blob/main/packages/mdream/src/plugins/extraction.ts)**: Extract specific elements using CSS selectors for data analysis
* **[`filterPlugin`](https://github.com/harlan-zw/mdream/blob/main/packages/mdream/src/plugins/filter.ts)**: Include or exclude elements based on CSS selectors or tag IDs
* **[`frontmatterPlugin`](https://github.com/harlan-zw/mdream/blob/main/packages/mdream/src/plugins/frontmatter.ts)**: Generate YAML frontmatter from HTML head elements (title, meta tags)
* **[`isolateMainPlugin`](https://github.com/harlan-zw/mdream/blob/main/packages/mdream/src/plugins/isolate-main.ts)**: Isolate main content using `<main>` elements or header-to-footer boundaries
* **[`tailwindPlugin`](https://github.com/harlan-zw/mdream/blob/main/packages/mdream/src/plugins/tailwind.ts)**: Convert Tailwind CSS classes to Markdown formatting (bold, italic, etc.)
* **[`readabilityPlugin`](https://github.com/harlan-zw/mdream/blob/main/packages/mdream/src/plugins/readability.ts)**: Content scoring and extraction (experimental)

```
import { filterPlugin, frontmatterPlugin, isolateMainPlugin } from 'mdream/plugins'

const markdown = htmlToMarkdown(html, {
  plugins: [
    isolateMainPlugin(),
    frontmatterPlugin(),
    filterPlugin({ exclude: ['nav', '.sidebar', '#footer'] })
  ]
})
```

###### Plugin Hooks

* `beforeNodeProcess`: Called before any node processing, can skip nodes
* `onNodeEnter`: Called when entering an element node
* `onNodeExit`: Called when exiting an element node
* `processTextNode`: Called for each text node
* `processAttributes`: Called to process element attributes

###### Creating a Plugin

Use `createPlugin()` to create a plugin with type safety:

```
import type { ElementNode, TextNode } from 'mdream'
import { htmlToMarkdown } from 'mdream'
import { createPlugin } from 'mdream/plugins'

const myPlugin = createPlugin({
  onNodeEnter(node: ElementNode) {
    if (node.name === 'h1') {
      return '🔥 '
    }
  },

  processTextNode(textNode: TextNode) {
    // Transform text content
    if (textNode.parent?.attributes?.id === 'highlight') {
      return {
        content: `**${textNode.value}**`,
        skip: false
      }
    }
  }
})

// Use the plugin
const html: string = '<div id="highlight">Important text</div>'
const markdown: string = htmlToMarkdown(html, { plugins: [myPlugin] })
```

###### Example: Content Filter Plugin

```
import type { ElementNode, NodeEvent } from 'mdream'
import { ELEMENT_NODE } from 'mdream'
import { createPlugin } from 'mdream/plugins'

const adBlockPlugin = createPlugin({
  beforeNodeProcess(event: NodeEvent) {
    const { node } = event

    if (node.type === ELEMENT_NODE && node.name === 'div') {
      const element = node as ElementNode
      // Skip ads and promotional content
      if (element.attributes?.class?.includes('ad')
        || element.attributes?.id?.includes('promo')) {
        return { skip: true }
      }
    }
  }
})
```

###### Extraction Plugin

Extract specific elements and their content during HTML processing for data analysis or content discovery:

```
import { extractionPlugin, htmlToMarkdown } from 'mdream'

const html: string = `
  <article>
    <h2>Getting Started</h2>
    <p>This is a tutorial about web scraping.</p>
    <img src="/hero.jpg" alt="Hero image" />
  </article>
`

// Extract elements using CSS selectors
const plugin = extractionPlugin({
  'h2': (element: ExtractedElement, state: MdreamRuntimeState) => {
    console.log('Heading:', element.textContent) // "Getting Started"
    console.log('Depth:', state.depth) // Current nesting depth
  },
  'img[alt]': (element: ExtractedElement, state: MdreamRuntimeState) => {
    console.log('Image:', element.attributes.src, element.attributes.alt)
    // "Image: /hero.jpg Hero image"
    console.log('Context:', state.options) // Access to conversion options
  }
})

htmlToMarkdown(html, { plugins: [plugin] })
```

The extraction plugin provides memory-efficient element extraction with full text content and attributes, perfect for SEO analysis, content discovery, and data mining.

#### Credits

* [ultrahtml](https://github.com/natemoo-re/ultrahtml): HTML parsing inspiration

#### License

Licensed under the [MIT license](https://github.com/harlan-zw/mdream/blob/main/LICENSE.md).
