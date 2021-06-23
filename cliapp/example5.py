# Copyright (C) 2014  Richard Ipsum
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


class LoggerApp(cliapp.Application):

    def log(self, s):
        ''' A dummy logger function

            In practice this would log the contents
            to a file or a set of files, perhaps filtering the output or
            prefixing each line with a date and time.

        '''

        self.output.write('log: %s' % s)
        self.output.flush()

    def process_args(self, args):
        commands = [['echo', 'hello world!'], ['ls', 'nosuchthing']]

        for command in commands:
            try:
                self.runcmd(command, stdout_callback=self.log,
                            stderr_callback=self.log)
            except cliapp.AppException:
                pass

LoggerApp().run()
