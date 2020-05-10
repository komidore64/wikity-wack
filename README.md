# Wikity-Wack

Make MediaWiki edits in VIM!

## Requirements

- Vim compiled with Python 3 support (`vim --version | grep +python3`)
- `mwclient` Python module installed (`pip install mwclient` or use your
  distro's package manager)

## Usage

### **:WWedit [article-name]**

Open the given article into the current buffer for editing

```vim
:WWedit EXVSMBON/Gundam
```


## Installation

**Wikity-Wack** is Vundle-compatible so just add the following to your plugin list:

```vim
Plugin 'komidore64/wikity-wack'
```

## Configuration

```vim
let g:wikity_wack = {
    \ 'host': 'dustloop.com',
    \ 'path': '/wiki/',
    \ 'username': 'komidore64', }
```

You can put `password` in there if you want, but if you don't
(recommended) **Wikity-Wack** will prompt for your password.

## Development TODO

### Main Functionality

- ~~fetch an article by name and populate it into the current buffer~~
- publish the current buffer contents to a mediawiki page
- diff the current buffer contents with a mediawiki page
- open the current buffer contents in a preview window
- Vim documentation / help

### nice-to-have

- store configurations for multiple mediawiki sites
- anonymous editing from sites that allow it

## Friends

This plugin works nicely with
[chikamichi/mediawiki.vim](https://github.com/chikamichi/mediawiki.vim)
for beautiful syntax highlighting!

## Inspirations

- [aquach/vim-mediawiki-editor](https://github.com/aquach/vim-mediawiki-editor)

## Contributing

This is my first vim plugin, but I welcome input, suggestions, bugs,
and/or fixes!
