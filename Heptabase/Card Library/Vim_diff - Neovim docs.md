# Vim_diff - Neovim docs

Differences between Nvim and Vim

Nvim differs from Vim in many ways, although editor and Vimscript (not Vim9script) features are mostly identical. This document is a complete and centralized reference of the differences.

## Configuration [nvim-config](#nvim-config)



User configuration and data files are found in standard [base-directories](https://neovim.io/doc/user/starting.html#base-directories) (see also [$NVIM_APPNAME](https://neovim.io/doc/user/starting.html#%24NVIM_APPNAME)). Note in particular:

Use `$XDG_CONFIG_HOME/nvim/init.vim` instead of `.vimrc` for your [config](https://neovim.io/doc/user/starting.html#config).

Use `$XDG_CONFIG_HOME/nvim` instead of `.vim` to store configuration files.

Use `$XDG_STATE_HOME/nvim/shada/main.shada` instead of `.viminfo` for persistent session information. [shada](https://neovim.io/doc/user/starting.html#shada)



Defaults [nvim-defaults](#nvim-defaults)



Filetype detection is enabled by default. This can be disabled by adding ":filetype off" to [init.vim](https://neovim.io/doc/user/starting.html#init.vim).

Syntax highlighting is enabled by default. This can be disabled by adding ":syntax off" to [init.vim](https://neovim.io/doc/user/starting.html#init.vim).

Default color scheme has been updated. This can result in color schemes looking differently due to them relying on how highlight groups are defined by default. Add ":colorscheme vim" to [init.vim](https://neovim.io/doc/user/starting.html#init.vim) or ":source $VIMRUNTIME/colors/vim.lua" to your color scheme file to restore the old default links and colors.

['autoread'](https://neovim.io/doc/user/options.html#'autoread') is enabled (works in all UIs, including terminal)

['background'](https://neovim.io/doc/user/options.html#'background') defaults to "dark" (unless set automatically by the terminal/UI)

['backupdir'](https://neovim.io/doc/user/options.html#'backupdir') defaults to .,\~/.local/state/nvim/backup// ([xdg](https://neovim.io/doc/user/starting.html#xdg)), auto-created

['define'](https://neovim.io/doc/user/options.html#'define') defaults to "". The C ftplugin sets it to "^\\\\s\*#\\\\s\*define"

['directory'](https://neovim.io/doc/user/options.html#'directory') defaults to \~/.local/state/nvim/swap// ([xdg](https://neovim.io/doc/user/starting.html#xdg)), auto-created

['fillchars'](https://neovim.io/doc/user/options.html#'fillchars') defaults (in effect) to "vert:│,fold:·,foldsep:│"

['grepprg'](https://neovim.io/doc/user/options.html#'grepprg') uses the -H and -I flags for regular grep, and defaults to using ripgrep if available

['history'](https://neovim.io/doc/user/options.html#'history') defaults to 10000 (the maximum)

['include'](https://neovim.io/doc/user/options.html#'include') defaults to "". The C ftplugin sets it to "^\\\\s\*#\\\\s\*include"

['isfname'](https://neovim.io/doc/user/options.html#'isfname') does not include ":" (on Windows). Drive letters are handled correctly without it. (Use [gF](https://neovim.io/doc/user/editing.html#gF) for filepaths suffixed with ":line:col").

['laststatus'](https://neovim.io/doc/user/options.html#'laststatus') defaults to 2 (statusline is always shown)

['listchars'](https://neovim.io/doc/user/options.html#'listchars') defaults to "tab:> ,trail:-,nbsp:+"

['path'](https://neovim.io/doc/user/options.html#'path') defaults to ".,,". The C ftplugin adds "/usr/include" if it exists.

['tags'](https://neovim.io/doc/user/options.html#'tags') defaults to "./tags;,tags"

['termguicolors'](https://neovim.io/doc/user/options.html#'termguicolors') is enabled by default if Nvim can detect support from the host terminal

['undodir'](https://neovim.io/doc/user/options.html#'undodir') defaults to \~/.local/state/nvim/undo// ([xdg](https://neovim.io/doc/user/starting.html#xdg)), auto-created

['viewoptions'](https://neovim.io/doc/user/options.html#'viewoptions') includes "unix,slash", excludes "options"

[editorconfig](https://neovim.io/doc/user/editorconfig.html#editorconfig) plugin is enabled, .editorconfig settings are applied.

[man.lua](https://neovim.io/doc/user/filetype.html#man.lua) plugin is enabled, so [:Man](https://neovim.io/doc/user/filetype.html#%3AMan) is available by default.

matchit plugin is enabled. To disable it in your config:

```
:let loaded_matchit = 1
```

[g:vimsyn_embed](https://neovim.io/doc/user/syntax.html#g%3Avimsyn_embed) defaults to "l" to enable Lua highlighting

### DEFAULT MOUSE

`[default-mouse](#default-mouse)` `[disable-mouse](#disable-mouse)` By default the mouse is enabled. This means [scroll-mouse-wheel](https://neovim.io/doc/user/scroll.html#scroll-mouse-wheel) will scroll the window instead of moving the cursor; `<LeftMouse>` click places the cursor; and `<RightMouse>` click opens the default [popup-menu](https://neovim.io/doc/user/gui.html#popup-menu) with standard actions.

Mouse is NOT enabled in [Cmdline-mode](https://neovim.io/doc/user/cmdline.html#Cmdline-mode) or the [more-prompt](https://neovim.io/doc/user/message.html#more-prompt), so you can temporarily disable it just by typing ":". Or if you want to partially or fully disable the mouse or popup-menu, do any of the following:

Disable mouse completely by unsetting the ['mouse'](https://neovim.io/doc/user/options.html#'mouse') option:

```
set mouse=
```

Change the ['mousemodel'](https://neovim.io/doc/user/options.html#'mousemodel'), so `<RightMouse>` extends selection instead of showing the popup-menu:

```
set mousemodel=extend
```

Map `<A-LeftMouse>` so that it temporarily disables mouse until the cursor moves:

```
nnoremap <A-LeftMouse> <Cmd>
  \ set mouse=<Bar>
  \ echo 'mouse OFF until next cursor-move'<Bar>
  \ autocmd CursorMoved * ++once set mouse&<Bar>
  \ echo 'mouse ON'<CR>
```

To remove the default popup-menu without disabling mouse:

```
aunmenu PopUp
autocmd! nvim_popupmenu
```

To remove only the "How-to disable mouse" menu item (and its separator):

```
aunmenu PopUp.How-to\ disable\ mouse
aunmenu PopUp.-2-
```

### DEFAULT MAPPINGS

`[default-mappings](#default-mappings)` Nvim creates the following default mappings at [startup](https://neovim.io/doc/user/starting.html#startup). You can disable any of these in your config by simply removing the mapping, e.g. ":unmap Y".

### DEFAULT AUTOCOMMANDS

`[default-autocmds](#default-autocmds)` Default autocommands exist in the following groups. Use ":autocmd! `{group}`" to remove them and ":autocmd `{group}`" to see how they're defined.

nvim_terminal:

TermClose: A [terminal](https://neovim.io/doc/user/terminal.html#terminal) buffer started with no arguments (which thus uses ['shell'](https://neovim.io/doc/user/options.html#'shell')) and which exits with no error is closed automatically.

TermRequest: The terminal emulator responds to OSC background and foreground requests, indicating (1) a black background and white foreground when Nvim option ['background'](https://neovim.io/doc/user/options.html#'background') is "dark" or (2) a white background and black foreground when ['background'](https://neovim.io/doc/user/options.html#'background') is "light". While this may not reflect the actual foreground/background color, it permits ['background'](https://neovim.io/doc/user/options.html#'background') to be retained for a nested Nvim instance running in the terminal emulator.

TermOpen: Sets default options for [terminal](https://neovim.io/doc/user/terminal.html#terminal) buffers:

nvim_cmdwin:

CmdwinEnter: Limits syntax sync to maxlines=1 in the [cmdwin](https://neovim.io/doc/user/cmdline.html#cmdwin).

nvim_swapfile:

SwapExists: Skips the swapfile prompt (sets [v:swapchoice](https://neovim.io/doc/user/vvars.html#v%3Aswapchoice) to "e") when the swapfile is owned by a running Nvim process. Shows [W325](https://neovim.io/doc/user/recover.html#W325) "Ignoring swapfile…" message.



New Features [nvim-features](#nvim-features)

MAJOR COMPONENTS

LSP framework [lsp](https://neovim.io/doc/user/lsp.html#lsp)

Lua scripting [lua](https://neovim.io/doc/user/lua.html#lua)

Providers

XDG base directories [xdg](https://neovim.io/doc/user/starting.html#xdg)

### USER EXPERIENCE



Working intuitively and consistently is a major goal of Nvim.

`[feature-compile](#feature-compile)`

Nvim always includes ALL features, in contrast to Vim (which ships various combinations of 100+ optional features). [feature-compile](https://neovim.io/doc/user/vim_diff.html#feature-compile) Think of it as a leaner version of Vim's "HUGE" build. This reduces surface area for bugs, and removes a common source of confusion and friction for users.

Nvim avoids features that cannot be provided on all platforms; instead that is delegated to external plugins/extensions. E.g. the `-X` platform-specific option is "sometimes" available in Vim (with potential surprises: <https://stackoverflow.com/q/14635295>).

Vim's internal test functions (test_autochdir(), test_settime(), etc.) are not exposed (nor implemented); instead Nvim has a robust API.

Behaviors, options, documentation are removed if they cost users more time than they save.

Usability details have been improved where the benefit outweighs any backwards-compatibility cost. Some examples:

Terminal features such as ['guicursor'](https://neovim.io/doc/user/options.html#'guicursor') are enabled where possible.

Some features are built in that otherwise required external plugins:



### ARCHITECTURE



The Nvim UI is "decoupled" from the core editor: all UIs, including the builtin [TUI](https://neovim.io/doc/user/tui.html#TUI) are just plugins that connect to a Nvim server (via [\--server](https://neovim.io/doc/user/remote.html#--server) or [\--embed](https://neovim.io/doc/user/starting.html#--embed)). Multiple Nvim UI clients can connect to the same Nvim editor server.

External plugins run in separate processes. [remote-plugin](https://neovim.io/doc/user/remote_plugin.html#remote-plugin) This improves stability and allows those plugins to work without blocking the editor. Even "legacy" Python and Ruby plugins which use the old Vim interfaces ([if_pyth](https://neovim.io/doc/user/if_pyth.html#if_pyth), [if_ruby](https://neovim.io/doc/user/if_ruby.html#if_ruby)) run out-of-process, so they cannot crash Nvim.

Platform and I/O facilities are built upon libuv. Nvim benefits from libuv features and bug fixes, and other projects benefit from improvements to libuv by Nvim developers.



### Features



Command-line:

(Experimental) `[g:Nvim_color_cmdline](#g%3ANvim_color_cmdline)` Command-line ([:](https://neovim.io/doc/user/cmdline.html#%3A)) is colored by callback defined in `g:Nvim_color_cmdline` (this callback is for testing only, and will be removed in the future).

Commands:

[:drop](https://neovim.io/doc/user/windows.html#%3Adrop) is always available

[:Man](https://neovim.io/doc/user/filetype.html#%3AMan) is available by default, with many improvements such as completion

[:match](https://neovim.io/doc/user/pattern.html#%3Amatch) can be invoked before highlight group is defined

[:source](https://neovim.io/doc/user/repeat.html#%3Asource) works with Lua User commands can support [:command-preview](https://neovim.io/doc/user/map.html#%3Acommand-preview) to show results as you type

[:write](https://neovim.io/doc/user/editing.html#%3Awrite) with "++p" flag creates parent directories.

Functions:

[matchadd()](https://neovim.io/doc/user/builtin.html#matchadd\\(\\)) can be called before highlight group is defined

[writefile()](https://neovim.io/doc/user/builtin.html#writefile\\(\\)) with "p" flag creates parent directories.

Highlight groups:

[hl-MsgArea](https://neovim.io/doc/user/syntax.html#hl-MsgArea) highlights messages/cmdline area

Input/Mappings:

ALT ([META](https://neovim.io/doc/user/intro.html#META)) chords always work (even in the [TUI](https://neovim.io/doc/user/tui.html#TUI)). Map [<M-](https://neovim.io/doc/user/intro.html#%3CM-) with any key: `<M-1>`, `<M-BS>`, `<M-Del>`, `<M-Ins>`, `<M-/>`, `<M-\>`, `<M-Space>`, `<M-Enter>`, etc.

Case-sensitive: `<M-a>` and `<M-A>` are two different keycodes.

Normal commands:

[gO](https://neovim.io/doc/user/various.html#gO) shows a filetype-defined "outline" of the current buffer.

[Q](https://neovim.io/doc/user/repeat.html#Q) replays the last recorded macro instead of switching to Ex mode ([gQ](https://neovim.io/doc/user/intro.html#gQ)).

Options:

Local values for global-local number/boolean options are unset when the option is set without a scope (e.g. by using [:set](https://neovim.io/doc/user/options.html#%3Aset)), similarly to how global-local string options work.

['autoread'](https://neovim.io/doc/user/options.html#'autoread') works in the terminal (if it supports "focus" events)

['exrc'](https://neovim.io/doc/user/options.html#'exrc') searches for ".nvim.lua", ".nvimrc", or ".exrc" files. The user is prompted whether to trust the file.

['fillchars'](https://neovim.io/doc/user/options.html#'fillchars') flags: "msgsep", "horiz", "horizup", "horizdown", "vertleft", "vertright", "verthoriz"

['foldcolumn'](https://neovim.io/doc/user/options.html#'foldcolumn') supports up to 9 dynamic/fixed columns

"view" tries to restore [mark-view](https://neovim.io/doc/user/motion.html#mark-view) when moving through the jumplist.

"clean" removes unloaded buffers from the jumplist.

['mousescroll'](https://neovim.io/doc/user/options.html#'mousescroll') amount to scroll by when scrolling with a mouse

"F" flag does not affect output from autocommands.

"q" flag fully hides macro recording message.

['signcolumn'](https://neovim.io/doc/user/options.html#'signcolumn') supports up to 9 dynamic/fixed columns

['tabline'](https://neovim.io/doc/user/options.html#'tabline') middle-click on tabpage label closes tabpage, and %@Func@foo%X can call any function on mouse-click

Shell:

Shell output ([:!](https://neovim.io/doc/user/various.html#%3A%21), [:make](https://neovim.io/doc/user/quickfix.html#%3Amake), …) is always routed through the UI, so it cannot "mess up" the screen. (You can still use "chansend(v:stderr,…)" if you want to mess up the screen :)

Nvim throttles (skips) messages from shell commands ([:!](https://neovim.io/doc/user/various.html#%3A%21), [:grep](https://neovim.io/doc/user/quickfix.html#%3Agrep), [:make](https://neovim.io/doc/user/quickfix.html#%3Amake)) if there is too much output. No data is lost, this only affects display and improves performance. [:terminal](https://neovim.io/doc/user/various.html#%3Aterminal) output is never throttled.

[:!](https://neovim.io/doc/user/various.html#%3A%21) does not support "interactive" commands. Use [:terminal](https://neovim.io/doc/user/various.html#%3Aterminal) instead. (GUI Vim has a similar limitation, see ":help gui-pty" in Vim.)

:!start is not special-cased on Windows.

[system()](https://neovim.io/doc/user/builtin.html#system\\(\\)) does not support writing/reading "backgrounded" commands. [E5677](https://neovim.io/doc/user/builtin.html#E5677)

Signs:

Signs are removed if the associated line is deleted.

Signs placed twice with the same identifier in the same group are moved.

Startup:

[\-e](https://neovim.io/doc/user/starting.html#-e) and [\-es](https://neovim.io/doc/user/starting.html#-es) invoke the same "improved Ex mode" as -E and -Es.

[\-E](https://neovim.io/doc/user/starting.html#-E) and [\-Es](https://neovim.io/doc/user/starting.html#-Es) read stdin as text (into buffer 1).

[\-es](https://neovim.io/doc/user/starting.html#-es) and [\-Es](https://neovim.io/doc/user/starting.html#-Es) have improved behavior:

Quits automatically, don't need "-c qa!".

Skips swap-file dialog.

[\-s](https://neovim.io/doc/user/starting.html#-s) reads Normal commands from stdin if the script name is "-".

Reading text (instead of commands) from stdin [\--](https://neovim.io/doc/user/starting.html#--):

works by default: "-" file is optional

works in more cases: [\-Es](https://neovim.io/doc/user/starting.html#-Es), file args

TUI: `[:set-termcap](#%3Aset-termcap)`

Start Nvim with ['verbose'](https://neovim.io/doc/user/options.html#'verbose') level 3 to show terminal capabilities:

```
nvim -V3
```

`['term'](#'term')` `[E529](#E529)` `[E530](#E530)` `[E531](#E531)`

['term'](https://neovim.io/doc/user/vim_diff.html#'term') reflects the terminal type derived from [$TERM](https://neovim.io/doc/user/tui.html#%24TERM) and other environment checks. For debugging only; not reliable during startup.

```
:echo &term
```

"builtin_x" means one of the [builtin-terms](https://neovim.io/doc/user/tui.html#builtin-terms) was chosen, because the expected terminfo file was not found on the system.

Nvim will use 256-colour capability on Linux virtual terminals. Vim uses only 8 colours plus bright foreground on Linux VTs.

Vim combines what is in its [builtin-terms](https://neovim.io/doc/user/tui.html#builtin-terms) with what it reads from terminfo, and has a ['ttybuiltin'](https://neovim.io/doc/user/vim_diff.html#'ttybuiltin') setting to control how that combination works. Nvim uses one or the other, it does not attempt to merge the two.

UI/Display:

messages: When showing messages longer than ['cmdheight'](https://neovim.io/doc/user/options.html#'cmdheight'), only scroll the message lines, not the entire screen. The separator line is decorated by [hl-MsgSeparator](https://neovim.io/doc/user/syntax.html#hl-MsgSeparator) and the "msgsep" flag of ['fillchars'](https://neovim.io/doc/user/options.html#'fillchars'). `[msgsep](#msgsep)`



## Upstreamed features [nvim-upstreamed](#nvim-upstreamed)



These Nvim features were later integrated into Vim.

['wildoptions'](https://neovim.io/doc/user/options.html#'wildoptions') flags: "pum" enables popupmenu for wildmode completion

[:source](https://neovim.io/doc/user/repeat.html#%3Asource) works with anonymous (no file) scripts

['statusline'](https://neovim.io/doc/user/options.html#'statusline') supports unlimited alignment sections



## Other changes [nvim-changed](#nvim-changed)



This section documents various low-level behavior changes.

[mkdir()](https://neovim.io/doc/user/builtin.html#mkdir\\(\\)) behaviour changed:

1\. Assuming /tmp/foo does not exist and /tmp can be written to mkdir('/tmp/foo/bar', 'p', 0700) will create both /tmp/foo and /tmp/foo/bar with 0700 permissions. Vim mkdir will create /tmp/foo with 0755.

2\. If you try to create an existing directory with `'p'` (e.g. mkdir('/', 'p')) mkdir() will silently exit. In Vim this was an error.

3\. mkdir() error messages now include strerror() text when mkdir fails.

[string()](https://neovim.io/doc/user/builtin.html#string\\(\\)) and [:echo](https://neovim.io/doc/user/eval.html#%3Aecho) behaviour changed:

1\. No maximum recursion depth limit is applied to nested container structures.

2\. [string()](https://neovim.io/doc/user/builtin.html#string\\(\\)) fails immediately on nested containers, not when recursion limit was exceeded.

3\. When [:echo](https://neovim.io/doc/user/eval.html#%3Aecho) encounters duplicate containers like

```
let l = []
echo [l, l]
```

it does not use "\[...\]" (was: "\[\[\], \[...\]\]", now: "\[\[\], \[\]\]"). "..." is only used for recursive containers.

4\. [:echo](https://neovim.io/doc/user/eval.html#%3Aecho) printing nested containers adds "@level" after "..." designating the level at which recursive container was printed: [:echo-self-refer](https://neovim.io/doc/user/eval.html#%3Aecho-self-refer). Same thing applies to [string()](https://neovim.io/doc/user/builtin.html#string\\(\\)) (though it uses construct like "{E724@level}"), but this is not reliable because [string()](https://neovim.io/doc/user/builtin.html#string\\(\\)) continues to error out.

5\. Stringifyed infinite and NaN values now use [str2float()](https://neovim.io/doc/user/builtin.html#str2float\\(\\)) and can be evaled back.

6\. (internal) Trying to print or stringify VAR_UNKNOWN in Vim results in nothing, E908, in Nvim it is internal error.

[json_decode()](https://neovim.io/doc/user/builtin.html#json_decode\\(\\)) behaviour changed:

2\. [msgpack-special-dict](https://neovim.io/doc/user/builtin.html#msgpack-special-dict) is emitted also in case of duplicate keys, while in Vim it errors out.

3\. It accepts only valid JSON. Trailing commas are not accepted.

Viminfo text files were replaced with binary (messagepack) [shada](https://neovim.io/doc/user/starting.html#shada) files. Additional differences:

[shada-s](https://neovim.io/doc/user/options.html#shada-s) now limits size of every item and not just registers.

['viminfo'](https://neovim.io/doc/user/deprecated.html#'viminfo') option got renamed to ['shada'](https://neovim.io/doc/user/options.html#'shada'). Old option is kept as an alias for compatibility reasons.

ShaDa file format was designed with forward and backward compatibility in mind. [shada-compatibility](https://neovim.io/doc/user/starting.html#shada-compatibility)

Some errors make ShaDa code keep temporary file in-place for user to decide what to do with it. Vim deletes temporary file in these cases. [shada-error-handling](https://neovim.io/doc/user/starting.html#shada-error-handling)

ShaDa file keeps search direction ([v:searchforward](https://neovim.io/doc/user/vvars.html#v%3Asearchforward)), viminfo does not.

[printf()](https://neovim.io/doc/user/builtin.html#printf\\(\\)) returns something meaningful when used with `%p` argument: in Vim it used to return useless address of the string (strings are copied to the newly allocated memory all over the place) and fail on types which cannot be coerced to strings. See [id()](https://neovim.io/doc/user/builtin.html#id\\(\\)) for more details, currently it uses `printf("%p", {expr})` internally.

[c_CTRL-R](https://neovim.io/doc/user/cmdline.html#c_CTRL-R) pasting a non-special register into [cmdline](https://neovim.io/doc/user/cmdline.html#cmdline) omits the last `<CR>`.

[CursorMoved](https://neovim.io/doc/user/autocmd.html#CursorMoved) triggers when moving between windows.

`:lua print("a\0b")` will print `a^@b`, like with `:echomsg "a\nb"` . In Vim that prints `a` and `b` on separate lines, exactly like `:lua print("a\nb")` .

`:lua error('TEST')` emits the error:

```
E5108: Error executing lua: [string "<Vimscript compiled string>"]:1: TEST
```

whereas Vim emits only "TEST".

Lua has direct access to Nvim [API](https://neovim.io/doc/user/api.html#API) via `vim.api`.

Commands:

[:doautocmd](https://neovim.io/doc/user/autocmd.html#%3Adoautocmd) does not warn about "No matching autocommands".

`:write!` does not show a prompt if the file was updated externally.

[:=](https://neovim.io/doc/user/various.html#%3A%3D) does not accept [ex-flags](https://neovim.io/doc/user/cmdline.html#ex-flags). With an arg it is equivalent to [:lua=](https://neovim.io/doc/user/lua.html#%3Alua%3D)

Command-line:

The meanings of arrow keys do not change depending on ['wildoptions'](https://neovim.io/doc/user/options.html#'wildoptions').

Functions:

[input()](https://neovim.io/doc/user/builtin.html#input\\(\\)) and [inputdialog()](https://neovim.io/doc/user/deprecated.html#inputdialog\\(\\)) support for each other’s features (return on cancel and completion respectively) via dictionary argument (replaces all other arguments if used), and "cancelreturn" can have any type if passed in a dictionary.

Highlight groups:

[hl-CursorLine](https://neovim.io/doc/user/syntax.html#hl-CursorLine) is low-priority unless foreground color is set

Highlight groups names are allowed to contain `@` characters.

It is an error to define a highlight group with a name that doesn't match the regexp `[a-zA-Z0-9_.@-]*` (see [group-name](https://neovim.io/doc/user/syntax.html#group-name)).

Macro ([recording](https://neovim.io/doc/user/repeat.html#recording)) behavior:

Replay of a macro recorded during :lmap produces the same actions as when it was recorded. In Vim if a macro is recorded while using :lmap'ped keys then the behaviour during record and replay differs.

['keymap'](https://neovim.io/doc/user/options.html#'keymap') is implemented via :lmap instead of :lnoremap so that you can use macros and ['keymap'](https://neovim.io/doc/user/options.html#'keymap') at the same time. This also means you can use [:imap](https://neovim.io/doc/user/map.html#%3Aimap) on the results of keys from ['keymap'](https://neovim.io/doc/user/options.html#'keymap').

Mappings:

Creating a mapping for a simplifiable key (e.g. `<C-I>`) doesn't replace an existing mapping for its simplified form (e.g. `<Tab>`).

"#" followed by a digit doesn't stand for a function key at the start of the lhs of a mapping.

Motion:

The [jumplist](https://neovim.io/doc/user/motion.html#jumplist) avoids useless/phantom jumps.

Performance:

Folds are not updated during insert-mode.

Syntax highlighting:

syncolor.vim has been removed. Nvim now sets up default highlighting groups automatically for both light and dark backgrounds, regardless of whether or not syntax highlighting is enabled. This means that [:syntax-on](https://neovim.io/doc/user/syntax.html#%3Asyntax-on) and [:syntax-enable](https://neovim.io/doc/user/syntax.html#%3Asyntax-enable) are now identical. Users who previously used an after/syntax/syncolor.vim file should transition that file into a colorscheme. [:colorscheme](https://neovim.io/doc/user/syntax.html#%3Acolorscheme)

Vimscript compatibility:

`count` does not alias to [v:count](https://neovim.io/doc/user/vvars.html#v%3Acount)

`errmsg` does not alias to [v:errmsg](https://neovim.io/doc/user/vvars.html#v%3Aerrmsg)

Working directory (Vim implemented some of these after Nvim):

[getcwd()](https://neovim.io/doc/user/builtin.html#getcwd\\(\\)) and [haslocaldir()](https://neovim.io/doc/user/builtin.html#haslocaldir\\(\\)) may throw errors if the tab page or window cannot be found. `[E5000](#E5000)` `[E5001](#E5001)` `[E5002](#E5002)`

[haslocaldir()](https://neovim.io/doc/user/builtin.html#haslocaldir\\(\\)) checks for tab-local directory if and only if -1 is passed as window number, and its only possible returns values are 0 and 1.

`getcwd(-1)` is equivalent to `getcwd(-1, 0)` instead of returning the global working directory. Use `getcwd(-1, -1)` to get the global working directory.

Autocommands:

[TermResponse](https://neovim.io/doc/user/autocmd.html#TermResponse) is fired for any OSC sequence received from the terminal, instead of the Primary Device Attributes response. [v:termresponse](https://neovim.io/doc/user/vvars.html#v%3Atermresponse)



## Missing features [nvim-missing](#nvim-missing)



These legacy Vim features are not yet implemented:



## Removed legacy features [nvim-removed](#nvim-removed)



These Vim features were intentionally removed from Nvim.

Aliases:

ex (alias for "nvim -e")

exim (alias for "nvim -E")

gex (GUI)

gview (GUI)

gvim (GUI)

gvimdiff (GUI)

rgview (GUI)

rgvim (GUI)

rview

rvim

view (alias for "nvim -R")

vimdiff (alias for "nvim -d" [diff-mode](https://neovim.io/doc/user/diff.html#diff-mode))

Commands:

:behave

:fixdel

`[hardcopy](#hardcopy)` `:hardcopy` was removed. Instead, use `:TOhtml` and print the resulting HTML using a web browser or other HTML viewer.

:helpfind

:mode (no longer accepts an argument)

:open

:Print

:promptfind

:promptrepl

:scriptversion (always version 1)

:shell

:sleep! (does not hide the cursor; same as :sleep)

:smile

:tearoff

:cstag

:cscope

:lcscope

:scscope

:Vimuntar

`:TOhtml` was replaced by a Lua version (with various differences)

Compile-time features:

Emacs tags support

Eval:

Vim9script

`[v:none](#v%3Anone)` (used by Vim to represent JavaScript "undefined"); use [v:null](https://neovim.io/doc/user/vvars.html#v%3Anull) instead.

Events:

`[SigUSR1](#SigUSR1)` Use [Signal](https://neovim.io/doc/user/autocmd.html#Signal) to detect `SIGUSR1` signal instead.

Options:

antialias

['backspace'](https://neovim.io/doc/user/options.html#'backspace') no longer supports number values. Instead:

for `backspace=0` set `backspace=` (empty)

for `backspace=1` set `backspace=indent,eol`

for `backspace=2` set `backspace=indent,eol,start` (default behavior in Nvim)

for `backspace=3` set `backspace=indent,eol,nostop`

bioskey (MS-DOS)

conskey (MS-DOS)

`['cp'](#'cp')` `['nocompatible'](#'nocompatible')` `['nocp'](#'nocp')` `['compatible'](#'compatible')` (Nvim is always "nocompatible".)

['cpoptions'](https://neovim.io/doc/user/options.html#'cpoptions') (gjpkHw<\*- and all POSIX flags were removed)

`['cryptmethod'](#'cryptmethod')` `['cm'](#'cm')` `['key'](#'key')` (Vim encryption implementation)

cscopepathcomp

cscopeprg

cscopequickfix

cscoperelative

cscopetag

cscopetagorder

cscopeverbose

esckeys

`['guipty'](#'guipty')` (Nvim uses pipes and PTYs consistently on all platforms.)

`['hkmap'](#'hkmap')` `['hk'](#'hk')` use `set keymap=hebrew` instead.

`['hkmapp'](#'hkmapp')` `['hkp'](#'hkp')` use `set keymap=hebrewp` instead.

keyprotocol

`['pastetoggle'](#'pastetoggle')` `['pt'](#'pt')` Just Paste It.™ [paste](https://neovim.io/doc/user/provider.html#paste) is handled automatically when you paste text using your terminal's or GUI's paste feature (`CTRL-SHIFT-v`, CMD-v (macOS), middle-click, …).

`['insertmode'](#'insertmode')` `['im'](#'im')` Use the following script to emulate ['insertmode'](https://neovim.io/doc/user/vim_diff.html#'insertmode'):

```
autocmd BufWinEnter * startinsert
inoremap <Esc> <C-X><C-Z><C-]>
inoremap <C-C> <C-X><C-Z>
inoremap <C-L> <C-X><C-Z><C-]><Esc>
inoremap <C-Z> <C-X><C-Z><Cmd>suspend<CR>
noremap <C-C> <Esc>
snoremap <C-C> <Esc>
noremap <C-\><C-G> <C-\><C-N><Cmd>startinsert<CR>
cnoremap <C-\><C-G> <C-\><C-N><Cmd>startinsert<CR>
inoremap <C-\><C-G> <C-X><C-Z>
autocmd CmdWinEnter * noremap <buffer> <C-C> <C-C>
autocmd CmdWinEnter * inoremap <buffer> <C-C> <C-C>
lua << EOF
  vim.on_key(function(c)
    if c == '\27' then
      local mode = vim.api.nvim_get_mode().mode
      if mode:find('^[nvV\22sS\19]') and vim.fn.getcmdtype() == '' then
        vim.schedule(function()
          vim.cmd('startinsert')
        end)
      end
    end
  end)
EOF
```

`['maxcombine'](#'maxcombine')` `['mco'](#'mco')` : Nvim counts maximum character sizes in bytes, not codepoints. This is guaranteed to be big enough to always fit all chars properly displayed in vim with ['maxcombine'](https://neovim.io/doc/user/vim_diff.html#'maxcombine') set to 6.

You can still edit text with larger characters than fits in the screen buffer, you just can't see them. Use [g8](https://neovim.io/doc/user/various.html#g8) or [ga](https://neovim.io/doc/user/various.html#ga). See [mbyte-combining](https://neovim.io/doc/user/mbyte.html#mbyte-combining).

**NOTE:** the rexexp engine still has a hard-coded limit of considering 6 composing chars only.

`['maxmem'](#'maxmem')` Nvim delegates memory-management to the OS.

`['maxmemtot'](#'maxmemtot')` Nvim delegates memory-management to the OS.

printoptions

`['secure'](#'secure')` : Everything is allowed in ['exrc'](https://neovim.io/doc/user/options.html#'exrc') files, because they must be explicitly marked as "trusted".

`['termencoding'](#'termencoding')` `['tenc'](#'tenc')` (Vim 7.4.852 also removed this for Windows)

textauto

textmode

weirdinvert

Plugins:

Providers:

`[if_lua](#if_lua)` : Nvim [Lua](https://neovim.io/doc/user/lua.html#Lua) API is not compatible with Vim's "if_lua".

Startup:

`--literal`: File args are always literal; to expand wildcards on Windows, use [:n](https://neovim.io/doc/user/editing.html#%3An) e.g. `nvim +"n *"`

Easy mode: eview, evim, nvim -y

Restricted mode: rview, rvim, nvim -Z

Vi mode: nvim -v

Test functions:

test_alloc_fail()

test_autochdir()

test_disable_char_avail()

test_feedinput()

test_garbagecollect_soon

test_getvalue()

test_ignore_error()

test_null_blob()

test_null_channel()

test_null_dict()

test_null_function()

test_null_job()

test_null_list()

test_null_partial()

test_null_string()

test_option_not_set()

test_override()

test_refcount()

test_scrollbar()

test_setmouse()

test_settime()

test_srand_seed()

TUI: `[t_xx](#t_xx)` `[termcap-options](#termcap-options)` `[t_AB](#t_AB)` `[t_Sb](#t_Sb)` `[t_vb](#t_vb)` `[t_SI](#t_SI)`

Nvim does not have special `t_XX` options nor `<t_XX>` keycodes to configure terminal capabilities. Instead Nvim treats the terminal as any other UI, e.g. ['guicursor'](https://neovim.io/doc/user/options.html#'guicursor') sets the terminal cursor style if possible.

`[xterm-8bit](#xterm-8bit)` `[xterm-8-bit](#xterm-8-bit)`

Xterm can be run in a mode where it uses true 8-bit CSI. Supporting this requires autodetection of whether the terminal is in UTF-8 mode or non-UTF-8 mode, as the 8-bit CSI character has to be written differently in each case. Vim issues a "request version" sequence to the terminal at startup and looks at how the terminal is sending CSI. Nvim does not issue such a sequence and always uses 7-bit control sequences.



Source: <https://neovim.io/doc/user/vim_diff.html#nvim-features>