---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:40+00:00
title: Introduction to fzf commandBaeldung on Linux
---

## Introduction to Fzf commandBaeldung on Linux

## Introduction to Fzf commandBaeldung on Linux

### 4\. Basic Usage

Usually, fzf is piped from the stdout of another program, such as _ps,_ or _apt-cache search_. When _fzf_ is not piped, it invokes _find_ to recursively list all non-hidden files under the current directory and begins the search on the list of file names:

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

To start the _fzf_ finder at 50% height and display files ending with _.md:_

```sh
$ fzf --reverse --multi --height 50% --query=.md$
```

To run _fzf_ in script mode and disable the interactive finder:

```sh
$ fzf -f .md$
```

We can find all the available options in the [man page](https://manpages.ubuntu.com/manpages/lunar/en/man1/fzf.1.html).

#### 4\.1. Shell Key Bindings

During installation, _fzf_ enables three key bindings to the shell:

1. _CTRL-R:_ search on recent history based on _$HISTFILE_, then return selected entry to the terminal
2. _CTRL-T:_ recursively search for a filename under _$PWD_, then return selected entries to the terminal
3. _ALT-C:_ recursively search for a directory name under _$PWD_, then _cd_ into the selected entry

#### 4\.2. Filename Autocomplete

In the terminal, we can trigger _fzf_ to autocomplete filenames by typing _\*\*_ and then the TAB key after the term to find:

```bash
$ ls /etc/sorce<TAB>
> source                                      
  64/3158                                     
> /etc/apt/sources.list                       
  /etc/apt/sources.list.d                     
  /etc/apt/sources.list.save
```

Notice that the argument to _ls_ is incorrect at first but _fzf_ returns the correct file paths.

#### 4\.3. Kill Command Autocomplete

With _kill_ and _fzf_, we can easily select processes to send signals to. After _kill -SIGNAL_, hit the TAB key to bring the _fzf_ process finder, then select the desired processes to autocomplete the _pid_ values:

```bash
$ kill -18 <TAB>
> gedit<ENTER>                                                
  55/295                                               
> user     8841     1  0 09:03 ?        00:00:01 gedit
$ kill -18 8841
```

#### 4\.4. Using Different Search Modes

_fzf_ supports multiple search modes. To review how _fzf_ operates in each mode, let's create a plaintext file:

```bash
$ tee /tmp/fzf.in <<EOF
I mean to confound these bungers
I swallowed a bug
Was that the Primary Buffer Panel?
Captain Reynolds
EOF
```

_fzf_ searches in fuzzy mode by default. When we search for the word _"bug"_, the degree of match is higher in the 2nd line of the heredoc than on the 1st line, and there is no match for the 3rd and 4th lines:

```bash
$ cat /tmp/fzf.in | fzf -f bug
I swallowed a bug
I mean to confound these bungers
```

Instead of fuzzy mode, we can prefix the keyword with an apostrophe to match in exact mode:

```bash
$ cat /tmp/fzf.in | fzf -f \'bug 
$ #cat /tmp/fzf.in | fzf -f "'bug"
I swallowed a bug
```

Lines 1 and 2 are equivalent. All characters which have special meaning in the shell must be escaped if not enclosed in quotes.

Negation mode matches a keyword in exact mode and filters out matching lines. We can prefix the keyword with _!_ for negation:

```bash
$ cat /tmp/fzf.in | fzf -f  \!bug
I mean to confound these bungers
Was that the Primary Buffer Panel?
Captain Reynolds
```

We can also specify if a substring appears at the beginning or at the end using _^_ and _$_ respectively. This is called an anchored match:

```bash
$ cat /tmp/fzf.in | fzf -f s$
Captain Reynolds
I mean to confound these bungers
$ cat /tmp/fzf.in | fzf -f \^c
Captain Reynolds
```

We can combine multiple filters separated by a space. A pipe separator acts as the OR operator. The following command filters all lines that begin with "I" and that match either "man" or "ban" in fuzzy mode.

```bash
$ cat /tmp/fzf.in | fzf -f "^i ban | man"
I mean to confound these bungers
```

Note that we can use the _\+i_ flag to enable case sensitive match.

### 5\. Example of Applications

Since _fzf_ excels by providing an interactive interface, we can use it as a browser in different scenarios, and use its fuzzy search capability to narrow down the searches with a high error tolerance.

The _preview_ option displays the output of the specified command in a preview pane for the selected line.

In a command embedded within the _preview_ flag, the expression _{}_ expands to the whole line, whereas _{1}_ expands to the 1st column of the current line*, {2}* expands to the 2nd column, and so on. _{n}_ expands the zero-based index of the line:

```bash
$ cat /tmp/fzf.in | fzf --preview 'echo line# {n}. first word: {1}. total words: \`wc -w <<< {}\`'
```

Let's view the threads of a process interactively by embedding our _ps_ command in the _–preview_ flag:

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

A vim plugin for _fzf_ is also available. An extensive list of advanced applications can be found on the official [wiki page](https://github.com/junegunn/fzf/wiki).
