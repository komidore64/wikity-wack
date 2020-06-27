import re
import unicodedata
import vim

class Utils():
    @classmethod
    def get_opt(cls, opt_key, prompt_text=None, ask=True):
        opt = vim.vars['wikitywack'].get(opt_key, None)

        if not opt and ask:
            opt = prompt(prompt_text or f"{opt_key}? : ", opt_key == 'password')
            vim.vars['wikitywack'][opt_key] = opt.encode()

        if type(opt) is bytes:
            opt = opt.decode()
        return opt

    @classmethod
    def get_argument(cls, arg_str):
        escapes = [
            ('\\', '')
        ]
        arg = vim.eval(arg_str)

        for s, r in escapes:
            arg = arg.replace(s, r)
        return arg

    @classmethod
    def prompt(cls, prompt_msg, is_password=False, err_on_blank=True, default=''):
        try:
            vim.eval('inputsave()')
            cmd = 'inputsecret' if is_password else 'input'
            ret = vim.eval(f"{cmd}('{cls.vim_squote_escape(prompt_msg)}', '{default}')").strip()
            if err_on_blank and not len(ret):
                vim.command('throw PromptBlankInput')
                raise
        except KeyboardInterrupt:
            vim.command('throw KeyboardInterrupt')
            raise
        finally:
            vim.eval('inputrestore()')
        return ret.strip()

    @classmethod
    def vim_squote_escape(cls, s):
        return s.replace("'", "''")

    @classmethod
    def vim_filename_escape(cls, s):
        return vim.eval(f"fnameescape('{cls.vim_squote_escape(s)}')")

    @classmethod
    def slugify(cls, s):
        """
        Thank you Django: https://docs.djangoproject.com/en/3.0/_modules/django/utils/text/#slugify
        """
        s = str(s)
        s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
        s = s.replace('/', '-')
        s = re.sub(r'[^\w\s-]', '', s).strip().lower()
        s = re.sub(r'[-\s]+', '-', s)
        return s

    @classmethod
    def get_current_article_name(cls):
        try:
            article_name = vim.current.buffer.vars['article_name'].decode()
        except KeyError:
            vim.command('throw NoRemoteWiki')
            raise
        return article_name

    @classmethod
    def setup_buffer(cls, **kwargs):
        set_opts = 'filetype=mediawiki nomodified'

        if 'append_set' in kwargs:
            set_opts += ' ' + kwargs['append_set']

        vim.command("""
            let old_undolevels = &undolevels
            set undolevels=-1
            execute "normal a \\<BS>\\<Esc>"
            let &undolevels = old_undolevels
            unlet old_undolevels
        """)
        vim.command(f"set {set_opts}")
