let s:initialized = 0

function! wikity_wack#init()
    if !has('python3')
        echo 'Error: Wikity-Wack requires Vim to be compiled with python3 support.'
        finish
    endif

    if !s:initialized
        python3 from wikity_wack_shim import Shim
        let s:initialized = 1
    endif
endfunction

function! wikity_wack#edit(article)
    call wikity_wack#init()
    python3 Shim().edit(vim.eval('a:article'))
endfunction
