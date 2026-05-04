# CLI ZET

# CLI ZET

This command gives me a way to search all my notes. With `ctrl-o` I can open the note in nvim

## Pre-requesite

- fzf

- mdcat

- fdfind

- sd

- ripgrep

- nvim

```sh
fzf --preview 'mdcat --style=plain --color=always {}' --bind "ctrl-o:execute(nvim {})" < <(fd -e md . $ZET_ROOT)
```