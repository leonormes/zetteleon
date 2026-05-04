# Tip 6 Meet the Dot Formula

# Tip 6 Meet the Dot Formula

We've considered three simple editing tasks so far. Even though each problem was different, we found a solution using the dot command for each one. In this tip, we'll compare each solution and identify a common pattern---an optimal editing strategy that I call the Dot Formula.

## Reviewing Three Dot-Command Editing Tasks

In Tip 2, we wanted to append a semicolon at the end of a sequence of lines. We changed the first line by invoking A;<Esc>, which set us up so that we could use the dot command to repeat the change on each subsequent line. We could move between lines using the j command, and the remaining changes could be completed simply by pressing j. as many times as necessary.

In Tip 3, we wanted to pad each occurrence of the + symbol with a space both in front and behind. We used the f+ command to jump to our target and then the s command to substitute one character with three. That set us up so that we could complete the task by pressing ;. a few times.

In Tip 5, we wanted to substitute every occurrence of the word "content" with the word "copy." We used the command to initiate a search for the target word and then ran the cw command to change the first occurrence. This set us up so that the n key would take us to the next match and the . key would apply the same change. We could complete the task simply by pressing n. as many times as it took.

## The Ideal: One Keystroke to Move, One Keystroke to Execute

In all of these examples, using the dot command repeats the last change. But that's not the only thing they share. A single keystroke is all that's required to move the cursor to its next target.

We're using one keystroke to move and one keystroke to execute. It can't really get any better than that, can it? It's an ideal solution. We'll see this editing strategy coming up again and again, so for the sake of convenience, we'll refer to this pattern as the Dot Formula.

---

[Practical Vim Edit Text at the Speed of Thought - Neil, Drew.md](Practical%20Vim%20Edit%20Text%20at%20the%20Speed%20of%20Thought%20-%20Neil,%20Drew.md)

---

[Chapter 1 The Vim Way.md](Chapter%201%20The%20Vim%20Way.md)