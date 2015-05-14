
echo '' > /etc/network/interfaces

cat <<EOF >  /etc/network/interfaces
auto lo

iface lo inet loopback
iface eth0 inet dhcp
EOF

echo "iface $INTERFACE inet static" /etc/network/interfaces

cat <<EOF >>  /etc/network/interfaces
address 10.0.0.1
netmask 255.255.255.0
broadcast 255.0.0.0
pre-up iptables-restore < /etc/iptables.rules

#allow-hotplug wlan0
#iface wlan0 inet manual
#wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
#iface default inet dhcp
EOF
