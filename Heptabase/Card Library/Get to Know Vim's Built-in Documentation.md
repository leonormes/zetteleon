# Get to Know Vim's Built-in Documentation

Get to Know Vim's Built-in Documentation

The best way to get to know Vim's documentation is by spending time in it. To help out, I've included "hyperlinks" for entries in Vim's documentation. For example, here's the "hyperlink" for the Vim tutor: vimtutor[ⓘ](http://vimhelp.appspot.com/usr_01.txt.html#vimtutor).

The icon has a dual function. First, it serves as a signpost, drawing the eye to these helpful references. Second, if you're reading this on an electronic device that's connected to the Internet, you can click the icon and it will take you to the relevant entry in Vim's online documentation. In this sense, it truly is a hyperlink.

But what if you're reading the paper edition of the book? Not to worry. If you have an installation of Vim within reach, simply enter the command as it appears in front of the icon.

For example, type :h vimtutor (:h is an abbreviation for the :help command). Consider this a unique address for the documentation on vimtutor: a URL of sorts. In this sense, the help reference is a kind of hyperlink to Vim's built-in documentation.

# Playing Melodies

In Normal mode, we compose commands by typing one or more keystrokes in sequence. These commands appear as follows:

| Notation | Meaning | 
|---|---|
| x | Press x once | 
| dw | In sequence, press d, then w | 
| dap | In sequence, press d, a, then p | 

Most of these sequences involve two or three keystrokes, but some are longer. Deciphering the meaning of Vim's Normal mode command sequences can be challenging, but you'll get better at it with practice.

# Playing Chords

When you see a keystroke such as <C-p>, it doesn't mean "Press <, then C, then -, and so on." The <C-p> notation is equivalent to Ctrl-p, which means "Press the <Ctrl> and p keys at the same time."

I didn't choose this notation without good reason. Vim's documentation uses it (key-notation[ⓘ](http://vimhelp.appspot.com/intro.txt.html#key-notation)), and we can also use it in defining custom key mappings. Some of Vim's commands are formed by combining chords and keystrokes in sequence, and this notation handles them well. Consider these examples:

| Notation | Meaning | 
|---|---|
| <C-n> | Press <Ctrl> and n at the same time | 
| g<C-\]> | Press g, followed by <Ctrl> and \] at the same time | 
| <C-r>0 | Press <Ctrl> and r at the same time, then 0 | 
| <C-w><C-=> | Press <Ctrl> and w at the same time, then <Ctrl> and = at the same time | 

# Placeholders

Many of Vim's commands require two or more keystrokes to be entered in sequence. Some commands must be followed by a particular kind of keystroke, while other commands can be followed by any key on the keyboard. I use curly braces to denote the set of valid keystrokes that can follow a command. Here are some examples:

| Notation | Meaning | 
|---|---|
| f{char} | Press f, followed by any other character | 
| \`{a-z} | Press \`, followed by any lowercase letter | 
| m{a-zA-Z} | Press m, followed by any lowercase or uppercase letter | 
| d{motion} | Press d, followed by any motion command | 
| <C-r>{register} | Press <Ctrl> and r at the same time, followed by the address of a register | 

# Showing Special Keys

Some keys are called by name. This table shows a selection of them:

| Notation | Meaning | 
|---|---|
| <Esc> | Press the Escape key | 
| <CR> | Press the carriage return key (also known as <Enter>) | 
| <Ctrl> | Press the Control key | 
| <Tab> | Press the Tab key | 
| <Shift> | Press the Shift key | 
| <S-Tab> | Press the <Shift> and <Tab> keys at the same time | 
| <Up> | Press the up arrow key | 
| <Down> | Press the down arrow key | 

![](images/000002.gif)

Press the space bar

Note that the space bar is represented as 

![](images/000002.gif)

. This could be combined with the f{char} command to form f

![](images/000002.gif)

.

# Switching Modes Midcommand

When operating Vim, it's common to switch from Normal to Insert mode and back again. Each keystroke could mean something different, depending on which mode is active. I've used an alternative style to represent keystrokes entered in Insert mode, which makes it easy to differentiate them from Normal mode keystrokes.

Consider this example: cwreplacement<Esc>. The Normal mode cw command deletes to the end of the current word and switches to Insert mode. Then we type the word "replacement" in Insert mode and press <Esc> to switch back to Normal mode again.

The Normal mode styling is also used for Visual mode keystrokes, while the Insert mode styling can indicate keystrokes entered in [Command-Line mode.md](Command-Line%20mode.md) and Replace mode. Which mode is active should be clear from context.

# Interacting with the Command Line

In some tips we'll execute a command line, either in the shell or from inside Vim. This is what it looks like when we execute the grep command in the shell:

`=\> $ grep -n Waldo`

And this is how it looks when we execute Vim's built-in :grep command:

`=\> :grep Waldo`

In Practical Vim, the $ symbol indicates that a command line is to be executed in an external shell, whereas the : prompt indicates that the command line is to be executed internally from [Command-Line mode.md](Command-Line%20mode.md). Occasionally we'll see other prompts, including these:

| Prompt | Meaning | 
|---|---|
| $ | Enter the command line in an external shell | 
| : | Use [Command-Line mode.md](Command-Line%20mode.md) to execute an Ex command | 
| / | Use [Command-Line mode.md](Command-Line%20mode.md) to perform a forward search | 
| ? | Use [Command-Line mode.md](Command-Line%20mode.md) to perform a backward search | 
| = | Use [Command-Line mode.md](Command-Line%20mode.md) to evaluate a Vim script expression | 

Any time you see an Ex command listed inline, such as :write, you can assume that the <CR> key is pressed to execute the command. Nothing happens otherwise, so you can consider <CR> to be implicit.

By contrast, Vim's search command allows us to preview the first match before pressing <CR> (see Tip 82). When you see a search command listed inline, such as /pattern<CR>, the <CR> keystroke is listed explicitly. If the <CR> is omitted, that's intentional, and it means you shouldn't press the Enter key just yet.

# Showing the Cursor Position in a Buffer

When showing the contents of a buffer, it's useful to be able to indicate where the cursor is positioned. In this example, you should see that the cursor is placed on the first letter of the word "One":
One two three
When we make a change that involves several steps, the contents of the buffer pass through intermediate states. To illustrate the process, I use a table showing the commands executed in the left column and the contents of the buffer in the right column. Here's a simple example:

| Keystrokes | Buffer Contents | 
|---|---|
|  | {start}One two three | 
| dw | two three | 

In row 2 we run the dw command to delete the word under the cursor. We can see how the buffer looks immediately after running this command by looking at the contents of the buffer in the same row.

# Highlighting Search Matches

When demonstrating Vim's search command, it's helpful to be able to highlight any matches that occur in the buffer. In this example, searching for the string "the" causes four occurrences of the pattern to be highlighted:
KeystrokesBuffer Contents
{start}
the problem with these new recruits is that they don't keep their boots clean.
/the<CR>
the problem with these new recruits is that they don't keep their boots clean.

Skip ahead to Tip 81, to find out how to enable search highlighting in Vim.

# Selecting Text in Visual Mode

Visual mode lets us select text in the buffer and then operate on the selection. Here, we use the it text object to select the contents of the <a> tag:
KeystrokesBuffer Contents
{start}
<a href="<http://pragprog.com/dnvim/>">Practical Vim</a>
vit
<a href="<http://pragprog.com/dnvim/>">Practical Vim</a>

Note that the styling for a Visual selection is the same for highlighted search matches. When you see this style, it should be clear from context whether it represents a search match or a Visual selection.

## Downloading the Examples

The examples in Practical Vim usually begin by showing the contents of a file before we change it. These code listings include the file path: [macros/incremental.txt](http://media.pragprog.com/titles/dnvim2/code/macros/incremental.txt) partridge in a pear tree turtle doves French hens calling birds golden rings

Each time you see a file listed with its file path in this manner, it means that you can download the example. I recommend that you open the file in Vim and try out the exercises for yourself. It's the best way to learn!

To follow along, download all the examples and source code from the Pragmatic Bookshelf. If you're reading on an electronic device that's connected to the Internet, you can also fetch each file one by one by clicking on the filename. Try it with the example above.

# Use Vim's Factory Settings

Vim is highly configurable. If you don't like the defaults, then you can change them. That's a good thing, but it could cause confusion if you follow the examples in this book using a customized version of Vim. You may find that some things don't work for you the way that they are described in the text. If you suspect that your customizations are causing interference, here's a quick test. Try quitting Vim and then launching it with these options:

`=\> $ vim -u NONE -N`

The -u NONE flag tells Vim not to source your vimrc on startup. That way, your customizations won't be applied and plugins will be disabled. When Vim starts up without loading a vimrc file, it reverts to vi compatible mode, which causes many useful features to be disabled. The -N flag prevents this by setting the 'nocompatible' option.

For most examples in Practical Vim, the vim -u NONE -N trick should guarantee that you get the same experience as described, but there are a couple of exceptions. Some of Vim's built-in features are implemented with Vim script, which means that they will only work when plugins are enabled. This file contains the absolute minimum configuration that is required to activate Vim's built-in plugins:

[essential.vim](http://media.pragprog.com/titles/dnvim2/code/essential.vim)
set nocompatible filetype plugin on
When launching Vim, you can use this file instead of your vimrc by running the following:
=> $ vim -u code/essential.vim
You'll have to adjust the code/essential.vim path accordingly. With Vim's built-in plugins enabled, you'll be able to use features such as netrw (Tip 44) and omni-completion (Tip 119), as well as many others. I consider Vim's factory settings to mean built-in plugins enabled and vi compatibility disabled.

Look out for subsections titled "Preparation" at the top of a tip. To follow along with the material in these tips, you'll need to configure Vim accordingly. If you start up with Vim's factory settings and then apply the customizations on the fly, you should be able to reproduce the steps from these tips without any problems.

If you're still having problems, see On Vim Versions.

# On the Role of Vim Script

Vim script enables us to add new functionality to Vim or to change existing functionality. It's a complete scripting language in itself and a subject worthy of a book of its own. Practical Vim is not that book.

But we won't steer clear of the subject entirely. Vim script is always just below the surface, ready to do our bidding. We'll see a few examples of how it can be used for everyday tasks in Tip 16; Tip 71; Tip 95; and Tip 96.

Practical Vim shows you how to get by with Vim's core functionality. In other words, no third-party plugins assumed. I've made an exception for Tip 87. The visual-star.vim plugin adds a feature that I find indispensable, and it requires very little code---less than ten lines of Vim script. It demonstrates how easily Vim's functionality can be extended. The implementation of visual-star.vim is presented inline without explanation. This should give you an idea of what Vim script looks like and what you can accomplish with it. If it piques your interest, then so much the better.

# On Vim Versions

All examples in Practical Vim were tested on the latest version of Vim, which was 7.4 at the time of writing. That said, most examples should work fine on any 7.x release, and many of the features discussed are also available in 6.x.

Some of Vim's functionality can be disabled during compilation. For example, when configuring the build, we could provide the --with-features=tiny option, which would disable all but the most fundamental features (there are also feature set labelled small, normal, big, and huge). You can browse the feature list by looking up +feature-list[ⓘ](http://vimhelp.appspot.com/various.txt.html#%2Bfeature-list).

If you find that you're missing a feature discussed in this book, you might be using a minimal Vim build. Check whether or not the feature is available to you with the :version command:
=> :version<= VIM - Vi IMproved 7.4 (2013 Aug 10, compiled Oct 14 2015 18:41:08) Huge version without GUI. Features included (+) or not (-): +arabic +autocmd +balloon_eval +browse +builtin_terms +byte_offset +cindent +clientserver +clipboard +cmdline_compl +cmdline_hist +cmdline_info +comments ...
On a modern computer, there's no reason to use anything less than Vim's huge feature set!

---

[Practical Vim Edit Text at the Speed of Thought - Neil, Drew.md](Practical%20Vim%20Edit%20Text%20at%20the%20Speed%20of%20Thought%20-%20Neil,%20Drew.md)