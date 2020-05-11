import mwclient

class Client():

    def __init__(self, host, username, password, **kwargs):
        conn_args = dict(host=host)

        if 'path' in kwargs:
            conn_args['path'] = kwargs['path']

        self.connection = mwclient.Site(**conn_args)
        self.connection.login(username, password)

    def fetch_page(self, article_name):
        return self.connection.Pages[article_name]

    def publish_page(self, article_name, text, summary, **kwargs):
        args = {
            'text': text,
            'summary': summary,
        }

        if 'minor' in kwargs:
            args['minor'] = kwargs['minor']

        article = self.fetch_page(article_name)
        article.save(**args)
