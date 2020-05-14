let s:initialized = 0

let s:RequiresPython3 = 'Wikity-Wack requires Vim to be compiled with Python3 support.'
let s:NoRemoteWiki = 'This buffer is not attached to a remote wiki page.'
let s:PromptBlankInput = 'Prompt input cannot be blank.'

function! wikity_wack#ErrorMessage(msg)
    echohl ErrorMsg
    redraw
    echo a:msg
    echohl None
endfunction

function! wikity_wack#Init()
    if !has('python3')
        call wikity_wack#ErrorMessage(s:RequiresPython3)
        finish
    endif

    if !s:initialized
        python3 from wikity_wack_shim import Shim
        let s:initialized = 1
    endif
endfunction

function! wikity_wack#Open(article_name)
    try
        call wikity_wack#Init()
        python3 Shim().article_open()
    catch /PromptBlankInput/
        call wikity_wack#ErrorMessage(s:PromptBlankInput)
    endtry
endfunction

function! wikity_wack#Publish()
    try
        call wikity_wack#Init()
        python3 Shim().article_publish()
    catch /NoRemoteWiki/
        call wikity_wack#ErrorMessage(s:NoRemoteWiki)
    catch /PromptBlankInput/
        call wikity_wack#ErrorMessage(s:PromptBlankInput)
    endtry
endfunction

function! wikity_wack#Diff()
    try
        call wikity_wack#Init()
        python3 Shim().article_diff()
    catch /NoRemoteWiki/
        call wikity_wack#ErrorMessage(s:NoRemoteWiki)
    endtry
endfunction
