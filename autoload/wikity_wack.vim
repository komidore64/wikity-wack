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
        echo 'Error: Wikity-Wack requires Vim to be compiled with python3 support.'
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
endfunction

function! wikity_wack#Publish()
    call wikity_wack#Init()
    python3 Shim().article_publish()
    set nomodified
endfunction
