# local interfaces file, parameters to configure the $INTERFACE with ifstate tool
cat <<EOF >  $SERVERPATH/interfaces
allow-hotplug $INTERFACE
auto $INTERFACE

iface $INTERFACE inet static
        address 10.0.0.1
        netmask 255.255.255.0
        network 10.0.0.0
        broadcast 10.0.0.255
        gateway 10.0.0.1

pre-up iptables-restore < /etc/iptables.rules

#wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
#iface default inet dhcp
EOF
