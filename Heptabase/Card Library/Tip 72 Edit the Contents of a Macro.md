# Tip 72 Edit the Contents of a Macro

# Tip 72 Edit the Contents of a Macro

In Tip 69, we saw that adding commands at the end of a macro is straightforward. But what if we want to remove the last command? Or change something at the beginning of the macro? In this tip, we'll learn how to edit the content of a macro as if it were plain text.

# The Problem: Non-standard Formatting

Suppose that we've just followed the steps in Record One Unit of Work, saving our keystrokes into register a. Now we're faced with this file, which is formatted slightly differently:

[macros/mixed-lines.txt](http://media.pragprog.com/titles/dnvim2/code/macros/mixed-lines.txt)

1. One 2. Two 3. three 4. four
   Some of the lines already use a capital letter. In our macro, we used the \~ command, which toggles the case of the letter under the cursor (see \~[ⓘ](http://vimhelp.appspot.com/change.txt.html#%7E)). Instead of using \~, let's update the macro to use the command vU, which uppercases the letter under the cursor (see v_U[ⓘ](http://vimhelp.appspot.com/change.txt.html#v_U)).

# Keyboard Codes in Macros

In this example, we are working with a relatively simple register. But things can get messy quickly if we attempt to edit a larger macro. For example, let's inspect the macro that was recorded in Tip 70:
=> :reg a<= --- Registers --- "a Omoul<80>kb<80>kbdule Rank^\[j>GGoend^\[
Notice anything strange? First of all, the ^\[ symbol appears a couple of times. No matter whether you press <Esc> or <C-\[>, that's how Vim represents the Escape key.

Stranger still is the <80>kb symbol, which represents the backspace key. Study the keystrokes. When I recorded this macro, I started off by typing "moul." Upon seeing my mistake, I hit the backspace key a couple of times and then typed out "dule," the rest of the word.

This action is of no practical consequence. If I replay those keystrokes, Vim will reproduce my mistake followed by my correction. The net result will be correct. But it does make the register harder to read and more fiddly to edit.

# Paste the Macro into a Document

The registers that we use for recording macros are the very same with which the yank and put operations interact. So if we want to make changes to the macro saved in register a, we simply have to paste it into the document, where we can edit it as plain text.

Let's press G and jump to the end of the current document. We want to paste the contents of register a into a new line. The simplest way of doing that is with the :put command:
=> :put a
Why didn't we just use the "ap command? In this context, the p command would paste the contents of the a register after the cursor position on the current line. The :put command, on the other hand, always pastes below the current line, whether the specified register contains a line-wise or a character-wise set of text.

# Edit the Text

Now we can edit the macro as plain text. The sequence of commands shown in Table 13, Editing the Macro as Plain Text replaces the \~ character with vU.

Table 13. Editing the Macro as Plain Text
KeystrokesBuffer Contents
{start}
0f.r)w~~j
f~~
0f.r)w\~j
svU<Esc>
0f.r)wvUj

# Yank the Macro from the Document Back into a Register

We've got the sequence of commands looking just the way we want it to, so we can yank it from the document back into a register. The simplest way is to run "add (or :d a), but this could cause us problems later. The dd command performs a line-wise deletion. The register contains a trailing ^J character:
=> :reg a<= 0f.r)wvUj^J
This character represents a newline, which in most circumstances won't matter. But sometimes this trailing newline could change the meaning of the macro. As a precaution, using a character-wise yank to get the characters from the document back into the register is a safer bet:
KeystrokesBuffer Contents
{start}
// last line of the file proper 0f.r)wvUj
0
// last line of the file proper 0f.r)wvUj
"ay$
// last line of the file proper 0f.r)wvUj
dd
// last line of the file proper

When we run the command 0 followed by "ay$, we yank every character on that line except for the carriage return. Having captured everything that we want to keep into register a, we can then run dd to delete the line. This will end up in the default register, but we won't use it.

Having followed these steps, register a now contains a new and improved macro. We can use it on the example text that we met at the start of this tip.

# Discussion

Being able to paste a macro into the document, edit it right there, and then yank it back into a register and execute it is very handy. But the register can be fussy to work with for the reasons noted in Keyboard Codes in Macros. If you only have to append a command at the end of your macro, following the procedure outlined in Tip 69, is simpler.

Since Vim's registers are no more than containers for strings of text, we can also manipulate them programmatically using Vim script. For example, we could use the substitute() function (which is not the same as the :substitute command! See substitute()[ⓘ](http://vimhelp.appspot.com/eval.txt.html#substitute%28%29)) to perform the same edit as before:
=> :let @a=substitute(@a, '\~', 'vU', 'g')
If you're curious about this approach, look up function-list[ⓘ](http://vimhelp.appspot.com/usr_41.txt.html#function-list) for more ideas.

---

[Practical Vim Edit Text at the Speed of Thought - Neil, Drew.md](Practical%20Vim%20Edit%20Text%20at%20the%20Speed%20of%20Thought%20-%20Neil,%20Drew.md)

---

[Chapter 11 Macros.md](Chapter%2011%20Macros.md)