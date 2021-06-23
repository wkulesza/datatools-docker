import cliapp

class Hello(cliapp.Plugin):

    def __init__(self, foo, bar=None):
        self.foo = foo
        self.bar = bar

    def enable(self):
        pass
