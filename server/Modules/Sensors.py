#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata, os, sys
from subprocess import *

commandes = ['cat', 'hostname', 'last', 'hddtemp', 'df', 'ps', 'free', 'ping', 'grep', 'uniq', 'who', 'uname',
             'sensors']

for comm in commandes:
    res = Popen("which %s" % comm, shell=True, stdout=PIPE).returncode
    if res:
        print("La commande", comm, "n'est pas présente sur votre système.")


def liste_hdd():
    hdd = []
    result = str(Popen("cat /proc/partitions", shell=True, stdout=PIPE).stdout.read()).split("\n")
    result.pop(0)
    for disque in result:
        if disque:
            disque = disque.split()[-1]
            if disque not in hdd:
                hdd.append(disque)
    return hdd


def hdd_temp():
    hdd = {}
    for disque in liste_hdd():
        temperature = str(Popen("hddtemp -n /dev/%s" % disque,
                                shell=True, stdout=PIPE).stdout.read()).split("\n")
        try:
            hdd[disque] = int(temperature)
        except:
            pass
    return hdd


def hdd_usage():
    # espace disque
    hdd = {}
    result = str(Popen("df -P | grep -e '^/dev'",
                       shell=True, stdout=PIPE).stdout.read()).split("\n")
    for disque in result:
        hdd[disque.split()[0] + '  '+str(disque.split()[5:])] = str(disque.split()[4][:-1])
    return hdd



def uptime():
    # uptime
    duree = float(str(Popen("cat /proc/uptime", shell=True, stdout=PIPE)
                      .stdout.read()).replace("b'", "").split()[0])
    secondes = int(duree % 60)
    minutes = int(duree/60 % 60)
    heures = int(duree/60/60 % 24)
    jours = int(duree/60/60/24)
    return [duree, jours, heures, minutes, secondes]


def avg_load():
    # average load
    return str(Popen("who /proc/loadavg", shell=True, stdout=PIPE).stdout.read()).split()[0]


def login_today():
    login = str(Popen("last | grep \"$(LANG=C date +\"%%a %%b %%-d\")\"",
                      shell=True, stdout=PIPE).stdout.read()).split("\n")
    if not login:
        login = str(Popen("last | grep \"$(LANG=C date +\"%%a %%b  %%-d\")\"",
                          shell=True, stdout=PIPE).stdout.read()).split("\n")
    return login


def login_now():
    logins_connectes = []
    wholiste = str(Popen("who", shell=True, stdout=PIPE).stdout.read()).split("\n")
    for ligne in wholiste:
        if ligne:
            user = ligne.split()[0]
            if user not in logins_connectes:
                logins_connectes.append(user)
    return logins_connectes


def processus_liste():
    psliste = []
    result = str(Popen("ps -e", shell=True, stdout=PIPE).stdout.read()).split("\n")
    result.pop(0)
    for processus in result:
        if processus.split(":")[-1][3:]:
            psliste.append(processus.split(":")[-1][3:])
        else:
            psliste.append(processus)
    return psliste


def ram_etat():
    ram = {}
    ram["install"] = str(Popen("cat /proc/meminfo | grep \"MemTotal\"",
                               shell=True, stdout=PIPE).stdout.read()).split(":")[1]
    result = str(Popen("free", shell=True, stdout=PIPE).stdout.read()).split("\\n")
    print(result)
    memoire = result[1].split()[1:]
    print(memoire)
    swap = result[3].split()[1:]
    print(swap)
    return ram


def ping(url):
    return str(Popen("ping -c 1 %s" % url, shell=True, stdout=PIPE)
               .stdout.read()).split("\\n")[-1].split("=")[-1].split("/")[1]


def ping6(url):
    return str(Popen("ping6 -c 1 %s" % url, shell=True, stdout=PIPE)
               .stdout.read()).split("\n")[-1].split("=")[-1].split("/")[1]


def temp():
    alltemp = {}
    raw = str(Popen("sensors", shell=True, stdout=PIPE).stdout.read()).split("\n")
    for ligne in raw:
        if not ligne:
            raw.remove(ligne)
    x = 1
    for ligne in raw:
        if not x % 3:
            name = ligne.split(":")[0]
            alltemp[name] = ligne.split(":")[1]
        x += 1
    return alltemp

print(liste_hdd())
print(hdd_temp())
print(hdd_usage())
print(uptime())
print(avg_load())
print(login_today())
print(login_now())
print(processus_liste())
print(ram_etat())
print(ping("google.com"))
print(temp())
