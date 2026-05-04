# Tip 69 Append Commands to a Macro

Tip 69 Append Commands to a Macro

Sometimes we miss a vital step when we record a macro. There's no need to re-record the whole thing from scratch. Instead, we can tack extra commands onto the end of an existing macro.

Suppose that we record this macro (borrowed from Tip 68):
KeystrokesBuffer contents
qa

1. one 2. two
   0f.r)w\~

2. One 2. two
   q

3. One 2. two

Immediately after pressing q to stop recording, we realize that we should have finished by pressing j to advance to the next line.

Before we fix it, let's inspect the contents of register a:
=> :reg a<= "a 0f.r)w\~
If we type qa, then Vim will record our keystrokes, saving them into register a by overwriting the existing contents of that register. If we type qA, then Vim will append our keystrokes to the existing contents of register a.
KeystrokesBuffer Contents
qA

1. One 2. two
   j

2. One 2. two
   q

3. One 2. two

Let's see what's in the a register now:
=> :reg a<= "a 0f.r)w\~j
All of the commands that we recorded the first time around are still there, but now it ends with j.

# Discussion

This little trick saves us from having to re-record the entire macro from scratch. But we can use it only to tack commands on at the end of a macro. If we wanted to add something at the beginning or somewhere in the middle of a macro, this technique would be of no use to us. In Tip 72, we'll learn about a more powerful method for amending a macro after it has been recorded.

---

[Chapter 11 Macros.md](Chapter%2011%20Macros.md)