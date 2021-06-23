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

from __future__ import unicode_literals

try:
    from StringIO import StringIO
    # Fake these types that exist only in Python 3
    TextIOBase = file
except ImportError:
    from io import StringIO, TextIOBase
import sys
import unittest

import cliapp


def devnull(msg):
    pass


class AppExceptionTests(unittest.TestCase):

    def setUp(self):
        self.e = cliapp.AppException('foo')

    def test_error_message_contains_foo(self):
        self.assertTrue('foo' in str(self.e))


class ApplicationTests(unittest.TestCase):

    def setUp(self):
        self.app = cliapp.Application()

    def test_creates_settings(self):
        self.assertTrue(isinstance(self.app.settings, cliapp.Settings))

    def test_calls_add_settings_only_in_run(self):

        class Foo(cliapp.Application):

            def process_args(self, args):
                pass

            def add_settings(self):
                self.settings.string(['foo'], '')

        foo = Foo()
        self.assertFalse('foo' in foo.settings)
        foo.run(args=[])
        self.assertTrue('foo' in foo.settings)

    def test_run_uses_string_list_options_only_once(self):

        class Foo(cliapp.Application):

            def add_settings(self):
                self.settings.string_list(['foo'], '')

            def process_args(self, args):
                pass

        foo = Foo()
        foo.run(args=['--foo=yo'])
        self.assertEqual(foo.settings['foo'], ['yo'])

    def test_run_sets_up_logging(self):
        self.called = False

        def setup():
            self.called = True

        self.app.setup_logging = setup
        self.app.process_args = lambda args: None
        self.app.run([])
        self.assertTrue(self.called)

    def test_run_sets_progname_from_sysargv0(self):
        self.app.process_args = lambda args: None
        self.app.run(args=[], sysargv=['foo'])
        self.assertEqual(self.app.settings.progname, 'foo')

    def test_run_calls_process_args(self):
        self.called = None
        self.app.process_args = lambda args: setattr(self, 'called', args)
        self.app.run(args=['foo', 'bar'])
        self.assertEqual(self.called, ['foo', 'bar'])

    def test_run_processes_input_files(self):
        self.inputs = []
        self.app.process_input = self.inputs.append
        self.app.run(args=['foo', 'bar'])
        self.assertEqual(self.inputs, ['foo', 'bar'])

    def test_run_sets_output_attribute(self):
        self.app.process_args = lambda args: None
        self.app.run(args=[])
        self.assertEqual(self.app.output, sys.stdout)

    def test_run_sets_output_to_file_if_output_option_is_set(self):
        self.app.process_args = lambda args: None
        self.app.run(args=['--output=/dev/null'])
        self.assertEqual(self.app.output.name, '/dev/null')

    def test_run_calls_parse_args(self):
        class DummyOptions(object):
            def __init__(self):
                self.output = None
                self.log = None
        self.called = None
        self.app.parse_args = lambda args, **kw: setattr(self, 'called', args)
        self.app.process_args = lambda args: None
        self.app.settings.options = DummyOptions()
        self.app.run(args=['foo', 'bar'])
        self.assertEqual(self.called, ['foo', 'bar'])

    def test_makes_envname_correctly(self):
        self.assertEqual(self.app.envname('foo'), 'FOO')
        self.assertEqual(self.app.envname('foo.py'), 'FOO')
        self.assertEqual(self.app.envname('foo bar'), 'FOO_BAR')
        self.assertEqual(self.app.envname('foo-bar'), 'FOO_BAR')
        self.assertEqual(self.app.envname('foo/bar'), 'BAR')
        self.assertEqual(self.app.envname('foo_bar'), 'FOO_BAR')

    def test_parses_options(self):
        self.app.settings.string(['foo'], 'foo help')
        self.app.settings.boolean(['bar'], 'bar help')
        self.app.parse_args(['--foo=foovalue', '--bar'])
        self.assertEqual(self.app.settings['foo'], 'foovalue')
        self.assertEqual(self.app.settings['bar'], True)

    def test_calls_setup(self):

        context = {}

        class App(cliapp.Application):

            def setup(self):
                context['setup-called'] = True

            def process_inputs(self, args):
                pass

        app = App()
        app.run(args=[])
        self.assertTrue(context['setup-called'])

    def test_calls_cleanup(self):

        context = {}

        class App(cliapp.Application):

            def cleanup(self):
                context['cleanup-called'] = True

            def process_inputs(self, args):
                pass

        app = App()
        app.run(args=[])
        self.assertTrue(context['cleanup-called'])

    def test_process_args_calls_process_inputs(self):
        self.called = False

        def process_inputs(args):
            self.called = True

        self.app.process_inputs = process_inputs
        self.app.process_args([])
        self.assertTrue(self.called)

    def test_process_inputs_calls_process_input_for_each_arg(self):
        self.args = []

        def process_input(arg):
            self.args.append(arg)

        self.app.process_input = process_input
        self.app.process_inputs(['foo', 'bar'])
        self.assertEqual(self.args, ['foo', 'bar'])

    def test_process_inputs_calls_process_input_with_dash_if_no_inputs(self):
        self.args = []

        def process_input(arg):
            self.args.append(arg)

        self.app.process_input = process_input
        self.app.process_inputs([])
        self.assertEqual(self.args, ['-'])

    def test_open_input_opens_file(self):
        f = self.app.open_input('/dev/null')
        self.assertTrue(isinstance(f, TextIOBase))
        self.assertEqual(getattr(f, 'mode'), 'r')

    def test_open_input_opens_file_in_binary_mode_when_requested(self):
        f = self.app.open_input('/dev/null', mode='rb')
        self.assertEqual(getattr(f, 'mode'), 'rb')

    def test_open_input_opens_stdin_if_dash_given(self):
        self.assertEqual(self.app.open_input('-'), sys.stdin)

    def test_process_input_calls_open_input(self):
        self.called = None

        def open_input(name):
            self.called = name
            return StringIO('')

        self.app.open_input = open_input
        self.app.process_input('foo')
        self.assertEqual(self.called, 'foo')

    def test_process_input_does_not_close_stdin(self):
        self.closed = False

        def close():
            self.closed = True

        f = StringIO('')
        f.close = close

        def open_input(name):
            if name == '-':
                return f

        self.app.open_input = open_input
        self.app.process_input('-', stdin=f)
        self.assertEqual(self.closed, False)

    def test_processes_input_lines(self):

        lines = []

        class Foo(cliapp.Application):

            def open_input(self, name, mode=None):
                return StringIO(''.join('%s%d\n' % (name, i)
                                        for i in range(2)))

            def process_input_line(self, name, line):
                lines.append(line)

        foo = Foo()
        foo.run(args=['foo', 'bar'])
        self.assertEqual(lines, ['foo0\n', 'foo1\n', 'bar0\n', 'bar1\n'])

    def test_process_input_line_can_access_counters(self):
        counters = []

        class Foo(cliapp.Application):

            def open_input(self, name, mode=None):
                return StringIO(''.join('%s%d\n' % (name, i)
                                        for i in range(2)))

            def process_input_line(self, name, line):
                counters.append((self.fileno, self.global_lineno, self.lineno))

        foo = Foo()
        foo.run(args=['foo', 'bar'])
        self.assertEqual(counters,
                         [(1, 1, 1),
                          (1, 2, 2),
                          (2, 3, 1),
                          (2, 4, 2)])

    def test_run_prints_out_error_for_appexception(self):
        def raise_error(args):
            raise cliapp.AppException('xxx')
        self.app.process_args = raise_error
        f = StringIO()
        self.assertRaises(SystemExit, self.app.run, [], stderr=f, log=devnull)
        self.assertTrue('xxx' in f.getvalue())

    def test_run_prints_out_stack_trace_for_not_appexception(self):
        def raise_error(args):
            raise Exception('xxx')
        self.app.process_args = raise_error
        f = StringIO()
        self.assertRaises(SystemExit, self.app.run, [], stderr=f, log=devnull)
        self.assertTrue('Traceback' in f.getvalue())

    def test_run_raises_systemexit_for_systemexit(self):
        def raise_error(args):
            raise SystemExit(123)
        self.app.process_args = raise_error
        f = StringIO()
        self.assertRaises(SystemExit, self.app.run, [], stderr=f, log=devnull)

    def test_run_raises_systemexit_for_keyboardint(self):
        def raise_error(args):
            raise KeyboardInterrupt()
        self.app.process_args = raise_error
        f = StringIO()
        self.assertRaises(SystemExit, self.app.run, [], stderr=f, log=devnull)


class DummySubcommandApp(cliapp.Application):

    def cmd_foo(self, args):
        self.foo_called = True


class SubcommandTests(unittest.TestCase):

    def setUp(self):
        self.app = DummySubcommandApp()
        self.trash = StringIO()

    def test_lists_subcommands(self):
        self.assertEqual(self.app._subcommand_methodnames(), ['cmd_foo'])

    def test_normalizes_subcommand(self):
        self.assertEqual(self.app._normalize_cmd('foo'), 'cmd_foo')
        self.assertEqual(self.app._normalize_cmd('foo-bar'), 'cmd_foo_bar')

    def test_raises_error_for_no_subcommand(self):
        self.assertRaises(SystemExit, self.app.run, [],
                          stderr=self.trash, log=devnull)

    def test_raises_error_for_unknown_subcommand(self):
        self.assertRaises(SystemExit, self.app.run, ['what?'],
                          stderr=self.trash, log=devnull)

    def test_calls_subcommand_method(self):
        self.app.run(['foo'], stderr=self.trash, log=devnull)
        self.assertTrue(self.app.foo_called)

    def test_calls_subcommand_method_via_alias(self):
        self.bar_called = False

        def bar(*args):
            self.bar_called = True

        self.app.add_subcommand('bar', bar, aliases=['yoyo'])
        self.app.run(['yoyo'], stderr=self.trash, log=devnull)
        self.assertTrue(self.bar_called)

    def test_adds_default_subcommand_help(self):
        self.app.run(['foo'], stderr=self.trash, log=devnull)
        self.assertTrue('help' in self.app.subcommands)


class ExtensibleSubcommandTests(unittest.TestCase):

    def setUp(self):
        self.app = cliapp.Application()

    def test_lists_no_subcommands(self):
        self.assertEqual(self.app.subcommands, {})

    def test_adds_subcommand(self):
        def help_callback(arg):
            pass
        self.app.add_subcommand('foo', help_callback)
        self.assertEqual(self.app.subcommands, {'foo': help_callback})
