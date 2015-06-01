#!/bin/bash

# vars :
export INTERFACE=wlan0
export DRIVER=nl80211
export CHANNEL=1
export SSID="test"
export PAGE="test"
export SERVERPATH="/media/USB"
export SSHPORT=22
# radius
export ACTIVATERADIUS = 1
export RADIUSLOGPATH="/media/USB/radius-log"
export RADIUSSECRET = "testing"
#export NASID = "NASID"
export AUTHSERVER = 127.0.0.1
export AUTHPORT = 0
export ACCTSERVER = 127.0.0.1
export ACCTPORT = 0


# instal scripts
bash ./install/conf-hostapd.sh
bash ./install/conf-dnsmasq.sh
bash ./install/conf-iptables.sh
bash ./install/conf-network-interfaces.sh
bash ./install/conf-raspberryphish-server.sh
bash ./install/conf-update-rc.sh
