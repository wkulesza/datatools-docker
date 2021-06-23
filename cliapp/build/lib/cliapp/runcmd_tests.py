# Copyright (C) 2011, 2012  Lars Wirzenius
# Copyright (C) 2012  Codethink Limited
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

from __future__ import unicode_literals

import os
import subprocess
import tempfile
import unittest

import cliapp


def devnull(msg):
    pass


class RuncmdTests(unittest.TestCase):

    def test_runcmd_executes_true(self):
        self.assertEqual(cliapp.runcmd(['true']), b'')

    def test_runcmd_raises_error_on_failure(self):
        self.assertRaises(cliapp.AppException, cliapp.runcmd, ['false'])

    def test_runcmd_returns_stdout_of_command(self):
        self.assertEqual(cliapp.runcmd(['echo', b'hello', b'world']),
                         b'hello world\n')

    def test_runcmd_returns_stderr_of_command(self):
        exit_code, out, err = cliapp.runcmd_unchecked(['ls', 'notexist'])
        self.assertNotEqual(exit_code, 0)
        self.assertEqual(out, b'')
        self.assertNotEqual(err, b'')

    def test_runcmd_pipes_stdin_through_command(self):
        self.assertEqual(cliapp.runcmd(['cat'], feed_stdin=b'hello, world'),
                         b'hello, world')

    def test_runcmd_pipes_stdin_through_two_commands(self):
        self.assertEqual(
            cliapp.runcmd(['cat'], ['cat'], feed_stdin=b'hello, world'),
            b'hello, world')

    def test_runcmd_pipes_stdin_through_command_with_lots_of_data(self):
        data = b'x' * (1024 ** 2)
        self.assertEqual(cliapp.runcmd(['cat'], feed_stdin=data), data)

    def test_runcmd_ignores_failures_on_request(self):
        self.assertEqual(cliapp.runcmd(['false'], ignore_fail=True), b'')

    def test_runcmd_obeys_cwd(self):
        self.assertEqual(cliapp.runcmd(['pwd'], cwd='/'), b'/\n')

    def test_runcmd_unchecked_returns_values_on_success(self):
        self.assertEqual(cliapp.runcmd_unchecked(['echo', 'foo']),
                         (0, b'foo\n', b''))

    def test_runcmd_unchecked_returns_values_on_failure(self):
        self.assertEqual(cliapp.runcmd_unchecked(['false']),
                         (1, b'', b''))

    def test_runcmd_unchecked_runs_simple_pipeline(self):
        self.assertEqual(
            cliapp.runcmd_unchecked(['echo', 'foo'], ['wc', '-c']),
            (0, b'4\n', b''))

    def test_runcmd_unchecked_runs_longer_pipeline(self):
        self.assertEqual(
            cliapp.runcmd_unchecked(['echo', 'foo'], ['cat'], ['wc', '-c']),
            (0, b'4\n', b''))

    def test_runcmd_redirects_stdin_from_file(self):
        fd, _ = tempfile.mkstemp()
        os.write(fd, 'foobar'.encode())   # send encoded data to stdin
        os.lseek(fd, 0, os.SEEK_SET)
        self.assertEqual(cliapp.runcmd_unchecked(['cat'], stdin=fd),
                         (0, b'foobar', b''))
        os.close(fd)

    def test_runcmd_redirects_stdout_to_file(self):
        fd, filename = tempfile.mkstemp()
        exit_code, _, _ = cliapp.runcmd_unchecked(
            ['echo', 'foo'], stdout=fd)
        os.close(fd)
        with open(filename) as f:
            data = f.read()
        self.assertEqual(exit_code, 0)
        self.assertEqual(data, 'foo\n')

    def test_runcmd_redirects_stderr_to_file(self):
        fd, filename = tempfile.mkstemp()
        exit_code, _, _ = cliapp.runcmd_unchecked(
            ['ls', 'notexist'], stderr=fd)
        os.close(fd)
        with open(filename) as f:
            data = f.read()
        self.assertNotEqual(exit_code, 0)
        self.assertNotEqual(data, '')

    def test_runcmd_unchecked_handles_stdout_err_redirected_to_same_file(self):
        fd, filename = tempfile.mkstemp()
        exit_code, _, _ = cliapp.runcmd_unchecked(
            ['sleep', '2'], stdout=fd, stderr=subprocess.STDOUT)
        os.close(fd)
        with open(filename) as f:
            data = f.read()
        self.assertEqual(exit_code, 0)
        self.assertEqual(data, '')

    def test_runcmd_calls_stdout_callback_when_msg_on_stdout(self):
        msgs = []

        def logger(s):
            msgs.append(s)

            # We return bytes to allow the callback to mangle
            # the data being returned.
            return b'foo'

        test_input = 'hello fox'
        _, out, _ = cliapp.runcmd_unchecked(
            ['echo', '-n', test_input], stdout_callback=logger)

        self.assertEqual(out, b'foo')
        self.assertEqual(msgs, [test_input.encode('UTF-8')])

    def test_runcmd_calls_stderr_callback_when_msg_on_stderr(self):
        msgs = []

        def logger(s):
            msgs.append(s)

            # We return None to signal that the data should not be
            # mangled.
            return None

        _, _, err = cliapp.runcmd_unchecked(
            ['ls', 'nosuchthing'], stderr_callback=logger)

        # The callback may be called several times, and we have no
        # control over that: output from the subprocess may arrive in
        # drips due to process scheduling and other reasons beyond our
        # control. Thus, we compare the joined string fragments,
        # instead of the list of fragments.

        self.assertNotEqual(err, '')
        self.assertEqual(b''.join(msgs), err)


class ShellQuoteTests(unittest.TestCase):

    def test_returns_empty_string_for_empty_string(self):
        self.assertEqual(cliapp.shell_quote(''), '')

    def test_returns_same_string_when_safe(self):
        self.assertEqual(cliapp.shell_quote('abc123'), 'abc123')

    def test_quotes_space(self):
        self.assertEqual(cliapp.shell_quote(' '), "' '")

    def test_quotes_double_quote(self):
        self.assertEqual(cliapp.shell_quote('"'), "'\"'")

    def test_quotes_single_quote(self):
        self.assertEqual(cliapp.shell_quote("'"), '"\'"')
