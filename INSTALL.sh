INTERFACE=wlan0
DRIVER=nl80211
CHANNEL=1
SSID="test"
PAGE="test"

bash ./install/conf-hostapd.sh
bash ./install/conf-dnsmasq.sh
bash ./install/conf-iptables.sh
bash ./install/conf-network-interfaces.sh
bash ./install/conf-update-rc.sh
