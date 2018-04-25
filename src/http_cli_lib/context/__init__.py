class Context(object):

    def __init__(self, url=None, spec=None):
        self.url = url
        self.action = None
        self.headers = {}
        self.querystring_params = {}
        self.body_params = {}
        self.body_json_params = {}
        self.options = {}
        self.should_exit = False

        if not self.url:
            self.url = 'http://localhost:8000'

        if not self.action:
            self.action = 'GET'

    def __eq__(self, other):
        return (self.url == other.url and
                self.headers == other.headers and
                self.action == other.action and
                self.querystring_params == other.querystring_params and
                self.body_params == other.body_params and
                self.body_json_params == other.body_json_params and
                self.should_exit == other.should_exit)

    def copy(self):
        context = Context(self.url)
        context.headers = self.headers.copy()
        context.action = self.action.copy()
        context.querystring_params = self.querystring_params.copy()
        context.body_params = self.body_params.copy()
        context.body_json_params = self.body_json_params.copy()
        context.should_exit = self.should_exit
        return context

    def update(self, context):
        if context.url:
            self.url = context.url

        self.headers.update(context.headers)
        self.action.update(context.action)
        self.querystring_params.update(context.querystring_params)
        self.body_params.update(context.body_params)
        self.body_json_params.update(context.body_json_params)
        self.should_exit = self.should_exit
