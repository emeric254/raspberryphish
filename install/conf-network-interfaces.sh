
cat <<EOF >  /etc/network/interfaces
auto lo
iface lo inet loopback
auto eth0
allow-hotplug eth0
iface eth0 inet dhcp
EOF

echo "auto $INTERFACE" >>  /etc/network/interfaces
echo "allow-hotplug $INTERFACE" >>  /etc/network/interfaces
echo "iface $INTERFACE inet static" >>  /etc/network/interfaces
cat <<EOF >>  /etc/network/interfaces
    address 10.0.0.254
    netmask 255.255.255.0
    network 10.0.0.0
    broadcast 10.0.0.255
pre-up iptables-restore < /etc/iptables.rules

#allow-hotplug wlan0
#iface wlan0 inet manual
#wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
#iface default inet dhcp
EOF
