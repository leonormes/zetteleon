# Introduction to fzf commandBaeldung on Linux

# Introduction to Fzf commandBaeldung on Linux

## 4\. Basic Usage

Usually, fzf is piped from the stdout of another program, such as *ps,* or *apt-cache search*. When *fzf* is not piped, it invokes *find* to recursively list all non-hidden files under the current directory and begins the search on the list of file names:

```sh
$ fzf
```

The program interface starts in fullscreen mode by default, and the search begins at the bottom. We can change the behavior using arguments:

```sh
--reverse 
        Display from the top of the screen 
--height N% 
        Use only N% height instead of full screen. 
--query PARAM 
        Begin search with PARAM as the initial query 
--multi 
        Enable multi-select with tab/shift-tab. 
-f, --filter PARAM
        Show matches for PARAM without the interactive finder
```

To start the *fzf* finder at 50% height and display files ending with *.md:*

```sh
$ fzf --reverse --multi --height 50% --query=.md$
```

To run *fzf* in script mode and disable the interactive finder:

```sh
$ fzf -f .md$
```

We can find all the available options in the [man page](https://manpages.ubuntu.com/manpages/lunar/en/man1/fzf.1.html).

### 4\.1. Shell Key Bindings

During installation, *fzf* enables three key bindings to the shell:

1. *CTRL-R:* search on recent history based on *$HISTFILE*, then return selected entry to the terminal

2. *CTRL-T:* recursively search for a filename under *$PWD*, then return selected entries to the terminal

3. *ALT-C:* recursively search for a directory name under *$PWD*, then *cd* into the selected entry

### 4\.2. Filename Autocomplete

In the terminal, we can trigger *fzf* to autocomplete filenames by typing *\*\** and then the TAB key after the term to find:

```bash
$ ls /etc/sorce**<TAB>
> source                                      
  64/3158                                     
> /etc/apt/sources.list                       
  /etc/apt/sources.list.d                     
  /etc/apt/sources.list.save
```

Notice that the argument to *ls* is incorrect at first but *fzf* returns the correct file paths.

### 4\.3. Kill Command Autocomplete

With *kill* and *fzf*, we can easily select processes to send signals to. After *kill -SIGNAL*, hit the TAB key to bring the *fzf* process finder, then select the desired processes to autocomplete the *pid* values:

```bash
$ kill -18 <TAB>
> gedit<ENTER>                                                
  55/295                                               
> user     8841     1  0 09:03 ?        00:00:01 gedit
$ kill -18 8841
```

### 4\.4. Using Different Search Modes

*fzf* supports multiple search modes. To review how *fzf* operates in each mode, let's create a plaintext file:

```bash
$ tee /tmp/fzf.in <<EOF
I mean to confound these bungers
I swallowed a bug
Was that the Primary Buffer Panel?
Captain Reynolds
EOF
```

*fzf* searches in fuzzy mode by default. When we search for the word *"bug"*, the degree of match is higher in the 2nd line of the heredoc than on the 1st line, and there is no match for the 3rd and 4th lines:

```bash
$ cat /tmp/fzf.in | fzf -f bug
I swallowed a bug
I mean to confound these bungers
```

Instead of fuzzy mode, **we can** **prefix the keyword with an apostrophe to match in exact mode:**

```bash
$ cat /tmp/fzf.in | fzf -f \'bug 
$ #cat /tmp/fzf.in | fzf -f "'bug"
I swallowed a bug
```

Lines 1 and 2 are equivalent. All characters which have special meaning in the shell must be escaped if not enclosed in quotes.

**Negation mode matches a keyword in exact mode and filters out matching lines.** We can prefix the keyword with *!* for negation:

```bash
$ cat /tmp/fzf.in | fzf -f  \!bug
I mean to confound these bungers
Was that the Primary Buffer Panel?
Captain Reynolds
```

**We can also specify if a substring appears at the beginning or at the end using *^* and *$* respectively.** This is called an anchored match:

```bash
$ cat /tmp/fzf.in | fzf -f s$
Captain Reynolds
I mean to confound these bungers
$ cat /tmp/fzf.in | fzf -f \^c
Captain Reynolds
```

We can combine multiple filters separated by a space. **A pipe separator acts as the OR operator.** The following command filters all lines that begin with "I" and that match either "man" or "ban" in fuzzy mode.

```bash
$ cat /tmp/fzf.in | fzf -f "^i ban | man"
I mean to confound these bungers
```

Note that we can use the *\+i* flag to enable case sensitive match.

## 5\. Example of Applications

Since *fzf* excels by providing an interactive interface, we can use it as a browser in different scenarios, and use its fuzzy search capability to narrow down the searches with a high error tolerance.

**The *preview* option displays the output of the** **specified command in a preview pane for the selected line**.

In a command embedded within the *preview* flag, the expression *{}* expands to the whole line, whereas *{1}* expands to the 1st column of the current line*, {2}* expands to the 2nd column, and so on. *{n}* expands the zero-based index of the line:

```bash
$ cat /tmp/fzf.in | fzf --preview 'echo line# {n}. first word: {1}. total words: \`wc -w <<< {}\`'
```

Let's view the threads of a process interactively by embedding our *ps* command in the *–preview* flag:

```bash
$ ps axo pid,rss,comm --no-headers | fzf --preview 'ps o args {1}; ps mu {1}'
```

Similarly, we can browse package dependencies, for example, in a Debian based Linux:

```bash
$ apt-cache search . | fzf --preview 'apt-cache depends {1}' 
```

We can also browse through the git commit history and view minimal information about each commit:

```bash
$ git log --oneline | fzf --preview 'git show --name-only {1}'
```

A vim plugin for *fzf* is also available. An extensive list of advanced applications can be found on the official [wiki page](https://github.com/junegunn/fzf/wiki).