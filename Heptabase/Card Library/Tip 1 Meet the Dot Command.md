# Tip 1 Meet the Dot Command

# Tip 1 Meet the Dot Command

The dot command lets us repeat the last change. It is the most powerful and versatile command in Vim.

Vim's documentation simply states that the dot command "repeats the last change" (see .[ⓘ](http://vimhelp.appspot.com/repeat.txt.html#.)). It doesn't sound like much, but in that simple definition we'll find the kernel of what makes Vim's modal editing model so effective. First we have to ask, "What is a change?"

To understand the power of the dot command, we have to realize that the "last change" could be one of many things. A change could act at the level of individual characters, entire lines, or even the whole file.

To demonstrate, we'll use this snippet of text: [the_vim_way/0_mechanics.txt](http://media.pragprog.com/titles/dnvim2/code/the_vim_way/0_mechanics.txt) Line one Line two Line three Line four

The x command deletes the character under the cursor. When we use the dot command in this context, "repeat last change" tells Vim to delete the character under the cursor:
KeystrokesBuffer Contents
{start}
Line one Line two Line three Line four
x
ine one Line two Line three Line four
.
ne one Line two Line three Line four
..
one Line two Line three Line four

We can restore the file to its original state by pressing the u key a few times to undo the changes.

The dd command also performs a deletion, but this one acts on the current line as a whole. If we use the dot command after dd, then "repeat last change" instructs Vim to delete the current line:
KeystrokesBuffer Contents
{start}
Line one Line two Line three Line four
dd
Line two Line three Line four
.
Line three Line four

Finally, the >G command increases the indentation from the current line until the end of the file. If we follow this command with the dot command, then "repeat last change" tells Vim to increase the indentation level from the current position to the end of the file. In this example, we'll start with the cursor on the second line to highlight the difference
KeystrokesBuffer Contents
{start}
Line one Line two Line three Line four

\> G
Line one Line two Line three Line four
j
Line one Line two Line three Line four
.
Line one Line two Line three Line four
j.
Line one Line two Line three Line four

The x, dd, and > commands are all executed from Normal mode, but we also create a change each time we dip into Insert mode. From the moment we enter Insert mode (by pressing i, for example) until we return to Normal mode (by pressing <Esc>), Vim records every keystroke. After making a change such as this, the dot command will replay our keystrokes (see Moving Around in Insert Mode Resets the Change, for a caveat).

## The Dot Command Is a Micro Macro

Later, in Chapter 11, Macros, we'll see that Vim can record any arbitrary number of keystrokes to be played back later. This allows us to capture our most repetitive workflows and replay them at a keystroke. We can think of the dot command as being a miniature macro, or a "micro" if you prefer.

We'll see a few applications of the dot command throughout this chapter. We'll also learn a couple of best practices for working with the dot command in Tip 9, and Tip 23.

---

[Chapter 1 The Vim Way.md](Chapter%201%20The%20Vim%20Way.md)