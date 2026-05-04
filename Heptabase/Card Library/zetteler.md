# zetteler

```sh
fd -e md --maxdepth 1 '^\d+' | sort | tail -n 1 | cut -c 1 | awk -F. '{print "next free parent " +1}'
```