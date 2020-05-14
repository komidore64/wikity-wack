import vim
from wikity_wack.client import Client

class Shim():
    """
    Shim is an adapter class for interfacing Wikity-Wack's python with Vim.
    """

    def _get_opt(self, opt_key, prompt_text=None, ask=True):
       opt = vim.vars['wikity_wack'].get(opt_key, None)

       if not opt and ask:
           opt = self._prompt(prompt_text or f"{opt_key}? : ", opt_key == 'password')
           vim.vars['wikity_wack'][opt_key] = opt.encode()

       if type(opt) is bytes:
           opt = opt.decode()
       return opt

    def _prompt(self, prompt_msg, is_password=False, err_on_blank=True, default=''):
        try:
            vim.eval('inputsave()')
            cmd = 'inputsecret' if is_password else 'input'
            ret = vim.eval(f"{cmd}('{self._squote_escape(prompt_msg)}', '{default}')").strip()
            vim.eval('inputrestore()')
            if err_on_blank and not len(ret):
                vim.command('throw PromptBlankInput')
                raise
        finally:
            vim.eval('inputrestore()')
        return ret.strip()

    def _squote_escape(self, s):
        return s.replace("'", "''")

    def _filename_escape(self, s):
        return vim.eval(f"fnameescape('{self._squote_escape(s)}')")

    # public functions

    def __init__(self):
        self.opts = dict(
            host=self._get_opt('host', "Mediawiki hostname? : "),
            username=self._get_opt('username', "Mediawiki username? : "),
            password=self._get_opt('password', "Mediawiki password? : "),
            path=self._get_opt('path', ask=False),
        )

    def article_open(self):
        article_name = vim.eval('a:article_name')

        client = Client(**self.opts)
        article = client.fetch_page(article_name)
        vim.current.buffer[:] = article.text().split("\n")
        vim.current.buffer.vars['article_name'] = self._squote_escape(article_name).encode()

        vim.command(f"redraw | echo \"Opening [ {article_name} ]\"")

        # buffer setup
        vim.command('let old_undolevels = &undolevels')
        vim.command('set undolevels=-1')
        vim.command('execute "normal a \<BS>\<Esc>"')
        vim.command('let &undolevels = old_undolevels')
        vim.command('unlet old_undolevels')
        vim.command('set nomodified filetype=mediawiki')

    def article_publish(self):
        try:
            article_name = vim.current.buffer.vars['article_name'].decode()
        except KeyError:
            vim.command('throw NoRemoteWiki')
            raise

        client = Client(**self.opts)
        text = "\n".join(vim.current.buffer[:])
        summary = self._prompt('Summary? : ', err_on_blank=False)
        minor_change = self._prompt('Minor change? [y/N] : ', err_on_blank=False, default='n').lower() == 'y'
        client.publish_page(article_name, text, summary, minor=minor_change)

        vim.command(f"redraw | echo \"Successfully published [ {article_name} ]\"")

        vim.command("set nomodified")
