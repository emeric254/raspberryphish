# -*- coding: utf-8 -*-

"""Generic linux daemon base class for python 3.x."""

import sys
import os
import time
import atexit
import signal
import logging


class Daemon:
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method."""

    def __init__(self, pid_file: str):
        self.pid_file = pid_file

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""
        try:
            if os.fork() > 0:  # do first fork
                sys.exit(0)  # exit first parent
        except OSError as err:
            logging.exception('fork #1 failed : ' + str(err))
            sys.exit(1)
        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)
        try:
            if os.fork() > 0:  # do second fork
                sys.exit(0)  # exit second parent
        except OSError as err:
            logging.exception('fork #2 failed : ' + str(err))
            sys.exit(1)
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        devnull = os.open('/dev/null', os.O_RDWR)
        os.dup2(devnull, sys.stdin.fileno())
        os.dup2(devnull, sys.stdout.fileno())
        os.dup2(devnull, sys.stderr.fileno())
        atexit.register(self.del_pid)  # delete pid_file at exit
        pid = str(os.getpid())  # get pid
        with open(self.pid_file, 'w+') as pid_file:
            pid_file.write(pid + '\n')  # write pid_file

    def del_pid(self):
        """Delete pid_file"""
        os.remove(self.pid_file)

    def start(self):
        """Start the daemon."""
        if self.status():  # running
            logging.error('pid_file ' + self.pid_file + ' already exist. Daemon is already running ?')
            sys.exit(1)  # error it's already running
        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""
        pid = self.status()
        if not pid:  # not running
            logging.warning('pid_file ' + self.pid_file + ' does not exist. Daemon is not running ?')
            return  # not an error in a restart
        try:  # Try killing the daemon process
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            error = str(err.args)
            if "No such process" in error:
                if os.path.exists(self.pid_file):
                    self.del_pid()
            else:
                print(str(err.args), file=sys.stderr)
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def status(self):
        """Status of the daemon.

        :return Daemon pid if running, None otherwise

        """
        try:
            with open(self.pid_file, 'r') as pid_file:
                pid = int(pid_file.read().strip())
                if pid:  # Get the pid from the pid_file
                    return pid
        except IOError:
            pass  # no pid_file so it's not running
        return None

    def run(self):
        """You should override this method when you subclass Daemons.

        It will be called after the process has been daemonized by
        start() or restart()."""
        raise NotImplementedError()
