## Tip 15 Paste from a Register Without Leaving Insert Mode

Vim's yank and put operations are usually executed from Normal mode, but sometimes we might want to paste text into the document without leaving Insert mode.

Here's an unfinished excerpt of text: [insert_mode/practical-vim.txt](http://media.pragprog.com/titles/dnvim2/code/insert_mode/practical-vim.txt) Practical Vim, by Drew Neil Read Drew Neil's

We want to complete the last line by inserting the title of this book. Since that text is already present at the start of the first line, we'll yank it into a register and then append the text at the end of the next line in Insert mode:

Keystrokes | Buffer Contents
yt,
Practical Vim, by Drew Neil Read Drew Neil's
jA

![](images/000002.gif)


Practical Vim, by Drew Neil Read Drew Neil's
<C-r>0
Practical Vim, by Drew Neil Read Drew Neil's Practical Vim
.<Esc>
Practical Vim, by Drew Neil Read Drew Neil's Practical Vim.

The command yt, yanks the words Practical Vim into the yank register (we'll meet the t{char} motion in Tip 50). In Insert mode, we can press <C-r>0 to paste the text that we just yanked at the current cursor position. We'll discuss registers and the yank operation at greater length in Chapter 10, Copy and Paste.

The general format of the command is <C-r>{register}, where {register} is the address of the register we want to insert (see i_CTRL-R[ⓘ](http://vimhelp.appspot.com/insert.txt.html#i_CTRL-R)).

### Use <C-r>{register} for Character-wise Registers

The <C-r>{register} command is convenient for pasting a few words from Insert mode. If the register contains a lot of text, you might notice a slight delay before the screen updates. That's because Vim inserts the text from the register as if it were being typed one character at a time. If the 'textwidth' or 'autoindent' options are enabled, you might end up with unwanted line breaks or extra indentation.

The <C-r><C-p>{register} command is smarter. It inserts text literally and fixes any unintended indentation (see i_CTRL-R_CTRL-P[ⓘ](http://vimhelp.appspot.com/insert.txt.html#i_CTRL-R_CTRL-P)). But it's a bit of a handful! If I want to paste a register containing multiple lines of text, I prefer to switch to Normal mode and use one of the put commands (see \[\[Tip 63\]\]).