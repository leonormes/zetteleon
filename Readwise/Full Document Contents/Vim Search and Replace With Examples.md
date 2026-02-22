# Vim Search and Replace With Examples

![rw-book-cover](https://thevaluable.dev/images/2017/vim-search/searching-lightsaber-vim.jpg)

## Metadata
- Author: [[The Valuable Dev]]
- Full Title: Vim Search and Replace With Examples
- Category: #articles
- Summary: The document on Vim Search and Replace provides detailed instructions on utilizing Vim's search functionalities efficiently. It covers searching within the current file, searching in multiple files using vimgrep, and using external programs like grep. Additionally, it explains how to perform find and replace operations in the current file and across multiple files using Vim's substitute command and the arglist feature. The document also recommends using plugins like fzf and ripgrep for enhanced searching capabilities in Vim, offering tips and examples for effective searching strategies.
- URL: https://thevaluable.dev/vim-search-find-replace/

## Full Document
![you can even search your lightsaber with Vim](https://thevaluable.dev/images/2017/vim-search/searching-lightsaber-vim.jpg)
Can developers survive without a good search in their editor? Who has never used the famous *find and replace* trick in one or multiple files?

Nobody indeed.

The good new is: Vim search features are pure awesomeness. With a minimum of configuration, you can search whatever you want, wherever you want, at light speed.

We’ll see in this article how to:

* Search in the current file.
* Search in multiple files.
* Find and replace everything you dream of.
* Use great plugins to transform Vim in a Search Monster™.

Without the search features I’ll present you in this article, Vim would maybe not be part of my Mouseless Development Environment.

Speaking of which...

If you want to build a complete Mouseless Development Environment, [you might be interested by this book](https://themouseless.dev/).

A little precision: I will often refer to *Vim current working directory* in this article. The [ex command](https://www.sbf5.com/~cduan/technical/vi/vi-2.shtml) `:pwd` can tell you what’s yours. To change it, you can use `:cd mydirectory`.

If you don’t feel comfortable using Vim, I cover the [basics you need to know here](https://thevaluable.dev/vim-for-beginners/).

Thanks for everybody who helped me on this article, especially the nice [Neovim Reddit community](https://www.reddit.com/r/neovim/). I learned a ton from them!

Enough babbling. Let’s launch Vim, and let’s search! I invite you to try the tips of this article while you read them: [it will help you learn and remember](https://thevaluable.dev/learning-developer-efficiently-effectively/).

#### Vim Search in the Current File

##### Basics

To search in the current file, you just need to type `/` in [normal mode](https://en.wikibooks.org/wiki/Learning_the_vi_Editor/Vim/Modes). Then, you need to type your search pattern, press `enter`, and the result becomes highlighted in your file.

To go backward and forward through the results, you can type `n` and `N` (for `n`ext) respectively.

Using `/` will search forward in the file. If you need to directly search backward, you can use `?` instead.

If you want to search again using the previous search pattern, `//` is your friend.

##### Vim Highlight Search

It’s practical to see the search highlighted in the file, but it’s not enabled by default. To do so, you can type the command `:set hlsearch`, or set it permanently in your `vimrc`.

If you use [Neovim](https://neovim.io/), the highlighting is set by default.

##### Clearing the Highlight

The command `:noh` in normal mode will clear this highlight you tried to get rid of by trying (almost) every button on your keyboard. You know, like when you tried to [quit Vim the first time](https://stackoverflow.com/questions/11828270/how-do-i-exit-the-vim-editor).

Since you don’t really want to type this command each time you do a search, you can map a key to this command in your [vimrc](http://vim.wikia.com/wiki/Open_vimrc_file). Personally, I use the following mapping: `map <esc> :noh<cr>`.

Warning

It’s not advised to map `<esc>` to anything. I use it for years without problem, but beware.

##### Searching the Word Under the Cursor

To search the word under your cursor:

1. Place your cursor on the word you want to search.
2. Type `*` or `g*`.

As with `/`, every result will be highlighted.

To search for partial words (including word parts in the results), you can use the keystroke `g*`.

To search backward, you can use `#` or `g#`.

##### Search With Case Sensitive or Insensitive

If you want to ignore the case, here you go:

* `/search\C` - Case-sensitive search.
* `/search\c` - Case-insensitive search.

You can as well write the following command in your `vimrc`:

* `set ignorecase` - All your searches will be case-insensitive.
* `set smartcase` - Your search will be case-sensitive if it contains an uppercase letter.

Be aware that `ignorecase` needs to be set for `smartcase` to work.

#### Vim Search in Multiple Files

Searching in one file is great, but what about a whole project? It’s where you realize that Vim is crazy fast.

##### Searching with vimgrep

 ![vimgrep quickfix window](https://thevaluable.dev/images/2017/vim-search/vim-search-2.jpg)
*The quickfix window after executing `vimgrep kernel **/*.php` and `:copen`*

Searching with `vimgrep` will populate the [quickfix list](http://vimdoc.sourceforge.net/htmldoc/quickfix.html) (see `:help quickfix` and `:help quickfix-window` in Vim) with the result of the search.

It implies that you need to use the command `:cnext` (or `:cn`) and `:cprev` (or :`cp`) to go through the results (instead of `n` and `N` respectively).

You can as well open the quickfix window with `:copen` and go through the results.

For example:

* `:vimgrep pattern *` - Search the pattern in every file of the working directory.
* `:vimgrep pattern a.txt b.txt c.txt` - Search the same pattern only in the files “a.txt”, “b.txt” and “c.txt”.
* `:vimgrep pattern *.php` - Search “pattern” in every php files.
* `:vimgrep pattern **/*.php` - Search “pattern” in every php files in the working directory *and* every subdirectory.

Quick tip: You can go through all your results by taping `:cnext`, and then using the keystroke `@:` which repeats your last command. Then, you can use `@@` which repeat the previous `@<whatever>` (`:help @@`).

For more information about `vimgrep`, I strongly advice you to look at the excellent [vimcast](http://vimcasts.org/episodes/search-multiple-files-with-vimgrep/) about it.

I encourage you to read Vim’s help about vimgrep by typing `:help :vimgrep`. Actually, I encourage you to use Vim’s help as often as you can.

##### Searching With grep

`Vimgrep` is good but unfortunately slow. As an alternative, you can use an external program ([grep](https://themouseless.dev/posts/grep-beginner-mouseless) by default) directly in Vim, by using `:grep`. To configure the external program you want to use, you need to set `grepprg` (see `:help grepprg`). There’s an example how to do that below.

Using `:grep` and `:vimgrep` is similar. For example:

* `:grep mySearch *` - Search every occurences of `mySearch` in the working directory
* `:grep mySearch a.txt b.txt c.txt` - Search every occurences of `mySearch` in the files a.txt, b.txt, c.txt

You know the drill: `:help :grep`.

#### Find and Replace

##### Substitution In the Current File

Vim has a powerful find and replace functionality thanks to the `substitute` (see `:help :substitute`) command.

Let’s look at some examples:

* `:s/pattern/replace/g` - Substitute “pattern” by “replace” on the current line.
* `:%s/pattern/replace/g` - Substitute “pattern” by “replace” in the current file.
* `:%s//replace/g` - Substitute your last search by “replace” in the current file.

You may ask yourself: what the hell those letters and signs mean? Good question!

* The letter `s` stands for `substitute`.
* The keyword `%` will target the entire file instead of the current line. You can use it with different commands in different context.
* The flag `g` means “global”: more than one occurrence is targeted. Without it, only the first occurrence in the file (or the in line) would be replaced.

The syntax is similar to the command line tool `sed`. If you need to add the character `/` in your pattern or in your replacement, you can do:

* `:s/pat\/tern/replace/g` - Escape the `/` to match “pat/tern”
* `:s#pat/tern#replace#g` - Use another character as separator to match “pat/tern”.

 ![Vim substitute](https://thevaluable.dev/images/2017/vim-search/vim-search-3.jpg)
*This substitute will crash Symfony 4 kernel*

##### Find and Replace One Occurrence at a Time

It’s simple to search and then decide if you want to keep or replace each result in a file:

1. Execute a regular search with `/`.
2. Use the keystroke `cgn` on the first result to replace it.
3. Type `n` or `N` to go to the next result.
4. Use `.` to replace the occurrence with the same replacement, or go to the next result if you want to keep it.

What’s this `cgn` keystroke, you may ask? What does it mean? If you read `:help gn`, you’ll see that `gn` is the same as `n`, except that it will start Visual mode and select the occurrence. We just do a change (`c`) on the next (selected) searched occurrence. From there, you can imagine that keystrokes like `cgN` or `dgn` will work as well.

With this technique, you can do a granular *find and replace* in the whole file.

##### Find and Replace in Multiple Files

To find and replace in multiple files, you can use the excellent Vim [arglist](http://vimcasts.org/episodes/meet-the-arglist/). Think of it as an internal list of files you can modify.

If you want to replace an occurrence in every `html` and `twig` files, you can type the following:

1. `:arg *.html` - Populate the arglist with all `html` files in the current working directory, and edit the first one.
2. `:argadd *.twig` - Add `twig` files to the arglist.
3. `:argdo %s/pattern/replace/ge | update` - Replace the occurence `pattern` by `replace` in every file of the arglist.

Even if the argument list (`:help arglist`) and the buffer list (`:help :buffers`) are different, every files added in the argument list will be added in the buffer list.

You can delete files in one of these lists without changing the other. For example, `:argdelete *` will remove everything in your argument list.

At that point, you might scream to your screen, violently shacked by extrem curiosity: what means the flag `e` at the end of the `substitute` command? It prevents Vim to display an error message when the pattern is not found in a file.

What about doing a *find and replace* in the working directory **and** the subdirectories? You can populate the arglist as follow:

* `:arg **/*.html`
* `:argadd **/*.php`

You need to find and replace in the files in the buffer list? Easy! I expected you to have more difficult questions. You can execute:

`:bufdo %s/pattern/replace/ge | update`

The argument list can be used with `:grep` or `:vimgrep` too. For example, you could search in your current buffer, and then apply the result to every file in the argument list. For example:

* `/vim`
* `arg *.md`
* `vimgrep // ##`

Here, `//` is expanded to last used search pattern (see `:help search-commands`), and `##` to your argument list.

Now that your quickfix list has the results of your search, you can use `:cdo` to execute a command on each entry of the list. For example:

1. `:grep pattern **/*.html`
2. `:cdo s/blink/div/g | update`

Every result in every file of your quicklist will replace `blink` with `div`.

#### Beyond Vanilla Vim: Search with External Plugins

It’s good to know how to search in bare bone Vim, especially when you’re lost in a remote server far aways from your lovely `vimrc`.

I have a good new: there are even more alternatives to `vimgrep` and `grep`. The plugins described here might change your search life forever!

Since we speak about Vim plugins, I wrote another article which list the necessary Vim plugins to build a [Vim PHP IDE](https://thevaluable.dev/vim-php-ide/), in case you’re interested.

##### One Plugin to Rule Them All, One Plugin to Find Them

If there is one plugin I would take with me on a lost inhabited island (with a computer and Vim), it would be [fzf.vim](https://github.com/junegunn/fzf.vim) with its terminal twin [fzf](https://github.com/junegunn/fzf). Why?

* It’s blazing fast (written in Go). Einstein was wrong: you can go beyond light speed.
* It allows you to search in your terminal whatever file or history you want.
* It can be coupled with Vim to search in *many* stuff like buffers, tags, the command history, the open files history…

Here are some basic examples:

* `:Files` - Search for a file in your working directory and subdirectories.
* `:Buffers` - Search for a file open in one of your buffer.
* `:History` - Search for a file in your open file history.

You can as well copy your filtered search in the quickfix list using `alt-a`, and use the good old `:cdo` command!

##### Search, Vim, Search! Faster!

`fzf` is a powerful tool, but it’s not enough to search a precise occurrence in a bunch of files. You need another crazy fast CLI: [ripgrep](https://github.com/BurntSushi/ripgrep).

This tool is similar to `grep`. Coupled to `fzf`, `ripgrep` will bring under your little fingers the best search engine I’ve ever seen in any IDE. No more, no less.

In order to link `fzf` with `ripgrep`, you can look at my [fzf config file](https://github.com/Phantas0s/.dotfiles/blob/master/nvim/pluggedconf/fzf.nvimrc) on Github.

Then you just have to enter the command `:Rg pattern` to search “pattern” in every file in the working directory.

 ![Vim search is a beast with fzf and ripgrep](https://thevaluable.dev/images/2017/vim-search/vim-search-4.jpg)
*The sweet combo fzf and ripgrep*

If you don’t like `fzf`, you can still use `ripgrep` with the Vim command `:grep`. First, add the following to your `vimrc`:

```
if executable("rg")     set grepprg=rg\ --vimgrep endif
```

We spoke quickly about `grepprg` above. You can use it to define what program to use for the `:grep` command.

##### Find and Replace in Multiple Files with Vim ferret

I sometimes use the plugin [ferret](https://github.com/wincent/ferret). It allows you to search an occurrence in multiple files, select what results you want to replace, and finally replace them. If you have [ripgrep](https://github.com/BurntSushi/ripgrep) installed on your system, this plugin will use it by default.

Here’s how it works:

* `:Ack pattern` - Search in the working directory.
* `:Ack pattern /path/to/directory` - Search in the specified path and its subdirectories.

At that point, Ferret will populate the quickfix window with every result found. You can delete the result by typing `dd`, in case you don’t want to replace it. You can as well type `enter` to open the file with the result highlighted.

Then, typing `:Acks /pattern/replacement/` will replace every results still present in the quickfix window.

Simple, granular, and powerful: that’s what we want.

##### CocSearch

If you use the plugin [coc.nvim](https://github.com/neoclide/coc.nvim) already, you can use the very nice `:CocSearch`. You can do for example:

```
:CocSearch pattern */**.html
```

It will open a new window with the result of your search. You can simply modify it and save.

Even better: it uses `ripgrep` under the hood, so you can pass to it any argument. For example, to display (and be able to modify) 10 lines after the search result in each file:

```
:CocSearch pattern */**.html -A 20
```

#### Vim is Now Your Personal Search Beast

This overview will bring you whatever search functionality you need as a developer.

I personally use built-in vim search functionality when I search (or search in replace) in one file. When the search needs to be in a whole project, or in multiple files, I use the combo:

If you know other functionalities (or plugins) which can bring even more coolness in our search life, the comment section is ready for you.

You know, sharing is caring.

 ![I love Vim so much!](https://thevaluable.dev/images/2017/vim-search/vim-search-5.jpg)
##### Let's Connect

You'll receive **each month** the last article with additional resources and updates.

[Here's how it looks](https://buttondown.email/thevaluabledev/archive/the-valuable-dev-new-article-about-vim-and-many/)

You can reply to any email if you have questions, problems, or feedback. I'll write back as soon as I can.

Share Your Knowledge
