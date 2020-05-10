import vim
from wikity_wack.client import Client

class Shim():
    """
    Shim is an adapter class for interfacing Wikity-Wack's python with Vim.
    """

    def _get_opt(self, opt_key, prompt=None, ask=True):
       opt = vim.vars['wikity_wack'].get(opt_key, None)

       if not opt and ask:
           opt = self._prompt(prompt or f"{opt_key}? : ", opt_key == 'password')
           vim.vars['wikity_wack'][opt_key] = opt.encode()

       if type(opt) is bytes:
           opt = opt.decode()
       return opt

    def _prompt(self, prompt_msg, is_password=False):
        try:
            vim.eval('inputsave()')
            cmd = 'inputsecret' if is_password else 'input'
            ret = vim.eval(f"{cmd}('{self._squote_escape(prompt_msg)}', '')").strip()
            if not len(ret):
                raise Exception('Prompt input cannot be blank.')
        finally:
            vim.eval('inputrestore()')
        return ret.strip()

    def _squote_escape(self, s):
        return s.replace("'", "''")

    # public

    def __init__(self):
        self.opts = dict(
            host=self._get_opt('host', "Mediawiki hostname? : "),
            username=self._get_opt('username', "Mediawiki username? : "),
            password=self._get_opt('password', "Mediawiki password? : "),
            path=self._get_opt('path', ask=False),
        )

    def edit(self, article_name):
        client = Client(**self.opts)

        vim.current.buffer[:] = client.fetch_page(article_name).split("\n")
        vim.command('set ft=mediawiki')
        vim.command(f"let b:article_name = '{self._squote_escape(article_name)}'")
