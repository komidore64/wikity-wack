command! -nargs=1 -complete=custom,wikitywack#CompleteOpen WikityWackopen call wikitywack#Open(<f-args>)
command! -nargs=? WikityWackpublish call wikitywack#Publish(<f-args>)
command! WikityWackdiff call wikitywack#Diff()
