# Tip 66 Normalize, Strike, Abort

Tip 66 Normalize, Strike, Abort

Executing a macro can sometimes produce unexpected results, but we can achieve better consistency if we follow a handful of best practices.

When we execute a macro, Vim blindly repeats the sequence of canned keystrokes. If we aren't careful, the outcome when we replay a macro might diverge from our expectations. But it's possible to compose macros that are more flexible, adapting to do the right thing in each context.

The golden rule is this: when recording a macro, ensure that every command is repeatable.

# Normalize the Cursor Position

As soon as you start recording a macro, ask yourself these questions: where am I, where have I come from, and where am I going? Before you do anything, make sure your cursor is positioned so that the next command does what you expect, where you expect it.

That might mean moving the cursor to the next search match (n) or the start of the current line (0) or perhaps the first line of the current file (gg). Always starting on square one makes it easier to strike the right target every time.

# Strike Your Target with a Repeatable Motion

Vim has many motion commands for getting around a text file. Use them well.

Don't just hammer the l key until your cursor reaches its target. Remember, Vim executes your keystrokes blindly. Moving your cursor ten characters to the right might get you where you need to go as you record the macro, but what about when you play it back later? In another context, moving the cursor ten places to the right might overshoot the mark or stop short of it.

Word-wise motions, such as w, b, e, and ge tend to be more flexible than character-wise h and l motions. If we recorded the motion 0 followed by e, we could expect consistent results each time we executed the macro. The cursor would end up on the last character of the first word of the current line. It wouldn't matter how many characters that word contained, so long as the line contained at least one word.

Navigate by search. Use text objects. Exploit the full arsenal of Vim's motions to make your macros as flexible and repeatable as you can. Don't forget: when recording a macro, using the mouse is verboten!

# Abort When a Motion Fails

Vim's motions can fail. For example, if our cursor is positioned on the first line of a file, the k command does nothing. The same goes for j when our cursor is on the last line of a file. By default, Vim beeps at us when a motion fails, although we can mute it with the 'visualbell' setting (see 'visualbell'[ⓘ](http://vimhelp.appspot.com/options.txt.html#%27visualbell%27)).

If a motion fails while a macro is executing, then Vim aborts the rest of the macro. Consider this a feature, not a bug. We can use motions as a simple test of whether or not the macro should be executed in the current context.

Consider this example: We start by searching for a pattern. Let's say that the document has ten matches. We start recording a macro using the n command to repeat the last search. With our cursor positioned on a match, we make some small change to the text and stop recording the macro. The result of our edit is that this particular region of text no longer matches our search pattern. Now the document has only nine matches.

When we execute this macro, it jumps to the next match and makes the same change. Now the document has only eight matches. We execute the macro again and again, until eventually no matches remain. If we attempt to execute the macro now, the n command will fail because there are no more matches. The macro aborts.

Suppose that the macro was stored in the a register. Rather than executing @a ten times, we could prefix it with a count: 10@a. The beauty of this technique is that we can be unscrupulous about how many times we execute this macro. Don't care for counting? It doesn't matter! We could execute 100@a or even 1000@a, and it would produce the same result.

---

[Chapter 11 Macros.md](Chapter%2011%20Macros.md)