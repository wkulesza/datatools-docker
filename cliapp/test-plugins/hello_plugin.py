import cliapp

class Hello(cliapp.Plugin):

    def __init__(self, foo, bar=None):
        self.foo = foo
        self.bar = bar

    @property
    def version(self):
        return '0.0.1'

    def setup(self):
        self.setup_called = True

    def enable(self):
        pass
