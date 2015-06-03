
cat <<EOF >  /etc/network/interfaces
auto lo
iface lo inet loopback
iface eth0 inet dhcp
EOF


cat <<EOF >>  /etc/network/interfaces
auto $INTERFACE
iface $INTERFACE inet static
    address 10.0.0.1
    netmask 255.255.255.0
pre-up iptables-restore < /etc/iptables.rules

#allow-hotplug wlan0
#iface wlan0 inet manual
#wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
#iface default inet dhcp
EOF
