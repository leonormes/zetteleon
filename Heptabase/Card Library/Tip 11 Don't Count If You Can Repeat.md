# Tip 11 Don't Count If You Can Repeat

Tip 11 Don't Count If You Can Repeat

We can minimize the keystrokes required to perform certain tasks by providing a count, but that doesn't mean that we should. Consider the pros and cons of counting versus repeating.

Suppose that we had the following text in our buffer:
Delete more than one word
We want to do as the text says, changing it to read "Delete one word" instead. That is to say, we're going to delete two words.

We can approach this in a handful of ways. Both d2w and 2dw will work. With d2w, we invoke the delete command and then give 2w as the motion. We could read that as "delete two words." However, 2dw turns things around. This time the count applies to the delete command, but the motion acts over a single word. We could read this as "delete a word two times." Putting semantics aside, we get the same result either way.

Now let's consider an alternative: dw.. This we can read as "Delete a word and then repeat."

To recap, our options are as follows: d2w, 2dw, or dw.---three keystrokes each. But which is best?

For our discussion, d2w and 2dw are identical. After running either of these, we can press the u key to undo, and the two words that were deleted will appear again. Or, instead of undoing our change, we could repeat it with the dot command, which would delete the next two words.

In the case of dw., the result of pressing u or . is subtly different. Here, the change was dw---"delete word." So if we wanted to restore the two words that were deleted, we'd have to undo twice: pressing uu (or 2u if you prefer). Pressing the dot command would just delete the next word rather than the next two.

Now suppose that instead of deleting two words, our original intent was to delete three words. By a small error in judgment, we run d2w instead of d3w. What next? We can't use the dot command, because that would cause a total of four words to be deleted. So we could either back up and revise our count (ud3w) or continue by deleting the next word (dw).

If, on the other hand, we had used the command dw. in the first place, we would have to repeat the dot command only one more time. Because our original change was simply dw, the u and . commands have more granularity. Each acts upon one word at a time.

Now suppose that we want to delete seven words. We could either run d7w, or dw...... (that is, dw followed by the dot command six times). Counting keystrokes, we have a clear winner. But would you trust yourself to make the right count?

Counting is tedious. I'd rather hit the dot command six times than spend the same time looking ahead in order to reduce the number of keys that I have to press. What if I hit the dot command one too many times? No matter, I just back up by hitting the u key once.

Remember our mantra (from Tip 4): act, repeat, reverse. Here it is in action.

# Use a Count When It Matters

Suppose that we wanted to change the text "I have a couple of questions" to instead read "I have some more questions." We could do so as follows:
KeystrokesBuffer Contents
{start}
I have a couple of questions.
c3wsome more<Esc>
I have some more questions.

In this scenario, it doesn't make much sense to use the dot command. We could delete one word and then another (with the dot command), but then we'd have to switch gears and change to Insert mode (using i or cw, for example). To me, that feels awkward enough that I'd rather go ahead and use a count.

There's another advantage to using a count: it gives us a clean and coherent undo history. Having made this change, we could undo it with a single press of the u key, which ties in with the discussion in Tip 8.

That same argument also goes in favor of counting (d5w) over repeating (dw....), so my preferences may seem inconsistent here. You'll develop your own opinion on this, depending on how much you value keeping your undo history clean and whether or not you find it tiresome to use counts.

---

[Chapter 2 Normal Mode.md](Chapter%202%20Normal%20Mode.md)