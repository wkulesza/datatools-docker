# This is a test plugin that requires a newer application version than
# what the test harness specifies.

import cliapp

class WrongVersion(cliapp.Plugin):

    required_application_version = '9999.9.9'

    def __init__(self, *args, **kwargs):
        pass

    def enable(self):
        pass
