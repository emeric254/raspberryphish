#!/bin/bash

# vars :
export INTERFACE=wlan0
export DRIVER=nl80211
export CHANNEL=6
export SSID="test"
export PAGE="test"
export SERVERPATH="/media/USB"
export SSHPORT=22
# radius
export ACTIVATERADIUS=0
export RADIUSLOGPATH="$SERVERPATH/radius-log"
export RADIUSSECRET="testing"
export AUTHSERVER=127.0.0.1
export AUTHPORT=1812
export ACCTSERVER=127.0.0.1
export ACCTPORT=1813


# instal scripts
bash ./install/conf-hostapd.sh
bash ./install/conf-dnsmasq.sh

if [ $ACTIVATERADIUS -eq 1 ]
then
bash ./install/conf-freeradius.sh
fi

bash ./install/conf-iptables.sh
bash ./install/conf-network-interfaces.sh
bash ./install/conf-raspberryphish-server.sh
bash ./install/conf-update-rc.sh
