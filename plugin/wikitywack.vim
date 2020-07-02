command! -nargs=1 -complete=custom,wikitywack#CompleteOpen WikityWackopen call wikitywack#Open(<f-args>)
command! WikityWackpublish call wikitywack#Publish()
command! WikityWackdiff call wikitywack#Diff()
