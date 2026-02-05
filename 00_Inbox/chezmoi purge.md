```bash
# First, see what would be removed
chezmoi purge --dry-run

# Actually remove managed files
chezmoi purge

# Then reapply from scratch
chezmoi apply
```