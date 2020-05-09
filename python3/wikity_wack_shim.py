import vim
from wikity_wack.client import Client

class Shim():
    """
    Shim is an adapter class for interfacing Wikity-Wack's python with Vim.
    """

    def __init__(self):
        self.options = [
            'host',
            'path',
            'username',
            'password',
        ]

    def __get_config_options(self):
        unsani = vim.vars['wikity_wack']

        sanitized = {k:unsani[k].decode() for k in self.options}
        return sanitized

    def edit(self, article_name):

        opts = self.__get_config_options()
        client = Client(**opts)

        vim.current.buffer[:] = client.fetch_page(article_name).split("\n")
        vim.command("set ft=mediawiki")
