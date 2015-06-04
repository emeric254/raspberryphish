# raspberryphish
=================


## TODO
  - config script for the server
  - make some html pages
  - more infos in this _README_ file
  - documentation
  - tests & reports


## dependencies
  - hostapd
  - dnsmasq
  - python3-tornado (for raspbian, or something like _python-tornado_ depending your OS)
  - freeradius (for fake securised APs)

```bash
# for raspbian
aptitude -y install hostapd dnsmasq python3-tornado
```


## configuration

edit the _INSTALL.sh_ file as you wish

```bash
nano INSTALL.sh
```

### basic vars

Name  | explanation | default
----- | ----------- | -------
 INTERFACE | interface to use | wlan0
 DRIVER | driver to use | nl80211
 CHANNEL | wifi channel to use | 1
 SSID | SSID to use | test
 PAGE | html pages the server have to use | test
 SERVERPATH | where the server will be installed | /media/USB

### radius vars

Name  | explanation | default
----- | ----------- | -------
 ACTIVATERADIUS | boolean, to activate radius set it to the value of _1_ | 0
 RADIUSLOGPATH | where radius server logs will be write | "$SERVERPATH/radius-log"
 RADIUSSECRET | the _password_ to communicate with the radius | "testing"
 AUTHSERVER | the pi itself here | 127.0.0.1
 AUTHPORT | default authentification radius port | 1812
 ACCTSERVER | the pi itself here | 127.0.0.1
 ACCTPORT | default accounting radius port | 1813


## install raspberryphish on your system

execute the _INSTALL.sh_ file (with permissions)

```bash
# remember to verify your permission !
# use « sudo » or execute that as « root » user 
bash INSTALL.sh
```
