# -*- coding: utf-8 -*-

from subprocess import *
import platform


class OSInfos:
    @staticmethod
    def name():
        return platform.node()

    @staticmethod
    def os_name():
        return platform.system() + " " + platform.release()

    @staticmethod
    def interpreter_name():
        return platform.python_implementation()
    
    @staticmethod
    def python_version():
        return platform.python_version()


class CpuInfos:
    @staticmethod
    def avg_load():
        usages1 = [int(num) for num in str(Popen("cat /proc/stat | grep 'cpu '", shell=True, stdout=PIPE)
                                           .stdout.read()).replace("\\n'", "").split()[2:12]]
        usages2 = [int(num) for num in str(Popen("cat /proc/stat | grep 'cpu '", shell=True, stdout=PIPE)
                                           .stdout.read()).replace("\\n'", "").split()[2:12]]
        total = sum(usages2)-sum(usages1)
        idle = usages2[3]-usages1[3]
        return int((total-idle/total))

    @staticmethod
    def cpu_name():
        return platform.processor()

    @staticmethod
    def cpu_type():
        return platform.machine()


class RamInfos:
    @staticmethod
    def avg_load():
        usages = str(Popen("free | grep ': '", shell=True, stdout=PIPE)
                     .stdout.read()).split("\\n")[0].split()[1:]
        return int(100*(int(usages[0]) - int(usages[-1]))/int(usages[0]))


class StorageInfos:
    @staticmethod
    def avg_load():
        usages = str(Popen("df -l --total | grep 'total '", shell=True, stdout=PIPE)
                     .stdout.read()).split()[4].replace("%", "").replace("'", "").replace("\\n", "")
        return int(usages)

    @staticmethod
    def io_load():
        lines1 = str(Popen("iotop -obqqqn 1", shell=True, stdout=PIPE)
                     .stdout.read()).replace("b'", "").replace("'", "").split("\\n")
        io = 0
        for line in lines1:
            if line:
                io += float(line.split()[9])
        return int(io)


class SensorInfos:
    @staticmethod
    def cpu_temp():
        return 0

    @staticmethod
    def mb_temp():
        return 0

    @staticmethod
    def raspberry_temp():
        lines1 = str(Popen("/opt/vc/bin/vcgencmd measure_temp", shell=True, stdout=PIPE)
                     .stdout.read()).replace("b'", "").replace("'", "").split("C")[0].split("=")[1]
        return int(float(lines1))
