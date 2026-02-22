# GitHub - VG-dev1/fdir: Find and organize anything on your system

![rw-book-cover](https://opengraph.githubassets.com/3605e41965ab7bcb69523f0ce61dadf531cc03d1dda8881bd6661c7860eaf815/VG-dev1/fdir)

## Metadata
- Author: [[https://github.com/VG-dev1/]]
- Full Title: GitHub - VG-dev1/fdir: Find and organize anything on your system
- Category: #articles
- Summary: fdir is a tool to find and organize files on your computer using filters like date, size, name, and type. It can sort, delete, convert, and search files, even with approximate matches. You can install it easily on Windows and Linux, but it is not yet available for MacOS.
- URL: https://github.com/VG-dev1/fdir

## Full Document
### VG-dev1/fdir

main

Go to file

Code

Open more actions menu

### fdir

*Find and organize anything on your system*

[![fdir demo](https://github.com/VG-dev1/fdir/raw/main/assets/demo2.png)](https://github.com/VG-dev1/fdir/blob/main/assets/demo2.png)
[![GitHub Downloads (all assets, latest release)](https://camo.githubusercontent.com/2ca4afe36742d98003bc28a26c56a17339c2b23e6fa7b919fb1c0b0801de5d94/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f646f776e6c6f6164732f56472d646576312f666469722f746f74616c)](https://camo.githubusercontent.com/2ca4afe36742d98003bc28a26c56a17339c2b23e6fa7b919fb1c0b0801de5d94/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f646f776e6c6f6164732f56472d646576312f666469722f746f74616c)
[![Latest Release](https://camo.githubusercontent.com/c83f0222d1b17b9b8e5a1c2f92dcb8840901e615fa31e6d18d280c71c971f70d/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f762f72656c656173652f56472d646576312f66646972)](https://github.com/VG-dev1/fdir/releases)
[![GitHub Repo stars](https://camo.githubusercontent.com/3ecd48cdc71884a39fef37777780265a7c302577dd6e633c7954d2aa99382c97/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f56472d646576312f66646972)](https://camo.githubusercontent.com/3ecd48cdc71884a39fef37777780265a7c302577dd6e633c7954d2aa99382c97/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f56472d646576312f66646972)
[![GitHub License](https://camo.githubusercontent.com/23670f204af423c304587527f686c9e57c0b1887b0a3d2f41c64924f5c94f8c2/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f56472d646576312f66646972)](https://github.com/VG-dev1/fdir/blob/main/LICENSE.md)
#### Features

* List all files and folders in the current directory
* Filter files by:
	+ Last modified date (`--gt`, `--lt`)
	+ File size (`--gt`, `--lt`)
	+ Name keywords (`--keyword`, `--swith`, `--ewith`)
	+ File type/extension (`--eq`)
* Sort results by:
	+ Name, size, or modification date (`--order <field> <a|d>`)
* Use and/or
* Delete results (`--del`)
* Convert results to a different extension (`--convert`, available for the `type` operation)
* Search approximately (`--fuzzy`)
* Search the content of files
* Field highlighting in yellow (e.g. using the `modified` operation would highlight the printed dates)
	+ With partial highlighting for the `name` operation
* Hyperlinks to open matching files
* Heatmap size field letter coloring (blue -> red)
* Add .fdirignore to your directory to make fdir ignore certain files, directories or extensions

#### Examples

```
fdir modified --gt 1y --order name a  # Show files older than 1 year, in the ascending order by name
fdir size --lt 100MB --order modified d  # Show files smaller than 100MB, in the descending order by modified
fdir name --keyword report --order size a --deep  # Show files containing the "report" keyword, in the ascending order by size, and search recursively
fdir type --eq .wav --order name d --convert .mp3  # Show files with the ".wav" extension, in the descending order by name, and convert them to ".mp3"
fdir all --order modified a  # Show all files in the ascending order by modified
fdir modified --gt 1y or size --gt 1gb --del  # Show files older than 1 year old larger than 1GB, and delete them
```

#### Usage

`fdir <operation> [options] [--order <field> <a|d>]`

###### Operations

| Operation | Flags | Description |
| --- | --- | --- |
| `modified` | `--gt | --lt <time>` | Filter files by last modified date |
| `size` | `--gt | --lt <size>` | Filter files by file size |
| `name` | `--keyword | --swith | --ewith <pattern>` | Filter files by name |
| `type` | `--eq <extension>` | Filter files by file extension |
| `all` | — | List all files and directories |
| `version` | — | Display the installed version of fdir |
| `content` | `--keyword <pattern>` | Search the content of textual files |

###### Time Units (modified)

| Unit | Meaning |
| --- | --- |
| `h` | Hours |
| `d` | Days |
| `w` | Weeks |
| `m` | Months (approx. 30 days) |
| `y` | Years (approx. 365 days) |

###### Size Units (size)

| Unit | Meaning |
| --- | --- |
| `B` | Bytes |
| `KB` | Kilobytes |
| `MB` | Megabytes |
| `GB` | Gigabytes |

###### Name Flags (name)

| Flag | Description |
| --- | --- |
| `--keyword` | Filename contains the pattern |
| `--swith` | Filename starts with the pattern |
| `--ewith` | Filename ends with the pattern |

###### Type Flags (type)

| Flag | Description |
| --- | --- |
| `--eq` | Match exact file extension (include the dot, e.g. `.py`) |

###### Additional flags

| Flag | Description |
| --- | --- |
| `--order` | Sort files in a specific order |
| `--deep` | Search recursively |
| `--top` | Print only the first certain amount of matches |
| `--fuzzy` | Search approximately (make fdir support typos) |

#### Installation

##### Windows

1. Download the "fdir.exe" file from the Releases tab.
2. Create a new folder in %USERPROFILE% on your computer.
3. Paste the downloaded "fdir.exe" file into that folder.
4. Copy the path of that folder.
5. Put the path of that folder into your system's PATH (run `setx PATH "%PATH%;C:\path\to\fdir_folder"` (replace the path with your actual path)).

##### Linux

1. Download the "fdir" file from the Releases tab.
2. Go to the downloaded "fdir" file's folder (run `cd path/to/your/folder` (replace the path with your actual path)).
3. Copy that path into `~/.local/bin` (run `cp fdir ~/.local/bin`).

##### MacOS

Sorry, not available yet.
