# Tip 5 Find and Replace by Hand

# Tip 5 Find and Replace by Hand

Vim has a :substitute command for find-and-replace tasks, but with this alternative technique, we'll change the first occurrence by hand and then find and replace every other match one by one. The dot command will save us from labor, but we'll meet another nifty one-key command that makes jumping between matches a snap.

In this excerpt, the word "content" appears on every line: [the_vim_way/1_copy_content.txt](http://media.pragprog.com/titles/dnvim2/code/the_vim_way/1_copy_content.txt) ...We're waiting for content before the site can go live... ...If you are content with this, let's go ahead with it... ...We'll launch as soon as we have the content...

Suppose that we want to use the word "copy" (as in "copywriting") instead of "content." Easy enough, you might think; we can just use the substitute command, like this:
=> :%s/content/copy/g
But wait a minute! If we run this command, then we're going to create the phrase "If you are 'copy' with this," which is nonsense!

We've run into this problem because the word "content" has two meanings. One is synonymous with "copy" (and pronounced content), the other with "happy" (pronounced content). Technically, we're dealing with heteronyms (words that are spelled the same but differ in both meaning and pronunciation), but that doesn't really matter. The point is, we have to watch our step.

We can't just blindly replace every occurrence of "content" with "copy." We have to eyeball each one and answer "yay" or "nay" to the question, should this occurrence be changed? The substitute command is up to the task, and we'll find out how in Tip 90. But right now, we'll explore an alternative solution that fits with the theme of this chapter.

## Be Lazy: Search Without Typing

You might have guessed by now that the dot command is my favorite single-key Vim trigger. In second place is the command. This executes a search for the word under the cursor at that moment (see [ⓘ](http://vimhelp.appspot.com/pattern.txt.html#star)).

We could search for the word "content" by pulling up the search prompt and spelling out the word in full:
=> /content
Or we could simply place our cursor on the word and hit the key. Consider the following workflow:
KeystrokesBuffer Contents
{start}
...We're waiting for content before the site can go live... ...If you are content with this, let's go ahead with it... ...We'll launch as soon as we have the content...

 ...We're waiting for content before the site can go live... ...If you are content with this, let's go ahead with it... ...We'll launch as soon as we have the content...
cwcopy<Esc>
...We're waiting for content before the site can go live... ...If you are content with this, let's go ahead with it... ...We'll launch as soon as we have the copy...
n
...We're waiting for content before the site can go live... ...If you are content with this, let's go ahead with it... ...We'll launch as soon as we have the copy...
.
...We're waiting for copy before the site can go live... ...If you are content with this, let's go ahead with it... ...We'll launch as soon as we have the copy...

We begin with our cursor positioned on the word "content" and then use the command to search for it. Try it for yourself. Two things should happen: the cursor will jump forward to the next match, and all occurrences will be highlighted. If you don't see any highlighting, try running :set hls and then refer to Tip 81, for more details.

Having executed a search for the word "content," we can now advance to the next occurrence just by hitting the n key. In this case, pressing nn would cycle through all matches, taking us back to where we started.

## Make the Change Repeatable

With our cursor positioned at the start of the word "content," we are poised to change it. This involves two steps: deleting the word "content" and then typing its replacement. The cw command deletes to the end of the word and then drops us into Insert mode, where we can spell out the word "copy." Vim records our keystrokes until we leave Insert mode, so the full sequence cwcopy<Esc> is considered to be a single change. Pressing the . command deletes to the end of the current word and changes it to "copy."

## All Together Now

We're all set! Each time we press the n key, our cursor advances to the next occurrence of the word "content." And when we press the . key, it changes the word under the cursor to "copy."

If we wanted to replace all occurrences, we could blindly hammer out n.n.n. as many times as it took to complete all the changes (although in that case, we might as well have used the :%s/content/copy/g command). But we need to watch out for false matches. So after pressing n, we can examine the current match and decide if it should be changed to "copy." If so, we trigger the . command. If not, we don't. Whatever our decision, we can then move on to the next occurrence by pressing n again. Rinse and repeat until done.

---

[Chapter 1 The Vim Way.md](Chapter%201%20The%20Vim%20Way.md)