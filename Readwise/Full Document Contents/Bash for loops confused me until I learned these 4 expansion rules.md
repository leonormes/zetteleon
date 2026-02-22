# Bash for loops confused me until I learned these 4 expansion rules

![rw-book-cover](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/12/bash-terminal-icon-inside-an-infinity-loop-surrounded-by-parameter-expansion-symbols.png?w=1600&h=900&fit=crop)

## Metadata
- Author: [[Graeme Peacock]]
- Full Title: Bash for loops confused me until I learned these 4 expansion rules
- Category: #articles
- Summary: Bash arrays behave differently depending on how you quote them in loops. Using quotes around "${my_arr[@]}" keeps array elements intact, while leaving them unquoted causes word splitting that breaks elements apart. Knowing this helps avoid unexpected results when processing arrays in Bash scripts.
- URL: https://www.howtogeek.com/bash-for-loops-confused-me-until-i-learned-these-expansion-rules/

## Full Document
![Bash terminal icon inside an infinity loop surrounded by parameter expansion symbols.](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/12/bash-terminal-icon-inside-an-infinity-loop-surrounded-by-parameter-expansion-symbols.png?&fit=crop&w=1600&h=900) 
Have you ever been confused by the different ways to use [Bash arrays](https://www.howtogeek.com/managing-data-with-your-bash-scripts-is-easy-when-you-know-arrays/)? Or perhaps you're just [learning Bash](https://www.howtogeek.com/easy-tips-you-can-do-to-polish-your-bash-scripts/), and they're next on your list? Bash arrays can act strangely depending on how you use them. I will explain the confusing circumstances you may encounter when doing so.

If you've written Bash scripts in the past, you've probably encountered the [for loop](https://www.howtogeek.com/815778/bash-for-loops-examples/). Their syntax is a little awkward, and the different approaches confused me until I understood the four fundamental rules.

 ![Tux, the Linux mascot, sitting with a laptop in front of a large terminal window.-1](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/10/tux-the-linux-mascot-sitting-with-a-laptop-in-front-of-a-large-terminal-window-1.png?q=49&fit=crop&w=220&h=182&dpr=2) 
Let's look at a problem. The following script processes an array in two different ways—quoted: `"${my_arr[@]}"` and unquoted: `${my_arr[@]}`:

```
my_arr=("one a" "two b")

echo 'Using ${my_arr[@]}:'
for item in ${my_arr[@]}; do
  echo "  $item"
done

echo -e "\n-----\n"

echo 'Using "${my_arr[@]}":'
for item in "${my_arr[@]}"; do
  echo "  $item"
done
```

   ![A terminal window compares quoted and unquoted Bash array expansion. The unquoted version splits into four words, while the quoted version preserves the two original array elements.](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/12/a-terminal-window-compares-quoted-and-unquoted-bash-array-expansion-the-unquoted-version-splits-into-four-words-while-the-quoted-version-preserves-the-two-original-array-elements.png?q=70&fit=crop&w=825&dpr=1) 
There are two items in the array, so why does `${my_arr[@]}` (without quotes) display four? The reason is called "word splitting," and it's the topic I'll cover today.

 ![HTG Wrapped Full Calendar - December 24](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/12/dec24-notitle.png?q=49&fit=crop&w=220&h=182&dpr=2) 
####  A quick primer on using a for loop

For those unfamiliar with Bash arrays and for loops, here's a quick rundown. If you're an experienced Bash scripter, you can skip this section.

This is a string: "foo bar." It's enclosed in quotes ([single or double](https://www.howtogeek.com/29980/whats-the-difference-between-single-and-double-quotes-in-the-bash-shell/)) because [spaces are ambiguous](https://www.howtogeek.com/850124/spaces-in-filenames-on-linux/) in computer programs. Using quotes explicitly defines the boundaries for text-based values.

Bash may treat "foo bar" as a single word, depending on the context. Bash [defines a word](https://www.gnu.org/software/bash/manual/bash.html#index-word) as "a sequence of characters treated as a unit by the shell." If you hear the term "word" in Bash, it doesn't mean English words separated by spaces. I will use the terms "Bash words" and "English words" to distinguish them.

This is an array: `my_arr=("foo" "bar")`. It's a sequence of values (two in this case) that are accessed one after the other.

A "for" loop is often a declaration of intent to process an array, cycling (iterating) over it, allowing you to perform actions on each item individually.

```
for item in "${my_arr[@]}"; do
  echo "$item"
done
```

   ![A terminal window displays foo and bar on separate lines, showing the output of a basic for loop iterating over an array.](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/12/a-terminal-window-displays-foo-and-bar-on-separate-lines-showing-the-output-of-a-basic-for-loop-iterating-over-an-array.png?q=70&fit=crop&w=825&dpr=1) 
"item" is called an iterator or loop variable. As the for loop iterates over each array value, it gets placed into "item," which you can then use to perform actions.

There are several ways to loop over an array, but this is the most common.

There is also another way to access items in arrays using a "\*"—`"${my_arr[*]}"`—which I will get into later.

####  Parameter expansion splits the array up

In Bash, a [parameter](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameters.html#Shell-Parameters-1) is an entity that stores a value—e.g., a [variable](https://www.howtogeek.com/442332/how-to-work-with-variables-in-bash/) is a parameter. A [parameter *expansion*](https://www.howtogeek.com/bash-string-tricks-that-fix-common-scripting-headaches/) is essentially the *evaluation* of a parameter—for example, turning `$foo` into "value" at runtime.

In terms of arrays, given `my_arr=("one a" "two b")`, `"${my_arr[@]}"` expands "my\_arr" into "one a" and "two b." When we use this array in a for loop, each Bash word ("one a" and "two b") gets assigned to the loop variable.

Let's look at an example:

```
my_arr=("one a" "two b")

echo 'Using "${my_arr[@]}":'
for item in "${my_arr[@]}"; do
  echo "  $item"
done

echo -e "\n-----\n"

echo 'Using "${my_arr[*]}":'
for item in "${my_arr[*]}"; do
  echo "  $item"
done
```

   ![A terminal window compares two quoted array expansions. The at-sign version outputs one a and two b on separate lines. The asterisk version outputs one a two b as a single line.](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/12/a-terminal-window-compares-two-quoted-array-expansions-the-at-sign-version-outputs-one-a-and-two-b-on-separate-lines-the-asterisk-version-outputs-one-a-two-b-as-a-single-line.png?q=70&fit=crop&w=825&dpr=1) 
In the first loop, using the "@" expands the array into separate values, delineated by their string boundaries (e.g., "one a" and "two b").

In the second loop, using the "\*" expands the array into one value—a string.

The use of double quotes around each array is crucial here, because, as we shall see next, Bash does something different if they're unquoted.

####  Word splitting further splits up each Bash word

We've seen what happens when we surround array parameters with double quotes, but what happens when we exclude them? Let's take a look:

```
my_arr=("one a" "two b")

echo 'Using ${my_arr[@]}:'
for item in ${my_arr[@]}; do
  echo "  $item"
done

echo -e "\n-----\n"

echo 'Using ${my_arr[*]}:'
for item in ${my_arr[*]}; do
  echo "  $item"
done
```

   ![A terminal window compares two unquoted array expansions. Both at-sign and asterisk versions output one, a, two, and b on separate lines, showing identical word splitting behavior.](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/12/a-terminal-window-compares-two-unquoted-array-expansions-both-at-sign-and-asterisk-versions-output-one-a-two-and-b-on-separate-lines-showing-identical-word-splitting-behavior.png?q=70&fit=crop&w=825&dpr=1) 
Both arrays output four items, but why? First, recall that parameter expansion will split (expand) the array around (Bash) word boundaries—for example, "one a" and "two b" produces two results. However, when these array parameters lack double quotes, Bash subjects them to further processing, called *word splitting*.

Word splitting simply means splitting each (Bash) word up. For example, "one a" and "two b" are further split into "one," "a," "two," and "b." By default, Bash splits them on any whitespace character:

```
my_arr=($'one\na' $'two\tb' "three c")

for item in ${my_arr[@]}; do
  echo "$item"
done
```

   ![A terminal window displays one, a, two, b, three, and c on separate lines, demonstrating that word splitting occurs on newlines, tabs, and spaces.](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/12/a-terminal-window-displays-one-a-two-b-three-and-c-on-separate-lines-demonstrating-that-word-splitting-occurs-on-newlines-tabs-and-spaces.png?q=70&fit=crop&w=825&dpr=1) 
`$'...'` is a special quotation type called [ANSI-C quoting](https://www.gnu.org/software/bash/manual/html_node/ANSI_002dC-Quoting.html#ANSI_002dC-Quoting-1). When using these, Bash replaces [escape sequence](https://tldp.org/HOWTO/Bash-Prompt-HOWTO/bash-prompt-escape-sequences.html) characters (like "\n") with their literal equivalents (e.g., a newline character). In addition, "\n" (newline) and "\t" (tab) are considered whitespace characters.

However, you can specify which characters to split words upon using the [IFS](https://www.baeldung.com/linux/ifs-shell-variable) (Internal Field Separator) variable:

```
my_arr=('one+a' 'two+b')

echo 'Default IFS:'
for item in ${my_arr[@]}; do
  echo "  $item"
done

echo -e "\n-----\n"

echo 'IFS="+":'  # Split words using "+".
IFS="+"
for item in ${my_arr[@]}; do
  echo "  $item"
done
```

   ![A terminal window compares word splitting with different IFS values. With default IFS, one+a and two+b remain intact. With IFS set to plus, they split into one, a, two, and b on separate lines.](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/12/a-terminal-window-compares-word-splitting-with-different-ifs-values-with-default-ifs-one-a-and-two-b-remain-intact-with-ifs-set-to-plus-they-split-into-one-a-two-and-b-on-separate-lines.png?q=70&fit=crop&w=825&dpr=1) 
The confusing part is that "word splitting" is a distinct process, and if you observe the [array length](https://itsfoss.com/bash-array-length/) ("#"), you'll see it's determined by the number of Bash words (array elements) and not split words.

```
my_arr=('one a' 'two b')

echo ${#my_arr[@]}
echo "${#my_arr[@]}"
echo ${#my_arr[*]}
echo "${#my_arr[*]}"
```

   ![A terminal window displays the number 2 four times on separate lines, demonstrating that array length is consistent regardless of quoting or expansion method.](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/12/a-terminal-window-displays-the-number-2-four-times-on-separate-lines-demonstrating-that-array-length-is-consistent-regardless-of-quoting-or-expansion-method.png?q=70&fit=crop&w=825&dpr=1) 
 ![A terminal window displaying sample Bash script outputs, accompanied by shell and .sh icons.](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/11/a-terminal-window-displaying-sample-bash-script-outputs-accompanied-by-shell-and-sh-icons.png?q=49&fit=crop&w=220&h=182&dpr=2) 
All parameter (array) forms you've seen today expand into something. Only the quoted `"${my_arr[*]}"` expands elements into a single string, but the rest expand into individual array items. All unquoted parameters (e.g., `${my_arr[@]}`) undergo further processing—aka (Bash) word splitting.

|  |  |  |
| --- | --- | --- |
| Type | Expands to... | Word splitting |
| `"${my_arr[@]}"` | Multiple (Bash) words | No |
| `"${my_arr[*]}"` | One (Bash) word | No |
| `${my_arr[@]}` | Multiple (Bash) words | Yes |
| `${my_arr[*]}` | Multiple (Bash) words | Yes |

Remember a "word" is a sequence of contiguous characters, not necessarily English words separated by spaces.

You may also have noticed that unquoted `${my_arr[@]}` and `${my_arr[*]}` produce the same result.

In closing, most of the time you will use `"${my_arr[@]}"` (with quotes), because it acts like a typical array, but it's important to know how quotations affect parameters. If you fail to quote your array, you may find for loops don't act as you expect.

These rules also apply to the `$@` and `$*` [special parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html) (aka arguments for functions).

 ![Tux, the Linux mascot, wearing sunglasses and peeking from behind a large terminal window displaying globbing commands.](https://static0.howtogeekimages.com/wordpress/wp-content/uploads/2025/11/tux-the-linux-mascot-wearing-sunglasses-and-peeking-from-behind-a-large-terminal-window-displaying-globbing-commands.png?q=49&fit=crop&w=220&h=182&dpr=2)
