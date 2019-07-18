# BookRemapper

Tool for remapping references from one book layout to another. Run with
--example to generate an configuration file.

```
remap_book.py [-h] [--example] [--flow] file
```

positional arguments:
  file           path to yml file describing book to be remapped, result will be written to this file

optional arguments:
  -h, --help     show this help message and exit
  --example, -e  generate example configuration file
  --flow, -f     output with less readible 'flow' style
  
### Example config file
```
sections:
  Chapter 1:
    old-first-page: 10
    new-first-page: 10
  Chapter 2:
    old-first-page: 21
    new-first-page: 23
  Chapter 3:
    old-first-page: 28
    new-first-page: 31
references:
  cat:
    old-pages: [9, 11, 22, 29]
  dog:
    old-pages: [2, 15, 50]
```

### Example output file
The remapped references appear as a list of ``new-references`` for each section, in addtion to having their remapped pages listed under ``new-pages``
```
sections:
  Chapter 1:
    old-first-page: 10
    new-first-page: 10
    new-references:
      cat: [11]
      dog: [15]
  Chapter 2:
    old-first-page: 21
    new-first-page: 23
    new-references:
      cat: [24]
  Chapter 3:
    old-first-page: 28
    new-first-page: 31
    new-references:
      cat: [32]
      dog: [53]
references:
  cat:
    old-pages: [9, 11, 22, 29]
    new-pages: [9, 11, 24, 32]
  dog:
    old-pages: [2, 15, 50]
    new-pages: [2, 15, 53]
```