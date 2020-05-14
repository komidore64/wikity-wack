# Wikity-Wack

![GitHub](https://img.shields.io/github/license/komidore64/wikity-wack)
![GitHub repo size](https://img.shields.io/github/repo-size/komidore64/wikity-wack)
![Vundle Compatible](https://img.shields.io/badge/Vundle.vim-compatible-yellow)

Make MediaWiki edits in VIM!

## Requirements

- Vim compiled with Python 3 support (`vim --version | grep +python3`)
- `mwclient` Python module installed (`pip install mwclient` or use your
  distro's package manager)

## Usage

### **:WikityWackopen [article-name]**

Open the given article into the current buffer for editing

```vim
:WikityWackopen EXVSMBON/Gundam
```

### **:WikityWackpublish**

Publish the contents of the current buffer to the same wiki page name you
opened.

Errors when this is run in a buffer that has not been previously attached
to a remote wiki page with `:WikityWackopen`.

### **:WikityWackdiff**

Opens a vimdiff split of the current buffer with the version of what is
currently on the remote wiki page. The buffer containing the remote wiki
page contents is unmodifiable to avoid any accidental changes.

When you're done, close the `<article_name> - REMOTE` buffer and run
`:diffoff` in your editing buffer to turn off vim's diff settings.

Errors when this is run in a buffer that has not been previously attached
to a remote wiki page with `:WikityWackopen`.

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

```
Mediawiki password? : ************************
```

## Development TODO

### Main Functionality

- ~~fetch an article by name and populate it into the current buffer~~
- ~~publish the current buffer contents to a mediawiki page~~
- ~~diff the current buffer contents with a mediawiki page~~
- open the current buffer contents in a preview window
- Vim documentation / help

### nice-to-have

- store configurations for multiple mediawiki sites
- anonymous editing from sites that allow it
- tab-completion for articles to edit

## Friends

This plugin works nicely with
[chikamichi/mediawiki.vim](https://github.com/chikamichi/mediawiki.vim)
for beautiful syntax highlighting!

## Inspirations

- [aquach/vim-mediawiki-editor](https://github.com/aquach/vim-mediawiki-editor)

## Contributing

This is my first vim plugin, but I welcome input, suggestions, bugs,
and/or fixes!
