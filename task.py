#!/usr/bin/env python

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
        self._out, self._rc = self._proc.communicate()
        self._rc = self._proc.returncode
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


class Manager(object):

    def __init__(self):
        self.tasks = {}

    def add_task(self, command):
        t = Task(command)
        self.tasks[t.start()] = t

    def _cleanup(self):
        running = self.tasks.values()
        for task in running:
            if not task.is_alive():
                del self.tasks[task.pid]

    def running_tasks(self):
        self._cleanup()
        return self.tasks.values()

if __name__ == '__main__':
    m = Manager()
    m.add_task('echo "hello world"')
    print m.running_tasks()

    print m.running_tasks()[0].wait()
