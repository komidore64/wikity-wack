import vim
from wikitywack.client import Client

class Shim():
    """
    Shim is an adapter class for interfacing Wikity-Wack's python with Vim.
    """

    def _get_opt(self, opt_key, prompt_text=None, ask=True):
       opt = vim.vars['wikitywack'].get(opt_key, None)

       if not opt and ask:
           opt = self._prompt(prompt_text or f"{opt_key}? : ", opt_key == 'password')
           vim.vars['wikitywack'][opt_key] = opt.encode()

       if type(opt) is bytes:
           opt = opt.decode()
       return opt

    def _get_argument(self, arg_str):
        escapes = [
            ('\ ', ' ')
        ]
        arg = vim.eval(arg_str)

        for s, r in escapes:
            arg = arg.replace(s, r)
        return arg

    def _prompt(self, prompt_msg, is_password=False, err_on_blank=True, default=''):
        try:
            vim.eval('inputsave()')
            cmd = 'inputsecret' if is_password else 'input'
            ret = vim.eval(f"{cmd}('{self._squote_escape(prompt_msg)}', '{default}')").strip()
            if err_on_blank and not len(ret):
                vim.command('throw PromptBlankInput')
                raise
        except KeyboardInterrupt:
            vim.command('throw KeyboardInterrupt')
            raise
        finally:
            vim.eval('inputrestore()')
        return ret.strip()

    def _squote_escape(self, s):
        return s.replace("'", "''")

    def _filename_escape(self, s):
        return vim.eval(f"fnameescape('{self._squote_escape(s)}')")

    def _get_current_article_name(self):
        try:
            article_name = vim.current.buffer.vars['article_name'].decode()
        except KeyError:
            vim.command('throw NoRemoteWiki')
            raise
        return article_name

    def _setup_buffer(self, **kwargs):
        set_opts = 'filetype=mediawiki nomodified buftype=nowrite'

        if 'append_set' in kwargs:
            set_opts += ' ' + kwargs['append_set']

        vim.command("""
            let old_undolevels = &undolevels
            set undolevels=-1
            execute "normal a \<BS>\<Esc>"
            let &undolevels = old_undolevels
            unlet old_undolevels
        """)
        vim.command(f"set {set_opts}")

    # public functions

    def __init__(self):
        self.opts = dict(
            host=self._get_opt('host', 'Mediawiki hostname? : '),
            username=self._get_opt('username', 'Mediawiki username? : '),
            password=self._get_opt('password', 'Mediawiki password? : '),
            path=self._get_opt('path', ask=False),
        )

    def article_open(self):
        article_name = self._get_argument('a:article_name')
        client = Client(**self.opts)

        article = client.fetch_page(article_name)
        vim.current.buffer[:] = article.text().split("\n")
        vim.current.buffer.vars['article_name'] = self._squote_escape(article_name).encode()
        vim.command(f"file '{self._squote_escape(article_name)}'")

        vim.command(f"redraw | echo 'Opening [ {article_name} ]'")
        self._setup_buffer()


    def article_publish(self):
        article_name = self._get_current_article_name()
        client = Client(**self.opts)

        text = "\n".join(vim.current.buffer[:])
        remote_text = client.fetch_page(article_name).text()
        if text == remote_text:
            vim.command('throw NoChangesToPublish')
            raise
        summary = self._prompt('Summary? : ', err_on_blank=False)
        minor_change = self._prompt('Minor change? [y/N] : ', err_on_blank=False, default='n').lower() == 'y'
        client.publish_page(article_name, text, summary, minor=minor_change)

        vim.command(f"redraw | echo 'Successfully published [ {article_name} ]'")
        vim.command('set nomodified')

    def article_diff(self):
        article_name = self._get_current_article_name()
        remote_article_title = self._filename_escape(article_name + ' - REMOTE')
        client = Client(**self.opts)

        # editing buffer
        vim.command('diffthis')

        # remote buffer
        vim.command(f"rightbelow vsplit {remote_article_title}")
        vim.command('set modifiable')
        vim.command('setlocal buftype=nofile bufhidden=delete nobuflisted')
        vim.current.buffer[:] = client.fetch_page(article_name).text().split("\n")
        self._setup_buffer(append_set='nomodifiable')
        vim.command('diffthis')
        vim.command('wincmd t')

    def complete_page_name(self):
        client = Client(**self.opts)
        prefix = self._get_argument('a:arglead')

        completion_list = "\n".join([self._filename_escape(page_name) for page_name in client.match_page_names(prefix)])
        vim.command(f"let l:completion_list = '{completion_list}'")
