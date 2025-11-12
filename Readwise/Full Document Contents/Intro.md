# Intro

![rw-book-cover](https://social-cards.sst.dev/opencode-docs/SW50cm8%3D.png?desc=Get%20started%20with%20opencode.)

## Metadata
- Author: [[opencode]]
- Full Title: Intro
- Category: #articles
- Summary: Opencode is an AI coding tool that works in the terminal and supports many AI models. It has a user-friendly interface and lets multiple agents work on projects together. You can easily install it, log in with Claude accounts, and add other AI providers through Models.dev.
- URL: https://opencode.ai/docs/

## Full Document
[**opencode**](https://opencode.ai/) is an AI coding agent built for the terminal. It features:

* A responsive, native, themeable terminal UI.
* Automatically loads the right LSPs, so the LLMs make fewer mistakes.
* Have multiple agents working in parallel on the same project.
* Create shareable links to any session for reference or to debug.
* Log in with Anthropic to use your Claude Pro or Claude Max account.
* Supports 75+ LLM providers through [Models.dev](https://models.dev), including local models.

![opencode TUI with the opencode theme](https://opencode.ai/_astro/screenshot.B4yUNM4n_dwGlE.webp)opencode TUI with the opencode theme
You can also install the opencode binary through the following.

Terminal window
```
curl -fsSL https://opencode.ai/install | bash
```

Terminal window
```
brew install sst/tap/opencode
```

Terminal window
```
paru -S opencode-bin
```

Right now the automatic installation methods do not work properly on Windows. However you can grab the binary from the [Releases](https://github.com/sst/opencode/releases).

We recommend signing up for Claude Pro or Max, running `opencode auth login` and selecting Anthropic. It’s the most cost-effective way to use opencode.

opencode is powered by the provider list at [Models.dev](https://models.dev), so you can use `opencode auth login` to configure API keys for any provider you’d like to use. This is stored in `~/.local/share/opencode/auth.json`.

The Models.dev dataset is also used to detect common environment variables like `OPENAI_API_KEY` to autoload that provider.

If there are additional providers you want to use you can submit a PR to the [Models.dev repo](https://github.com/sst/models.dev). You can also [add them to your config](https://opencode.ai/docs/config) for yourself.
