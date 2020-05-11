let s:initialized = 0

function! wikity_wack#ResetUndo()
    let old_undolevels = &undolevels
    set undolevels=-1
    execute "normal a \<BS>\<Esc>"
    let &undolevels = old_undolevels
    unlet old_undolevels
endfunction

function! wikity_wack#Init()
    if !has('python3')
        echoerr 'Wikity-Wack requires Vim to be compiled with Python3.'
        finish
    endif

    if !s:initialized
        python3 from wikity_wack_shim import Shim
        let s:initialized = 1
    endif
endfunction

function! wikity_wack#Open(article_name)
    call wikity_wack#Init()
    python3 Shim().article_open()
    call wikity_wack#ResetUndo()
    set nomodified
    set filetype=mediawiki
endfunction

function! wikity_wack#Publish()
    try
        call wikity_wack#Init()
        python3 Shim().article_publish()
        set nomodified
    catch /noRemoteWiki
        echoerr 'This buffer doesn''t have a remote wiki page.'
    endtry
endfunction
