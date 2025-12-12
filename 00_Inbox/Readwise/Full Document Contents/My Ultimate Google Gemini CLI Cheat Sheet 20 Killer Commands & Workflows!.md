# My Ultimate Google Gemini CLI Cheat Sheet: 20 Killer Commands & Workflows!

![rw-book-cover](https://substackcdn.com/image/fetch/$s_!Y5eY!,w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b80aa21-3626-4dc9-9159-15f86825c431_1042x435.jpeg)

## Metadata
- Author: [[Between the Clouds Newsletter]]
- Full Title: My Ultimate Google Gemini CLI Cheat Sheet: 20 Killer Commands & Workflows!
- Category: #articles
- Summary: Google's Gemini CLI lets you run AI commands directly in your terminal for coding, debugging, and automation. The free preview offers five ready-to-use workflows, like app scaffolding and auto-documentation. Paid subscribers get a full 20-command cheat sheet, toolkits, and extra features.
- URL: https://bleevht.substack.com/p/my-ultimate-google-gemini-cli-cheat

## Full Document
[![Between the Clouds Newsletter](https://substackcdn.com/image/fetch/$s_!N0yj!,w_80,h_80,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e17a48b-338f-40f3-b805-767eb64ad8f9_1024x1024.png)](https://bleevht.substack.com/)

### [Between the Clouds Newsletter](https://bleevht.substack.com/)

##### Step-by-step prompts, shell tricks, and pro tips to automate coding, debugging, and DevOps with Google’s free Gemini CLI.

“**[BetweentheClouds 1300+ subscribers: 25% discount offer code](https://bleevht.substack.com/25offnow)**”

Google’s brand-new **Gemini CLI** pipes the full Gemini 2.5 Pro model straight into your terminal. A quick Google sign-in unlocks roughly **60 requests per minute and 1 000 per day, free**. The tool is Apache-2.0 on GitHub, so you can fork or extend it however you like.

[![](https://substackcdn.com/image/fetch/$s_!Y5eY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b80aa21-3626-4dc9-9159-15f86825c431_1042x435.jpeg)](https://substackcdn.com/image/fetch/$s_!Y5eY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b80aa21-3626-4dc9-9159-15f86825c431_1042x435.jpeg)
Below you’ll find two parts:

* **Free Preview** – five copy-and-paste workflows you can run right now.
* **Paid Subscriber Section** – a 20-command deep-dive cheat sheet, ready-made aliases, safety flags, and a downloadable toolkit.

#### Quick Install (⏱ ≈30 s)

If you need to install NodeJS in Windows, you an use the following:

```
winget install -e --id OpenJS.NodeJS
```

[![](https://substackcdn.com/image/fetch/$s_!fey1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5ed4454-5d06-45bc-b4a0-ab6d6364707f_1113x626.jpeg)](https://substackcdn.com/image/fetch/$s_!fey1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5ed4454-5d06-45bc-b4a0-ab6d6364707f_1113x626.jpeg)
After you install NodeJS, you can then install Gemini CLI.

```
# Node 18 or newer required 
npm install -g @google/gemini-cli 

#Launch the Gemini CLI
gemini
```

[![](https://substackcdn.com/image/fetch/$s_!Japi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbaf87d54-6438-446f-b76e-f857c19dea2d_850x719.jpeg)](https://substackcdn.com/image/fetch/$s_!Japi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbaf87d54-6438-446f-b76e-f857c19dea2d_850x719.jpeg)
Prefer a one-off run?

```
npx https://github.com/google-gemini/gemini-cli
```

**Key launch modes**

Interactive chat:

`gemini`

You plan to ask follow-ups, run shell commands (`!`) or tools.

Single-shot:

`gemini --prompt "…"` (alias `-p`)

Prints an answer and exits – perfect for scripts and CI. Add `--tools <name>` if the prompt needs to run built-ins such as `git`.

#### Free Preview – 5 Instant-Win Workflows

##### 1. Scaffold an app from a PDF

```
gemini --prompt "Generate a minimal Flask API that satisfies requirements.pdf. Include a Dockerfile and unit tests.
```

##### 2. Auto-document any repo

```
gemini --prompt "@. Create a Mermaid diagram of this repo’s modules, classes and external services."

@. injects the whole repo (obeying .geminiignore). Gemini outputs Mermaid text – render it with npx @mermaid-js/mermaid-cli or a VS Code extension.
```

##### 3. One-liner Conventional Commit

```
git add . gemini --prompt "@. Generate a Conventional Commits message for the staged diff." --tools git
```

##### 4. Shell-mode troubleshooting

```
gemini # start the REPL > !journalctl -u kubelet -n 500 > Summarise the recurring errors and propose three fixes.
```

The `!` prefix runs a local command and streams the output back so Gemini can analyse it.

##### 5. Release notes + hero image in one go

```
gemini --prompt "@. Take CHANGELOG.md, craft 280-char release notes, then call Imagen to create a 16:9 banner." --tools genmedia
```

*Requires the* `gen-media` *MCP server – details in the paid section.*

##### Enjoying the preview?

Unlock the full **20-command power cheat sheet**, a 40-line `gemini_toolkit.sh`, and future updates by becoming a paid subscriber.
