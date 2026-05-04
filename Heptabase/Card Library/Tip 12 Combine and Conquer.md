# Tip 12 Combine and Conquer

Tip 12 Combine and Conquer

Much of Vim's power stems from the way that operators and motions can be combined. In this tip, we'll look at how this works and consider the implications.

# Operator + Motion = Action

The d{motion} command can operate on a single character (dl), a complete word (daw), or an entire paragraph (dap). Its reach is defined by the motion. The same goes for c{motion}, y{motion}, and a handful of others. Collectively, these commands are called operators. You can find the complete list by looking up operator[ⓘ](http://vimhelp.appspot.com/motion.txt.html#operator), while Table 2, Vim's Operator Commands, summarizes some of the more common ones.

Table 2. Vim's Operator Commands
TriggerEffect
c
Change
d
Delete
y
Yank into register
g\~
Swap case
gu
Make lowercase
gU
Make uppercase

Shift right
<
Shift left

=

Autoindent
!
Filter {motion} lines through an external program

The g\~, gu, and gU commands are invoked by two keystrokes. In each case, we can consider the g to be a prefix that modifies the behavior of the subsequent keystroke. See Meet Operator-Pending Mode, for further discussion.

The combination of operators with motions forms a kind of grammar. The first rule is simple: an action is composed from an operator followed by a motion. Learning new motions and operators is like learning the vocabulary of Vim. If we follow the simple grammar rules, we can express more ideas as our vocabulary grows.

Suppose that we already know how to delete a word using daw, and then we learn about the gU command (see gU[ⓘ](http://vimhelp.appspot.com/change.txt.html#gU)). It's an operator too, so we can invoke gUaw to convert the current word to SHOUTY case. If we then expand our vocabulary to include the ap motion, which acts upon a paragraph, then we find two new operations at our disposal: dap to delete, or gUap to make the whole paragraph shout.

Vim's grammar has just one more rule: when an operator command is invoked in duplicate, it acts upon the current line. So dd deletes the current line, while >> indents it. The gU command is a special case. We can make it act upon the current line by running either gUgU or the shorthand gUU.

# Extending Vim's Combinatorial Powers

The number of actions that we can perform using Vim's default set of operators and motions is vast. But we can expand these even further by rolling our own custom motions and operators. Let's consider the implications.

# Custom Operators Work with Existing Motions

The standard set of operators that ships with Vim is relatively small, but it is possible to define new ones. Tim Pope's commentary.vim plugin provides a good example. This adds a command for commenting and uncommenting lines of code in all languages supported by Vim.

The commentary command is triggered by gc{motion}, which toggles commenting for the specified lines. It's an operator command, so we can combine it with all of the usual motions. gcap will toggle commenting for the current paragraph. gcG comments from the current line to the end of the file. gcc comments the current line.

If you're curious about how to create your own custom operators, start by reading :map-operator[ⓘ](%3C%3Chttp://vimhelp.appspot.com/map.txt.html#%3Amap-operator%3E%3E).

# Custom Motions Work with Existing Operators

Vim's standard set of motions is fairly comprehensive, but we can augment it further by defining new motions and text objects.

Kana Natsuno's textobj-entire plugin is a good example. It adds two new text objects to Vim: ie and ae, which act upon the entire file.

If we wanted to autoindent the entire file using the = command, we could run gg=G (that is, gg to jump to the top of the file and then =G to autoindent everything from the cursor position to the end of the file). But if we had the textobj-entire plugin installed, we could simply run =ae. It wouldn't matter where our cursor was when we ran this command; it would always act upon the entire file.

Note that if we had both the commentary and textobj-entire plugins installed, we could use them together. Running gcae would toggle commenting throughout the current file.

If you're curious about how to create your own custom motions, start by reading omap-info[ⓘ](http://vimhelp.appspot.com/map.txt.html#omap-info).

Meet Operator-Pending Mode
Normal, Insert, and Visual modes are readily identified, but Vim has other modes that are easy to overlook. Operator-Pending mode is a case in point. We use it dozens of times daily, but it usually lasts for just a fraction of a second. For example, we invoke it when we run the command dw. It lasts during the brief interval between pressing d and w keys. Blink and you'll miss it!

If we think of Vim as a finite-state machine, then Operator-Pending mode is a state that accepts only motion commands. It is activated when we invoke an operator command, and then nothing happens until we provide a motion, which completes the operation. While Operator-Pending mode is active, we can return to Normal mode in the usual manner by pressing escape, which aborts the operation.

Many commands are invoked by two or more keystrokes (for examples, look up g[ⓘ](http://vimhelp.appspot.com/index.txt.html#g), z[ⓘ](http://vimhelp.appspot.com/index.txt.html#z), ctrl-w[ⓘ](http://vimhelp.appspot.com/index.txt.html#CTRL-W), or \[[ⓘ](http://vimhelp.appspot.com/index.txt.html#%5B)), but in most cases, the first keystroke merely acts as a prefix for the second. These commands don't initiate Operator-Pending mode. Instead, we can think of them as namespaces that expand the number of available command mappings. Only the operator commands initiate Operator-Pending mode.

Why, you might be wondering, is an entire mode dedicated to those brief moments between invoking operator and motion commands, whereas the namespaced commands are merely an extension of Normal mode? Good question! Because we can create custom mappings that initiate or target Operator-Pending mode. In other words, it allows us to create custom operators and motions, which in turn allows us to expand Vim's vocabulary.

---

[Practical Vim Edit Text at the Speed of Thought - Neil, Drew.md](Practical%20Vim%20Edit%20Text%20at%20the%20Speed%20of%20Thought%20-%20Neil,%20Drew.md)

---

[Chapter 2 Normal Mode.md](Chapter%202%20Normal%20Mode.md)