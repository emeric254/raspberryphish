__author__ = 'emeric'

import os
from subprocess import *
import sys
import platform


class OSInfos:
    def name():
        return platform.node()
    name = staticmethod(name)

    def os_name():
        return platform.system() + " " + platform.release()
    os_name = staticmethod(os_name)

    def interpreter_name():
        return platform.python_implementation()
    interpreter_name = staticmethod(interpreter_name)

    def python_version():
        return platform.python_version()
    python_version = staticmethod(python_version)


class CpuInfos:
    def avg_load():
        usages1 = [int(num) for num in str(Popen("cat /proc/stat | grep 'cpu '", shell=True, stdout=PIPE)
                                           .stdout.read()).replace("\\n'", "").split()[2:12]]
        usages2 = [int(num) for num in str(Popen("cat /proc/stat | grep 'cpu '", shell=True, stdout=PIPE)
                                           .stdout.read()).replace("\\n'", "").split()[2:12]]
        total = sum(usages2)-sum(usages1)
        idle = usages2[3]-usages1[3]
        return int((total-idle/total))
    avg_load = staticmethod(avg_load)
    
    def cpu_name():
        return platform.processor()
    cpu_name = staticmethod(cpu_name)

    def cpu_type():
        return platform.machine()
    cpu_type = staticmethod(cpu_type)


class RamInfos:
    def avg_load():
        usages = str(Popen("free | grep ': '", shell=True, stdout=PIPE)
                     .stdout.read()).split("\\n")[0].split()[1:]
        return int(100*(int(usages[0]) - int(usages[-1]))/int(usages[0]))
    avg_load = staticmethod(avg_load)


class StorageInfos:
    def avg_load():
        usages = str(Popen("df -l --total | grep 'total '", shell=True, stdout=PIPE)
                     .stdout.read()).split()[4].replace("%", "").replace("'","").replace("\\n","")
        return int(usages)
    avg_load = staticmethod(avg_load)

    def io_load():
        lines1 = str(Popen("iotop -obqqqn 1", shell=True, stdout=PIPE)
                     .stdout.read()).replace("b'", "").replace("'", "").split("\\n")
        io = 0
        for line in lines1:
            if line:
                io += float(line.split()[9])
        return int(io)
    io_load = staticmethod(io_load)


class SensorInfos:
    def cpu_temp():
        return 0
    cpu_temp = staticmethod(cpu_temp)

    def mb_temp():
        return 0
    mb_temp = staticmethod(mb_temp)

    def raspberry_temp():
        lines1 = str(Popen("/opt/vc/bin/vcgencmd measure_temp", shell=True, stdout=PIPE)
                     .stdout.read()).replace("b'", "").replace("'", "").split("C")[0].split("=")[1]
        return int(float(lines1))
    raspberry_temp = staticmethod(raspberry_temp)
