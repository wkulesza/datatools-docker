# Copyright (C) 2011  Lars Wirzenius
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


'''Example for cliapp framework.

Greet or insult people.

'''


import cliapp


class ExampleApp(cliapp.Application):

    cmd_synopsis = {
        'greet': 'USER...',
        'insult': 'USER...',
    }

    def cmd_greet(self, args):
        '''Greet the user.

        The user is treated to a a courteus,
        but terse form of greeting.

        '''
        if len(args) == 0:
            raise cliapp.AppException(self.get_subcommand_usage('greet'))

        for arg in args:
            self.output.write('greetings, %s\n' % arg)

    def cmd_insult(self, args):
        '''Insult the user.

        Sometimes, though rarely, it happens that a user is really a bit of
        a prat, and needs to be told off. This is the command for that.

        '''
        if len(args) == 0:
            raise cliapp.AppException(self.get_subcommand_usage('insult'))

        for arg in args:
            self.output.write('you suck, %s\n' % arg)


app = ExampleApp(
    version='0.1.2',
    description='''
Greet the user.
Or possibly insult them. User's choice.
''',
    epilog='''
This is the epilog.

I hope you like it.
''')

app.run()
