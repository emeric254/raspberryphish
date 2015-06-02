
cat <<EOF >  /etc/network/interfaces
auto lo

iface lo inet loopback
iface eth0 inet dhcp
allow-hotplug eth0
EOF

cat <<EOF >>  /etc/network/interfaces
iface $INTERFACE inet static
allow-hotplug $INTERFACE
address 10.0.0.1
network 10.0.0.0
netmask 255.255.255.0
broadcast 10.0.0.255
dns-nameservers 127.0.0.1
pre-up iptables-restore < /etc/iptables.rules
EOF
