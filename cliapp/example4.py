# Copyright (C) 2013  Lars Wirzenius
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


import cliapp


class ExampleApp(cliapp.Application):

    def setup(self):
        self.add_subcommand('insult', self.insult, hidden=True)

    def add_settings(self):
        self.settings.string(['yoyo'], 'yoyo help', hidden=True)
        self.settings.boolean(['blip'], 'blip help', hidden=True)

    def cmd_greet(self, args):
        '''Greet the user.

        The user is treated to a a courteus,
        but terse form of greeting.

        '''
        for arg in args:
            self.output.write('greetings, %s\n' % arg)

    def insult(self, args):
        '''Insult the user. (hidden command)

        Sometimes, though rarely, it happens that a user is really a bit of
        a prat, and needs to be told off. This is the command for that.

        '''
        for arg in args:
            self.output.write('you suck, %s\n' % arg)


ExampleApp().run()
