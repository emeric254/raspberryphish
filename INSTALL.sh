export INTERFACE=wlan0
export DRIVER=nl80211
export CHANNEL=1
export SSID="test"
export PAGE="test"

bash ./install/conf-hostapd.sh
bash ./install/conf-dnsmasq.sh
bash ./install/conf-iptables.sh
bash ./install/conf-network-interfaces.sh
bash ./install/conf-update-rc.sh
