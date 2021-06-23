# Copyright 2011-2015  Lars Wirzenius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =*= License: GPL-3+ =*=


import gc
import logging
import os
import platform
import time


class MemoryProfileDumper(object):

    def __init__(self, settings):
        self.settings = settings
        self.last_memory_dump = 0
        self.memory_dump_counter = 0
        self.started = time.time()

    def dump_memory_profile(self, msg):
        '''Log memory profiling information.

        Get the memory profiling method from the dump-memory-profile
        setting, and log the results at DEBUG level. ``msg`` is a
        message the caller provides to identify at what point the profiling
        happens.

        '''

        kind = self.settings['dump-memory-profile']
        interval = self.settings['memory-dump-interval']

        if kind == 'none':
            return

        now = time.time()
        if self.last_memory_dump + interval > now:
            return
        self.last_memory_dump = now

        # Log wall clock and CPU times for self, children.
        utime, stime, cutime, cstime, elapsed_time = os.times()
        duration = elapsed_time - self.started
        logging.debug('process duration: %s s', duration)
        logging.debug('CPU time, in process: %s s', utime)
        logging.debug('CPU time, in system: %s s', stime)
        logging.debug('CPU time, in children: %s s', cutime)
        logging.debug('CPU time, in system for children: %s s', cstime)

        logging.debug('dumping memory profiling data: %s', msg)
        logging.debug('VmRSS: %s KiB', self._vmrss())

        if kind == 'simple':
            return

        # These are fairly expensive operations, so we only log them
        # if we're doing expensive stuff anyway.
        logging.debug('# objects: %d', len(gc.get_objects()))
        logging.debug('# garbage: %d', len(gc.garbage))

    def _vmrss(self):  # pragma: no cover
        '''Return current resident memory use, in KiB.'''
        if platform.system() != 'Linux':
            return 0
        try:
            f = open('/proc/self/status')
        except IOError:
            return 0
        rss = 0
        for line in f:
            if line.startswith('VmRSS'):
                rss = line.split()[1]
        f.close()
        return rss
