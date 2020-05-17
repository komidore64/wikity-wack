let s:initialized = 0

let s:RequiresPython3 = 'Wikity-Wack requires Vim to be compiled with Python3 support.'
let s:NoRemoteWiki = 'This buffer is not attached to a remote wiki page.'
let s:PromptBlankInput = 'Prompt input cannot be blank.'

function! wikitywack#ErrorMessage(msg)
    echohl ErrorMsg
    redraw
    echo a:msg
    echohl None
endfunction

function! wikitywack#Init()
    if !has('python3')
        call wikitywack#ErrorMessage(s:RequiresPython3)
        finish
    endif

    if !s:initialized
        python3 from wikitywack_shim import Shim
        let s:initialized = 1
    endif
endfunction

function! wikitywack#Open(article_name)
    try
        call wikitywack#Init()
        python3 Shim().article_open()
    catch /PromptBlankInput/
        call wikitywack#ErrorMessage(s:PromptBlankInput)
    endtry
endfunction

function! wikitywack#Publish()
    try
        call wikitywack#Init()
        python3 Shim().article_publish()
    catch /NoRemoteWiki/
        call wikitywack#ErrorMessage(s:NoRemoteWiki)
    catch /PromptBlankInput/
        call wikitywack#ErrorMessage(s:PromptBlankInput)
    endtry
endfunction

function! wikitywack#Diff()
    try
        call wikitywack#Init()
        python3 Shim().article_diff()
    catch /NoRemoteWiki/
        call wikitywack#ErrorMessage(s:NoRemoteWiki)
    endtry
endfunction

function! wikitywack#CompletePageName(arglead, cmdline, cursorpos)
    try
        call wikitywack#Init()
        python3 Shim().complete_page_name()
        return l:completion_list
    catch /PromptBlankInput/
        call wikitywack#ErrorMessage(s:PromptBlankInput)
    endtry
endfunction
