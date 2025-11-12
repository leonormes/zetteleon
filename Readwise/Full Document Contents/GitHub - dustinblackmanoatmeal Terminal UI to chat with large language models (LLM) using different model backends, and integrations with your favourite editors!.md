# GitHub - dustinblackman/oatmeal: Terminal UI to chat with large language models (LLM) using different model backends, and integrations with your favourite editors!

![rw-book-cover](https://repository-images.githubusercontent.com/714853510/5460077e-7aa5-445a-89d0-f0891f8360cc)

## Metadata
- Author: [[https://github.com/dustinblackman/]]
- Full Title: GitHub - dustinblackman/oatmeal: Terminal UI to chat with large language models (LLM) using different model backends, and integrations with your favourite editors!
- Category: #articles
- Summary: Oatmeal is a terminal chat app for talking to large language models using different backends.  
It integrates with editors like Neovim and can append or replace code blocks from model output.  
It is configurable, saves chat sessions, and can be installed on many platforms.
- URL: https://github.com/dustinblackman/oatmeal

## Full Document
### dustinblackman/oatmeal

### Oatmeal

[![oatmeal](https://github.com/dustinblackman/oatmeal/raw/main/.github/banner.png)](https://github.com/dustinblackman/oatmeal/blob/main/.github/banner.png)
[![Build Status](https://camo.githubusercontent.com/4d115689f8bbe7e88e6973c816882e6ff9cf0646a926a38e7ee64e3dab1e78e7/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f616374696f6e732f776f726b666c6f772f7374617475732f64757374696e626c61636b6d616e2f6f61746d65616c2f63692e796d6c3f6272616e63683d6d61696e)](https://github.com/dustinblackman/oatmeal/actions)
[![Release](https://camo.githubusercontent.com/0522b93bafa66cbcec9bae867203fb1fb0a8933976aa8db4d46c3f401f749f26/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f762f72656c656173652f64757374696e626c61636b6d616e2f6f61746d65616c)](https://github.com/dustinblackman/oatmeal/releases)
[![Coverage Status](https://camo.githubusercontent.com/880698669bc547611976a8e4ff7c49ea47f163852dad2435ccda32c2480d2024/68747470733a2f2f636f766572616c6c732e696f2f7265706f732f6769746875622f64757374696e626c61636b6d616e2f6f61746d65616c2f62616467652e7376673f6272616e63683d6d61696e)](https://coveralls.io/github/dustinblackman/oatmeal?branch=main)

>  Terminal UI to chat with large language models (LLM) using different model backends, and integrations with your favourite [editors](https://github.com/dustinblackman/oatmeal#editors)!
> 
>  

* [Overview](https://github.com/dustinblackman/oatmeal#Overview)
* [Install](https://github.com/dustinblackman/oatmeal#Install)
	+ [MacOS](https://github.com/dustinblackman/oatmeal#macos)
	+ [Debian / Ubuntu](https://github.com/dustinblackman/oatmeal#debian--ubuntu)
	+ [Fedora / CentOS](https://github.com/dustinblackman/oatmeal#fedora--centos)
	+ [Nix](https://github.com/dustinblackman/oatmeal#nix)
	+ [Arch Linux](https://github.com/dustinblackman/oatmeal#arch-linux)
	+ [Alpine Linux](https://github.com/dustinblackman/oatmeal#alpine-linux)
	+ [Windows](https://github.com/dustinblackman/oatmeal#windows)
	+ [Cargo](https://github.com/dustinblackman/oatmeal#cargo)
	+ [Docker](https://github.com/dustinblackman/oatmeal#docker)
	+ [Manual](https://github.com/dustinblackman/oatmeal#manual)
	+ [Source](https://github.com/dustinblackman/oatmeal#source)
* [Usage](https://github.com/dustinblackman/oatmeal#Usage)
	+ [Configuration](https://github.com/dustinblackman/oatmeal#configuration)
	+ [Backends](https://github.com/dustinblackman/oatmeal#backends)
	+ [Editors](https://github.com/dustinblackman/oatmeal#editors)
	+ [Themes](https://github.com/dustinblackman/oatmeal#themes)
	+ [Sessions](https://github.com/dustinblackman/oatmeal#sessions)
* [Contributing](https://github.com/dustinblackman/oatmeal#contributing)
	+ [Report an issue](https://github.com/dustinblackman/oatmeal#report-an-issue)
	+ [Development](https://github.com/dustinblackman/oatmeal#Development)
		- [Setup](https://github.com/dustinblackman/oatmeal#setup)
		- [Adding a backend](https://github.com/dustinblackman/oatmeal#adding-a-backend)
		- [Adding an editor](https://github.com/dustinblackman/oatmeal#adding-an-editor)
		- [Adding syntax highlighting for a language](https://github.com/dustinblackman/oatmeal#adding-syntax-highlighting-for-a-language)
* [FAQ](https://github.com/dustinblackman/oatmeal#faq)
	+ [Why Oatmeal?](https://github.com/dustinblackman/oatmeal#why-oatmeal)
* [License](https://github.com/dustinblackman/oatmeal#license)

#### Overview

Oatmeal is a terminal UI chat application that speaks with LLMs, complete with slash commands and fancy chat bubbles. It features agnostic backends to allow switching between the powerhouse of ChatGPT, or keeping things private with Ollama. While Oatmeal works great as a stand alone terminal application, it works even better paired with an editor like Neovim!

See it in action with Neovim (click to restart):

[![oatmeal-demo](https://private-user-images.githubusercontent.com/5246169/281238246-9ee5e910-4eff-4deb-8065-aeab8bfe6b00.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzgxOTUxMjksIm5iZiI6MTczODE5NDgyOSwicGF0aCI6Ii81MjQ2MTY5LzI4MTIzODI0Ni05ZWU1ZTkxMC00ZWZmLTRkZWItODA2NS1hZWFiOGJmZTZiMDAuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI1MDEyOSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTAxMjlUMjM1MzQ5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ODExNzQxYzRkMTgyZWQzOTRlYjAwMzVlNGRiZGU4MWEyY2MwZTQ1MTEyMDgyYzEzYzIyOGFiZjc3NmIyZDMyOSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.oxKmtYruN2h5a7PmaDfw00W36ewUspAanO_qEt124Wk)](https://private-user-images.githubusercontent.com/5246169/281238246-9ee5e910-4eff-4deb-8065-aeab8bfe6b00.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzgxOTUxMjksIm5iZiI6MTczODE5NDgyOSwicGF0aCI6Ii81MjQ2MTY5LzI4MTIzODI0Ni05ZWU1ZTkxMC00ZWZmLTRkZWItODA2NS1hZWFiOGJmZTZiMDAuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI1MDEyOSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTAxMjlUMjM1MzQ5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ODExNzQxYzRkMTgyZWQzOTRlYjAwMzVlNGRiZGU4MWEyY2MwZTQ1MTEyMDgyYzEzYzIyOGFiZjc3NmIyZDMyOSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.oxKmtYruN2h5a7PmaDfw00W36ewUspAanO_qEt124Wk)
  [![oatmeal-demo](https://private-user-images.githubusercontent.com/5246169/281238246-9ee5e910-4eff-4deb-8065-aeab8bfe6b00.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzgxOTUxMjksIm5iZiI6MTczODE5NDgyOSwicGF0aCI6Ii81MjQ2MTY5LzI4MTIzODI0Ni05ZWU1ZTkxMC00ZWZmLTRkZWItODA2NS1hZWFiOGJmZTZiMDAuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI1MDEyOSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTAxMjlUMjM1MzQ5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ODExNzQxYzRkMTgyZWQzOTRlYjAwMzVlNGRiZGU4MWEyY2MwZTQ1MTEyMDgyYzEzYzIyOGFiZjc3NmIyZDMyOSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.oxKmtYruN2h5a7PmaDfw00W36ewUspAanO_qEt124Wk)](https://private-user-images.githubusercontent.com/5246169/281238246-9ee5e910-4eff-4deb-8065-aeab8bfe6b00.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzgxOTUxMjksIm5iZiI6MTczODE5NDgyOSwicGF0aCI6Ii81MjQ2MTY5LzI4MTIzODI0Ni05ZWU1ZTkxMC00ZWZmLTRkZWItODA2NS1hZWFiOGJmZTZiMDAuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI1MDEyOSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTAxMjlUMjM1MzQ5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ODExNzQxYzRkMTgyZWQzOTRlYjAwMzVlNGRiZGU4MWEyY2MwZTQ1MTEyMDgyYzEzYzIyOGFiZjc3NmIyZDMyOSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.oxKmtYruN2h5a7PmaDfw00W36ewUspAanO_qEt124Wk)  

*Note:* This project is still quite new, and LLM's can return unexpected answers the UI isn't prepped for. There's likely a few bugs hidden somewhere.

#### Install

##### macOS

```
brew install dustinblackman/tap/oatmeal
```

##### Debian / Ubuntu

Note: This method may have outdated releases.

```
curl -s https://apt.dustinblackman.com/KEY.gpg | apt-key add -
curl -s https://apt.dustinblackman.com/dustinblackman.list > /etc/apt/sources.list.d/dustinblackman.list
sudo apt-get update
sudo apt-get install oatmeal
```

##### Fedora / CentOS

Note: This method may have outdated releases.

```
dnf config-manager --add-repo https://yum.dustinblackman.com/config.repo
dnf install oatmeal
```

##### Nix

```
nix-env -f '<nixpkgs>' -iA nur.repos.dustinblackman.oatmeal
```

##### Arch Linux

```
yay -S oatmeal-bin
```

##### Alpine Linux

```
arch=$(uname -a | grep -q aarch64 && echo 'arm64' || echo 'amd64')
curl -L -o oatmeal.apk "https://github.com/dustinblackman/oatmeal/releases/download/v0.13.0/oatmeal_0.13.0_linux_${arch}.apk"
apk add --allow-untrusted ./oatmeal.apk
```

##### Windows

**Chocolatey**

```
choco install oatmeal --version=0.13.0
```

**Scoop**

```
scoop bucket add dustinblackman https://github.com/dustinblackman/scoop-bucket.git
scoop install oatmeal
```

**Winget**

```
winget install -e --id dustinblackman.oatmeal
```

##### Cargo

```
cargo install oatmeal --locked
```

##### Docker

```
docker run --rm -it ghcr.io/dustinblackman/oatmeal:latest
```

##### Manual

Download the pre-compiled binaries and packages from the [releases page](https://github.com/dustinblackman/oatmeal/releases) and copy to the desired location.

##### Source

```
git clone https://github.com/dustinblackman/oatmeal.git
cd oatmeal
cargo build --release
mv ./target/release/oatmeal /usr/local/bin/
```

#### Usage

The following shows the available options to start a chat session. By default when running `oatmeal`, Ollama is the selected backend, and the `clipboard` integration for an editor. See `oatmeal --help`, `/help` in chat, or the output below to get all the details.

```
Terminal UI to chat with large language models (LLM) using different model backends, and direct integrations with your favourite editors!

Version: 0.13.0
Commit: v0.13.0

Usage: oatmeal [OPTIONS] [COMMAND]

Commands:
  chat         Start a new chat session.
  completions  Generates shell completions.
  config       Configuration file options.
  manpages     Generates manpages and outputs to stdout.
  sessions     Manage past chat sessions.
  help         Print this message or the help of the given subcommand(s)

Options:
  -b, --backend <backend>
          The initial backend hosting a model to connect to. [default: ollama] [env: OATMEAL_BACKEND=] [possible values: langchain, ollama, openai, claude, gemini]
      --backend-health-check-timeout <backend-health-check-timeout>
          Time to wait in milliseconds before timing out when doing a healthcheck for a backend. [default: 1000] [env: OATMEAL_BACKEND_HEALTH_CHECK_TIMEOUT=]
  -m, --model <model>
          The initial model on a backend to consume. Defaults to the first model available from the backend if not set. [env: OATMEAL_MODEL=]
  -c, --config-file <config-file>
          Path to configuration file [default: ~/.config/oatmeal/config.toml] [env: OATMEAL_CONFIG_FILE=]
  -e, --editor <editor>
          The editor to integrate with. [default: clipboard] [env: OATMEAL_EDITOR=] [possible values: neovim, clipboard, none]
  -t, --theme <theme>
          Sets code syntax highlighting theme. [default: base16-onedark] [env: OATMEAL_THEME=] [possible values: base16-github, base16-monokai, base16-one-light, base16-onedark, base16-seti]
      --theme-file <theme-file>
          Absolute path to a TextMate tmTheme to use for code syntax highlighting. [env: OATMEAL_THEME_FILE=]
      --lang-chain-url <lang-chain-url>
          LangChain Serve API URL when using the LangChain backend. [default: http://localhost:8000] [env: OATMEAL_LANGCHAIN_URL=]
      --ollama-url <ollama-url>
          Ollama API URL when using the Ollama backend. [default: http://localhost:11434] [env: OATMEAL_OLLAMA_URL=]
      --open-ai-url <open-ai-url>
          OpenAI API URL when using the OpenAI backend. Can be swapped to a compatible proxy. [default: https://api.openai.com] [env: OATMEAL_OPENAI_URL=]
      --open-ai-token <open-ai-token>
          OpenAI API token when using the OpenAI backend. [env: OATMEAL_OPENAI_TOKEN=]
      --claude-token <claude-token>
          Anthropic's Claude API token when using the Claude backend. [env: OATMEAL_CLAUDE_TOKEN=]
      --gemini-token <gemini-token>
          Google Gemini API token when using the Gemini backend. [env: OATMEAL_GEMINI_TOKEN=]
  -h, --help
          Print help
  -V, --version
          Print version

CHAT COMMANDS:
  - /modellist (/ml) - Lists all available models from the backend.
  - /model (/model) [MODEL_NAME,MODEL_INDEX] - Sets the specified model as the active model. You can pass either the model name, or the index from `/modellist`.
  - /append (/a) [CODE_BLOCK_NUMBER?] - Appends code blocks to an editor. See Code Actions for more details.
  - /replace (/r) [CODE_BLOCK_NUMBER?] - Replaces selections with code blocks in an editor. See Code Actions for more details.
  - /copy (/c) [CODE_BLOCK_NUMBER?] - Copies the entire chat history to your clipboard. When a `CODE_BLOCK_NUMBER` is used, only the specified copy blocks are copied to clipboard. See Code Actions for more details.
  - /quit /exit (/q) - Exit Oatmeal.
  - /help (/h) - Provides this help menu.

CHAT HOTKEYS:
  - Up arrow - Scroll up.
  - Down arrow - Scroll down.
  - CTRL+U - Page up.
  - CTRL+D - Page down.
  - CTRL+C - Interrupt waiting for prompt response if in progress, otherwise exit.
  - CTRL+O - Insert a line break at the cursor position.
  - CTRL+R - Resubmit your last message to the backend.

CHAT CODE ACTIONS:
When working with models that provide code, and using an editor integration, Oatmeal has the capabilities to read selected code from an editor, and submit model provided code back in to an editor. Each code block provided by a model is indexed with a (NUMBER) at the beginning of the block to make it easily identifiable.

  - /append (/a) [CODE_BLOCK_NUMBER?] will append one-to-many model provided code blocks to the open file in your editor.
  - /replace (/r) [CODE_BLOCK_NUMBER?] - will replace selected code in your editor with one-to-many model provided code blocks.
  - /copy (/c) [CODE_BLOCK_NUMBER?] - Copies the entire chat history to your clipboard. When a `CODE_BLOCK_NUMBER` is used it will append one-to-many model provided code blocks to your clipboard, no matter the editor integration.

The `CODE_BLOCK_NUMBER` allows you to select several code blocks to send back to your editor at once. The parameter can be set as follows:
  - `1` - Selects the first code block
  - `1,3,5` - Selects code blocks 1, 3, and 5.
  - `2..5`- Selects an inclusive range of code blocks between 2 and 5.
  - None - Selects the last provided code block.

```

##### Configuration

On top of being configurable with command flags and environment variables, Oatmeal is also manageable with a configuration file such as [this example](https://github.com/dustinblackman/oatmeal/blob/main/config.example.toml). You can run `oatmeal config create` to initialize for the first time.

```
Configuration file options.

Usage: oatmeal config [OPTIONS] [COMMAND]

Commands:
  create   Saves the default config file to the configuration file path. This command will fail if the file exists already.
  default  Outputs the default configuration file to stdout.
  path     Returns the default path for the configuration file.
  help     Print this message or the help of the given subcommand(s)

```

##### Backends

The following model backends are supported:

* [OpenAI](https://chat.openai.com) (Or any compatible proxy/API)
* [Ollama](https://github.com/jmorganca/ollama)
* [LangChain/LangServe](https://python.langchain.com/docs/langserve) (Experimental)
* [Claude](https://claude.ai) (Experimental)
* [Gemini](https://gemini.google.com) (Experimental)

##### Editors

The following editors are currently supported. The `clipboard` editor is a special case where any copy or accept commands are simply copied to your clipboard. This is the default behaviour. Hit any of the links below for more details on how to use!

* Clipboard (Default)
* None (Disables all editor functionality)
* [Neovim](https://github.com/dustinblackman/oatmeal.nvim)

##### Themes

A handful of themes are embedded in the application for code syntax highlighting, defaulting to [OneDark](https://github.com/atom/one-dark-ui). If none suits your needs, Oatmeal supports any Sublime Text/Text Mate `.tmTheme` file with the `theme-file` configuration option. [base16-textmate](https://github.com/chriskempson/base16-textmate) has plenty to pick from!

##### Sessions

Oatmeal persists all chat sessions with your models, allowing you to go back and review an old conversation, or pick up from where you left off!

```
Manage past chat sessions.

Usage: oatmeal sessions [OPTIONS] [COMMAND]

Commands:
  dir     Print the sessions cache directory path.
  list    List all previous sessions with their ids and models.
  open    Open a previous session by ID. Omit passing any session ID to load an interactive selection.
  delete  Delete one or all sessions.
  help    Print this message or the help of the given subcommand(s)

```

Grepping through previous sessions isn't something built in to Oatmeal *(yet)*. This bash function can get you there nicely using [Ripgrep](https://github.com/BurntSushi/ripgrep) and [FZF](https://github.com/junegunn/fzf).

```
function oatmeal-sessions() {
    (
        cd "$(oatmeal sessions dir)"
        id=$(rg --color always -n . | fzf --ansi | awk -F ':' '{print $1}' | head -n1 | awk -F '.' '{print $1}')
        oatmeal sessions open --id "$id"
    )
}
```

Or something a little more in depth (while hacky) that additionally uses [yq](https://github.com/mikefarah/yq) and [jq](https://github.com/jqlang/jq).

```
function oatmeal-sessions() {
    (
        cd "$(oatmeal sessions dir)"
        id=$(
          ls | \
          (while read f; do echo "$(cat $f)\n---\n"; done;) | \
          yq -p=yaml -o=json - 2> /dev/null | \
          jq -s . | \
          jq -rc '. |= sort_by(.timestamp) | .[] |  "\(.id):\(.timestamp):\(.state.backend_model):\(.state.editor_language):\(.state.messages[] | .text | tojson)"' | \
          fzf --ansi | \
          awk -F ':' '{print $1}' | \
          head -n1 | \
          awk -F '.' '{print $1}'
        )
        oatmeal sessions open --id "$id"
    )
}
```

#### Contributing

##### Report an issue

On each Oatmeal release there is a separate download to help in reporting issues to really drill down in to what the problem is! If you've run in to a problem, I'd really help appreciate solving it.

1. Head over to [releases](https://github.com/dustinblackman/oatmeal/releases) and download the DEBUG package for the latest release of Oatmeal.
2. Extract the contents of the archive, and `cd` in your terminal inside the archive.
3. Run your command with the arguments provided in the error message prefixing with `RUST_BACKTRACE=1 ./oatmeal **ARGS-HERE**`
4. Copy/paste the output and [open an issue](https://github.com/dustinblackman/oatmeal/issues/new). Include any screenshots you believe will be helpful!

##### Development

###### Setup

[![Open in DevPod!](https://github.com/dustinblackman/oatmeal/raw/main/.github/devpod.svg)](https://devpod.sh/open#https://github.com/dustinblackman/oatmeal)
Oatmeal comes with a ready made DevContainer with all the magic needed to work on the project. However if you wish to develop fully local, the following will get you set up with all the necessary tooling.

```
cargo install cargo-run-bin
git clone https://github.com/dustinblackman/oatmeal.git
cd oatmeal
cargo cmd setup
```

###### Adding a backend

Each backend implements the [Backend trait](https://github.com/dustinblackman/oatmeal/blob/main/src/domain/models/backend.rs) in its own infrastructure file. The trait has documentation on what is expected of each method. You can checkout [Ollama](https://github.com/dustinblackman/oatmeal/blob/main/src/infrastructure/backends/ollama.rs) as an example.

The following steps should be completed to add a backend:

1. Implement trait for new backend.
2. Update the [BackendName](https://github.com/dustinblackman/oatmeal/blob/main/src/domain/models/backend.rs) enum with your new Backend name.
3. Update the [BackendManager](https://github.com/dustinblackman/oatmeal/blob/main/src/infrastructure/backends/mod.rs) to provide your new backend.
4. Write tests

###### Adding an editor

Each editor implements the [Editor trait](https://github.com/dustinblackman/oatmeal/blob/main/src/domain/models/editor.rs) in its own infrastructure file. The trait has documentation on what is expected of each method. You can checkout [Neovim](https://github.com/dustinblackman/oatmeal/blob/main/src/infrastructure/editors/neovim.rs) as an example.

The following steps should be completed to add an editor:

1. Implement trait for new editor.
2. Update the [EditorName](https://github.com/dustinblackman/oatmeal/blob/main/src/domain/models/editor.rs) enum with your new Editor name.
3. Update the [EditorManager](https://github.com/dustinblackman/oatmeal/blob/main/src/infrastructure/editors/mod.rs) to provide your new editor.
4. Write tests

###### Adding syntax highlighting for a language

Syntax highlighting language selection is a tad manual where several languages must be curated and then added to [`assets.toml`](https://github.com/dustinblackman/oatmeal/blob/main/assets.toml).

1. Google to find a `.sublime-syntax` project on GitHub for your language. [bat](https://github.com/sharkdp/bat/tree/master/assets/syntaxes/02_Extra) has many!
2. Update [`assets.toml`](https://github.com/dustinblackman/oatmeal/blob/main/assets.toml) to include the new repo. Make sure to include the license in the files array. You can leave `nix-hash` as an empty string, and it'll be updated by a maintainer later. Or if you have docker installed, you can run `cargo xtask hash-assets`.
3. `rm -rf .caches && cargo build`
4. Test to see highlighting works.

#### FAQ

##### Why Oatmeal?

I was eating a bowl of oatmeal when I wrote the first commit 🤷. (They don't let me name things at work anymore...)

#### License

[MIT](https://github.com/dustinblackman/oatmeal/blob/main/LICENSE)
