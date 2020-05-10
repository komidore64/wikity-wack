import vim
from wikity_wack.client import Client

class Shim():
    """
    Shim is an adapter class for interfacing Wikity-Wack's python with Vim.
    """

    def _get_config_options(self):
        unsani = vim.vars['wikity_wack']

        sanitized = {k:unsani[k].decode() for k in self.options}
        return sanitized

    def _squote_escape(self, s):
        return s.replace("'", "''")

    # public

    def __init__(self):
        self.options = [
            'host',
            'path',
            'username',
            'password',
        ]

    def edit(self, article_name):
        client = Client(**self._get_config_options())

        vim.current.buffer[:] = client.fetch_page(article_name).split("\n")
        vim.command("set ft=mediawiki")
        vim.command(f"let b:article_name = '{self._squote_escape(article_name)}'")
