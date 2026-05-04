# Tip 8 Chunk Your Undos

# Tip 8 Chunk Your Undos

Tip 8 Chunk Your Undos

In other text editors, invoking the undo command after typing a few words might revert the last typed word or character. However, in Vim we can control the granularity of the undo command.

The u key triggers the undo command, which reverts the most recent change. A change could be anything that modifies the text in the document. That includes commands triggered from Normal, Visual, and Command-Line modes, but a change could also encompass any text entered (or deleted) in Insert mode. So we could also say that i{insert some text}<Esc> constitutes a change.

In nonmodal text editors, triggering the undo command after typing a few words could do one of two things. It could undo the last character that was typed. Or, more helpfully, it could chunk a set of characters together so that each undo operation removed a word instead of a character.

In Vim, we can control the granularity of the undo command. From the moment we enter Insert mode until we return to Normal mode, everything we type (or delete) counts as a single change. So we can make the undo command operate on words, sentences, or paragraphs just by moderating our use of the <Esc> key.

So how often should you leave Insert mode? It's a matter of preference, but I like to make each "undoable chunk" correspond to a thought. As I write this text (in Vim, of course!), I often pause at the end of a sentence to consider what I'll write next. No matter how brief its duration, each pause forms a natural break point, giving me a cue to leave Insert mode. When I'm ready to continue writing, I press A and carry on where I left off.

If I decide that I've taken a wrong turn, I'll switch to Normal mode and press u. Each time I undo, my text decomposes in coherent chunks that correspond to my thought process as I was writing the original text. It means that I can easily try out a sentence or two and then throw them away with a couple of keystrokes.

If I'm in Insert mode with my cursor at the end of a line, the quickest way to open a new line is to press <CR>. And yet I sometimes prefer to press <Esc>o just because I anticipate that I might want that extra granularity from the undo command. If this sounds hard core, don't worry. As you become adept with Vim, switching modes feels more and more lightweight.

As a general rule, if you've paused for long enough to ask the question, "Should I leave Insert mode?" then do it.

Moving Around in Insert Mode Resets the Change
When I said that the undo command would revert all characters entered (or deleted) during a trip into Insert mode and back, I was glossing over a small detail. If we use the <Up>, <Down>, <Left>, or <Right> cursor keys while in Insert mode, a new undo chunk is created. It's just as though we had switched back to Normal mode to move around with the h, j, k, or l commands, except that we don't have to leave Insert mode. This also has implications on the operation of the dot command.

---

[Chapter 2 Normal Mode.md](Chapter%202%20Normal%20Mode.md)