# Chapter 3 Insert Mode

Most of Vim's commands are triggered from other modes, but some functionality is within easy reach from Insert mode. In this chapter, we'll explore these commands. Although delete, yank, and put commands are all triggered from Normal mode, we'll see that there is a convenient shortcut for pasting text from a register without leaving Insert mode. We'll learn that Vim provides two easy ways for inserting unusual characters that are not represented on the keyboard.

Replace mode is a special case of Insert mode, which overwrites existing characters in the document. We'll learn how to invoke this and consider some scenarios where it proves useful. We'll also meet [Insert Normal mode.md](Insert%20Normal%20mode.md), a submode that lets us fire a single Normal mode command before dropping us back into Insert mode.

Autocompletion is the most advanced functionality available to us from Insert mode. We'll cover it in depth in Chapter 19, Dial X for Autocompletion.