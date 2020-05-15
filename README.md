# WikityWack

![GitHub](https://img.shields.io/github/license/komidore64/wikitywack)
![GitHub repo size](https://img.shields.io/github/repo-size/komidore64/wikitywack)
![Vundle Compatible](https://img.shields.io/badge/Vundle.vim-compatible-yellow)

Make MediaWiki edits in Vim!

## Requirements

- Vim compiled with Python 3 support (`vim --version | grep +python3`)
- `mwclient` Python module installed (`pip install mwclient` or use your
  distro's package manager)

## Usage

### `:WikityWackopen <article-name>`

Open the named wiki page in the current buffer for editing.

example:

```vim
:WikityWackopen EXVSMBON/Gundam
```

### `:WikityWackpublish`

Publish the contents of the current buffer to the wiki page you opened.

Errors when this is run in a buffer that has not been previously attached
to a remote wiki page with `:WikityWackopen`.

### `:WikityWackdiff`

Opens a vimdiff split of the current buffer with the version of what is
currently on the remote wiki page.

Errors when this is run in a buffer that has not been previously attached
to a remote wiki page with `:WikityWackopen`.

When you're done, close the `<article_name> - REMOTE` buffer and run
`:diffoff` in your editing buffer to turn off vim's diff settings.

## Installation

**Wikity-Wack** is [Vundle-compatible](https://github.com/VundleVim/Vundle.vim) so just add the following to your
plugin list:

```vim
Plugin 'komidore64/wikitywack'
```

## Configuration

```vim
let g:wikitywack = {
    \ 'host': 'dustloop.com',
    \ 'path': '/wiki/',
    \ 'username': 'komidore64', }
```

You can put `password` in there if you want. If you don't put your
password in your `~/.vimrc` (recommended) **Wikity-Wack** will prompt for
it and save it for the rest of the vim session:

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
