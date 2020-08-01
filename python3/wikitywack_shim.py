import argparse
import shlex
import vim

from wikitywack.client import Client
from wikitywack.utils import Utils as utils

class Shim():
    def __init__(self):
        self.opts = dict(
            host=utils.get_opt('host', 'Mediawiki hostname? : '),
            username=utils.get_opt('username', 'Mediawiki username? : '),
            password=utils.get_opt('password', 'Mediawiki password? : '),
            path=utils.get_opt('path', ask=False),
        )

    def article_open(self):
        article_name = utils.get_argument('a:article_name')
        client = Client(**self.opts)

        article = client.fetch_page(article_name)
        vim.current.buffer[:] = article.text().split("\n")
        vim.current.buffer.vars['article_name'] = utils.vim_squote_escape(article_name).encode()
        vim.command(f"file '{utils.slugify(article_name)}.wiki'")

        vim.command(f"redraw | echo 'Opening [ {article_name} ]'")
        utils.setup_buffer()


    def article_publish(self):
        article_name = utils.get_current_article_name()
        client = Client(**self.opts)
        input_str = utils.get_argument('a:input_str')

        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--summary', dest='summary')
        parser.add_argument('-n', '--no-summary', dest='summary', action='store_const', const='')
        parser.add_argument('-m', '--minor', action='store_true', dest='minor_change', default=argparse.SUPPRESS)
        parser.add_argument('-M', '--major', action='store_false', dest='minor_change', default=argparse.SUPPRESS)
        publish_args = parser.parse_args(shlex.split(input_str))

        # have we made any actual changes to the page?
        text = "\n".join(vim.current.buffer[:])
        remote_text = client.fetch_page(article_name).text()
        if text == remote_text:
            vim.command('set nomodified')
            vim.command('throw NoChangesToPublish')
            raise

        # do we need to prompt for the summary?
        try:
            summary = publish_args.summary
        except AttributeError:
            summary = utils.prompt('Summary? : ', err_on_blank=False)

        # do we need to prompt for the minor change boolean?
        try:
            minor_change = publish_args.minor_change
        except AttributeError:
            minor_change = utils.prompt('Minor change? [y/N] : ', err_on_blank=False, default='n').lower() == 'y'

        client.publish_page(article_name, text, summary, minor=minor_change)
        vim.command(f"redraw | echo 'Successfully published [ {article_name} ]'")
        vim.command('set nomodified')

    def article_diff(self):
        article_name = self._get_current_article_name()
        remote_article_title = utils.vim_filename_escape(article_name + ' - REMOTE')
        client = Client(**self.opts)

        # editing buffer
        vim.command('diffthis')

        # remote buffer
        vim.command(f"rightbelow vsplit {remote_article_title}")
        vim.command('set modifiable')
        vim.command('setlocal buftype=nofile bufhidden=delete nobuflisted')
        vim.current.buffer[:] = client.fetch_page(article_name).text().split("\n")
        utils.setup_buffer(append_set='nomodifiable')
        vim.command('diffthis')
        vim.command('wincmd t')

    def complete_open(self):
        client = Client(**self.opts)
        prefix = utils.get_argument('a:arglead')

        completion_list = [utils.vim_filename_escape(page_name) for page_name in client.match_page_names(prefix)]
        completion_list = "\n".join(completion_list)
        vim.command(f"let l:completion_list = '{completion_list}'")
