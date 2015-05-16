# raspberryphish
=================


## TODO
  - install script for the server
  - config script for the server
  - make some html pages
  - more infos in this _README_
  - documentation
  - tests & reports


## dependencies
  - hostapd
  - dnsmasq
  - python-tornado

```bash
aptitude -y install hostapd dnsmasq python3-tornado
```



## configuration

edit the _INSTALL.sh_ file as you wish

```bash
nano INSTALL.sh
```

Name  | explanation | default
----- | ----------- | -------
 INTERFACE | interface to use | wlan0
 DRIVER | driver to use | nl80211
 CHANNEL | wifi channel to use | 1
 SSID | SSID to use | test
 PAGE | html pages the server have to use | test
 SERVERPATH | where the server will be installed | /media/USB



## install raspberryphish on your system

execute the _INSTALL.sh_ file

```bash
bash INSTALL.sh
```
