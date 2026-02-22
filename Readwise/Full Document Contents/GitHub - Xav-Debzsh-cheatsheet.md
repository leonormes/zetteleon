# GitHub - Xav-Deb/zsh-cheatsheet

![rw-book-cover](https://opengraph.githubassets.com/3d5b5bc61ad176ae18e18d5faabcd5a133ddffea83bb550229d9222db6c2b3e8/Xav-Deb/zsh-cheatsheet)

## Metadata
- Author: [[https://github.com/Xav-Deb/]]
- Full Title: GitHub - Xav-Deb/zsh-cheatsheet
- Category: #articles
- Summary: zsh-cheatsheet is a lightweight Zsh plugin that shows interactive cheat sheets in your terminal using fzf. It detects the command you type and opens its documentation instantly with a simple key press. The plugin is fast, easy to install, and supports searching, auto-insertion, and updating cheat sheets.
- URL: https://github.com/Xav-Deb/zsh-cheatsheet

## Full Document
### Xav-Deb/zsh-cheatsheet

main

Go to file

Code

Open more actions menu

### 🚀 Zsh Cheatsheet

[![License: MIT](https://camo.githubusercontent.com/fdf2982b9f5d7489dcf44570e714e3a15fce6253e0cc6b5aa61a075aac2ff71b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d79656c6c6f772e737667)](https://opensource.org/licenses/MIT)
[![Zsh Version](https://camo.githubusercontent.com/39c16edfba08607620a3e5b1ef6e2d71acc920651a32cfecad1395f057919a43/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5a73682d352e382532422d626c75652e737667)](https://www.zsh.org/)
[![fzf](https://camo.githubusercontent.com/5733a5ba820a27be4a1e1976bbf11e53a8ead9b7cd567c80f2aa757cd4dcf3a9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446570656e64656e63792d667a662d6f72616e67652e737667)](https://github.com/junegunn/fzf)
**zsh-cheatsheet** is a lightweight Zsh plugin that provides context-aware interactive cheat sheets directly in your terminal. Using ZLE (Zsh Line Editor) and `fzf`, it gives you instant access to your command documentation without leaving the command line.

#### 🛠️ Technology Stack

* **Language**: [Zsh](https://www.zsh.org/) (Version 5.8 or higher required).
* **Fuzzy Finder**: [fzf](https://github.com/junegunn/fzf).
* **Database**: Markdown (`.md`) files parsed on-the-fly.
* **Integration**: Zsh Line Editor (ZLE) for native command buffer interaction.

#### 🏗️ Project Architecture

The project follows a simple and high-performance architecture, prioritizing Zsh internal mechanisms:

* **ZLE Integration**: The plugin registers a `zsh-cheatsheet-open` widget that interacts directly with `$BUFFER` and `$LBUFFER`.
* **Markdown-as-Database**: Cheat sheets are stored in the `cheats/` directory. Each file follows a strict formatting contract for ultra-fast parsing without heavy external tools.
* **Autoloadable Functions**: Business logic is decoupled into autoloadable functions in `functions/`, ensuring minimal shell startup time.
* **Context Awareness**: The plugin automatically detects the command being typed to open the relevant documentation directly.

#### 🚀 Getting Started

##### Prerequisites

* **Zsh (5.8+)**
* **fzf** installed and available in your `$PATH`.

##### Installation

###### Via Oh-My-Zsh

1. Clone the repository into your custom plugins folder:

 
```
git clone https://github.com/Xav-Deb/zsh-cheatsheet.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-cheatsheet
```
2. Add `zsh-cheatsheet` to your plugins list in `~/.zshrc`:

 
```
plugins=(... zsh-cheatsheet)
```
3. Reload your configuration:

 
```
source ~/.zshrc
```

###### Manual Installation

1. Clone the repository:

 
```
git clone https://github.com/Xav-Deb/zsh-cheatsheet.git ~/.zsh-cheatsheet
```
2. Source the plugin in your `~/.zshrc`:

 
```
echo "source ~/.zsh-cheatsheet/zsh-cheatsheet.plugin.zsh" >> ~/.zshrc
```

#### ⚙️ Usage

##### Basic Interaction

1. **Context-Aware Search**: Type a command (e.g., `git`) and press `Ctrl+H` (default). The plugin will detect the command and open the specific cheat sheet for `git`.

 
```
git <Ctrl+H>
```
2. **Global Search**: If the command line is empty or the command is not recognized, pressing `Ctrl+H` will open a searchable list of all available cheat sheets.
3. **Navigation (fzf)**:

	* Type to filter entries.
	* Use `Up`/`Down` arrows or `Ctrl+K`/`Ctrl+J` to navigate results.
	* Press `Enter` to select a command. The command will be **inserted under your cursor** in the terminal, ready to be edited or executed.
	* Press `Esc` or `Ctrl+C` to close without inserting anything.

##### Customizing Keybinding

The default keybinding is `^H` (Ctrl+H). To change it, define `ZSH_CHEATSHEET_BIND` **before** loading the plugin (or before `source ~/.zshrc` if using Oh-My-Zsh plugins) in your `.zshrc`:

```
# Example: bind to Ctrl+O
export ZSH_CHEATSHEET_BIND='^O'

plugins=(... zsh-cheatsheet)
```

##### Management Commands

* **Reload**: If you modify a cheat sheet file manually, reload the plugin without restarting your shell:

 
```
zsh-cheatsheet reload
```
* **Update**: Fetch the latest cheat sheets (if configured with remote source) and plugin updates:

 
```
zsh-cheatsheet update   # Update database
zsh-cheatsheet upgrade  # Update plugin code
source ~/.zshrc         # Reload configuration to apply all changes
```

##### 📸 Screenshots

[![Context Aware Search](https://github.com/Xav-Deb/zsh-cheatsheet/raw/main/docs/img/screenshot-context.png)](https://github.com/Xav-Deb/zsh-cheatsheet/blob/main/docs/img/screenshot-context.png)
*1. Type a command (e.g., `git`) to set the context.*

[![FZF Interface](https://github.com/Xav-Deb/zsh-cheatsheet/raw/main/docs/img/screenshot-fzf.png)](https://github.com/Xav-Deb/zsh-cheatsheet/blob/main/docs/img/screenshot-fzf.png)
*2. Press `Ctrl+H` to open the interactive cheat sheet, filter with fzf, and press Enter to insert.*

#### 📂 Project Structure

* `zsh-cheatsheet.plugin.zsh`: Main entry point (loading, keybindings).
* `functions/`: Core logic for functions (`open`, `update`, `upgrade`).
* `cheats/`: Markdown "database" of cheat sheets.
* `test/`: Testing scripts and content validation.

#### ✨ Key Features

* 🏎️ **Speed**: Pure Zsh parsing; avoids heavy dependencies like grep, sed, or awk.
* 🧠 **Contextual**: Typing `git` then the hotkey automatically opens `git.md`.
* 🔍 **Fuzzy Search**: Powered by `fzf` with category filtering based on H2 headers.
* ⌨️ **Auto-Insertion**: The selected command is inserted directly at the cursor position.
* 🔄 **Auto-Update**: Built-in commands to update the database and the plugin itself.

#### 🚦 Development Workflow

Development follows iterative steps defined in the project plan:

1. Skeleton definition and widget registration.
2. Context detection implementation.
3. `fzf` integration.
4. Markdown parsing according to the contract.
5. Command insertion logic.
6. Fallback for global selection.

Every new feature must be validated by the scripts in `test/`.

#### 📏 Coding Standards

* **Prefer Zsh Builtins**: Use parameter expansion and internal pattern matching instead of external system calls.
* **Portability**: Ensure support for both macOS and Linux (GNU/BSD compatibility).
* **Buffer Safety**: Never clear the user's buffer without explicit action.
* **Markdown Contract**:
	+ Exactly one `# <cmd>` header at the top.
	+ `## <Category>` sections for visual grouping.
	+ Entries formatted as `- \`command` — description`.

#### 🧪 Testing

The project includes an automated test suite to ensure stability:

* **Syntax Check**: `zsh -n` on all scripts.
* **Content Validation**: Ensures all files in `cheats/` follow the Markdown contract.

Run all tests with:

```
./test/run.sh
```

#### 🤝 Contributing

Contributions are welcome! To add or modify a cheat sheet:

1. Review the [Coding Standards](https://github.com/Xav-Deb/zsh-cheatsheet/#-coding-standards) section to understand the Markdown contract.
2. Add your file to the `cheats/` directory.
3. Validate with `./test/run.sh`.
4. Open a Pull Request.

#### ⭐ Star History

#### Star History

[![Star History Chart](https://camo.githubusercontent.com/ba5d0fc1950d94f250c1a02a3a520be63bdc665df1e8102f9d37eb0a4378787f/68747470733a2f2f6170692e737461722d686973746f72792e636f6d2f7376673f7265706f733d5861762d4465622f7a73682d6368656174736865657426747970653d64617465266c6567656e643d746f702d6c656674)](https://www.star-history.com/#Xav-Deb/zsh-cheatsheet&type=date&legend=top-left)
#### 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

*Built with ❤️ for the Zsh community.*
