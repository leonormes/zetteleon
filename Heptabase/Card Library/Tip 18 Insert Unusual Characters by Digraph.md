## Tip 18 Insert Unusual Characters by Digraph

While Vim allows us to insert any character by its numeric code, these can be hard to remember and awkward to type. We can also insert unusual characters as digraphs: pairs of characters that are easy to remember.

Digraphs are easy to use. From Insert mode, we just type <C-k>{char1}{char2}. So if we wanted to insert the "¿" character, which is represented by the digraph ?I, we would simply type <C-k>?I.

The character pairs that make up a digraph are chosen to be descriptive, making them easier to remember or even guess. For example, the double-angle quotation marks " and " are represented by the digraphs << and >>; the vulgar (or common) fractions ½, ¼, and ¾ are represented by the digraphs 12, 14, and 34, respectively. The default set of digraphs that ship with Vim follows certain conventions, which are summarized under digraphs-default[ⓘ](http://vimhelp.appspot.com/digraph.txt.html#digraphs-default).

We can view a list of the available digraphs by running :digraphs, but the output of this command is difficult to digest. A more usable list can be found by looking up digraph-table[ⓘ](http://vimhelp.appspot.com/digraph.txt.html#digraph-table).