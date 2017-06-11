#!/usr/bin/env python

import logging
import subprocess
import shlex


class Task(object):

    def __init__(self, command):
        self.command = command
        self._proc = None
        self._out = None
        self._err = None
        self._rc = None
        self.pid = None

    def wait(self):
        if not self._proc:
            self.start()
        self._out, self._rc = self._proc.communicate()
        self._rc = self._proc.returncode
        logging.debug('Finished process (%i): %s', self.pid, self.command)
        return self._rc, self._out, self._err

    def __getattr__(self, key):
        if key in ['rc', 'err', 'out']:
            self.wait()
            return getattr(self, '_' + key)
        raise AttributeError('Object has no property: %s' % (key))

    def start(self):
        self._proc = subprocess.Popen(shlex.shlex(self.command), \
                    stdout=subprocess.PIPE, \
                    stderr=subprocess.PIPE, \
                    universal_newlines=True)
        self.pid = self._proc.pid
        logging.debug('Started process (%i): %s', self.pid, self.command)
        return self.pid

    def stop(self):
        if self.is_alive():
            self._proc.kill()
            return True
        return False

    def is_alive(self):
        if self._proc.poll() is None:
            return True
        self.wait()
        return False
