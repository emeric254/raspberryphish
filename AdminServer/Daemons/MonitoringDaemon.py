# -*- coding: utf-8 -*-

import sys
import time
from subprocess import Popen, PIPE
from AbstractDaemon import Daemon


def cpu_avg_load():
    # TODO doc
    usage1 = [int(num) for num in str(Popen("cat /proc/stat | grep 'cpu '", shell=True, stdout=PIPE)
                                       .stdout.read()).replace("\\n'", "").split()[2:12]]
    usage2 = [int(num) for num in str(Popen("cat /proc/stat | grep 'cpu '", shell=True, stdout=PIPE)
                                       .stdout.read()).replace("\\n'", "").split()[2:12]]
    total = sum(usage2) - sum(usage1)
    idle = usage2[3] - usage1[3]
    return int(total - idle / total)


def ram_avg_load():
    # TODO doc
    usages = str(Popen("free | grep ': '", shell=True, stdout=PIPE)
                 .stdout.read()).split("\\n")[0].split()[1:]
    return int(100*(int(usages[0]) - int(usages[-1]))/int(usages[0]))


class LoadDaemon(Daemon):
    # TODO doc

    data = []

    def run(self):
        # TODO doc
        while True:
            time.sleep(10)
            self.data.append([cpu_avg_load(), ram_avg_load()])
            if len(self.data) > 360:
                self.data = self.data[len(self.data)-360:]


if __name__ == "__main__":
    daemon = LoadDaemon('/tmp/raspberryphish-load-daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            if daemon.status():
                print('Daemon is running.')
            else:
                print('Daemon is not running.')
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart|status" % sys.argv[0])
        sys.exit(2)
