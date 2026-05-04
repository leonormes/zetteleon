# Tip 4 Act, Repeat, Reverse

# Tip 4 Act, Repeat, Reverse

When facing a repetitive task, we can achieve an optimal editing strategy by making both the motion and the change repeatable. Vim has a knack for this. It remembers our actions and keeps the most common ones within close reach so that we can easily replay them. In this tip, we'll introduce each of the actions that Vim can repeat and learn how to reverse them.

Table 1. Repeatable Actions and How to Reverse Them
IntentActRepeatReverse
Make a change

{edit}

.

u

Scan line for next character

f{char}/t{char}

;

,

Scan line for previous character

F{char}/T{char}

;

,

Scan document for next match

/pattern<CR>

n

N

Scan document for previous match

?pattern<CR>

n

N

Perform substitution

:s/target/replacement

&

u

Execute a sequence of changes

qx{changes}q

@x

u

We've seen that the dot command repeats the last change. Since lots of operations count as a change, the dot command proves to be versatile. But some commands can be repeated by other means. For example, @: can be used to repeat any Ex command (as discussed in Tip 31). Or we can repeat the last :substitute command (which itself happens to be an Ex command as well) by pressing & (see Tip 93).

If we know how to repeat our actions without having to spell them out every single time, then we can be more efficient. First we act; then we repeat.

But when so much can be achieved with so few keystrokes, we have to watch our step. It's easy to get trigger-happy. Rapping out j.j.j. again and again feels a bit like doing a drum roll. What happens if we accidentally hit the j key twice in a row? Or worse, the . key?

Whenever Vim makes it easy to repeat an action or a motion, it always provides some way of backing out in case we accidentally go too far. In the case of the dot command, we can always hit the u key to undo the last change. If we hit the ; key too many times after using the f{char} command, we'll miss our mark. But we can back up again by pressing the , key, which repeats the last f{char} search in the reverse direction (see Tip 50).

It always helps to know where the reverse gear is in case you accidentally go a step too far. Table 1, Repeatable Actions and How to Reverse Them, summarizes Vim's repeatable commands along with their corresponding reverse action. In most cases, the undo command is the one that we reach for. No wonder the u key on my keyboard is so worn out!

---

[Chapter 1 The Vim Way.md](Chapter%201%20The%20Vim%20Way.md)