# -*- coding: utf-8 -*-

import sys
import time
from subprocess import Popen, PIPE

from Daemons.AbstractDaemon import Daemon


def cpu_avg_load():
    usages1 = [int(num) for num in str(Popen("cat /proc/stat | grep 'cpu '", shell=True, stdout=PIPE)
                                       .stdout.read()).replace("\\n'", "").split()[2:12]]
    usages2 = [int(num) for num in str(Popen("cat /proc/stat | grep 'cpu '", shell=True, stdout=PIPE)
                                       .stdout.read()).replace("\\n'", "").split()[2:12]]
    total = sum(usages2) - sum(usages1)
    idle = usages2[3] - usages1[3]
    return int(total - idle / total)


def ram_avg_load():
    usages = str(Popen("free | grep ': '", shell=True, stdout=PIPE)
                 .stdout.read()).split("\\n")[0].split()[1:]
    return int(100*(int(usages[0]) - int(usages[-1]))/int(usages[0]))


class LoadDaemon(Daemon):

    data = []

    def run(self):
        while True:
            time.sleep(10)
            self.data.append(self.current_system_load())
            if len(self.data) > 360:
                self.data = self.data[len(self.data)-360:]
            # TODO write data to a file ! (CSV)

    @staticmethod
    def current_system_load():
        return cpu_avg_load(), ram_avg_load()  # 'StorageInfos.avg_load()


if __name__ == "__main__":
    daemon = LoadDaemon('/tmp/raspberryphish-load-daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
