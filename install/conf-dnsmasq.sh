
echo "log-facility=/var/log/dnsmasq.log" /etc/dnsmasq.conf
echo "address=/#/10.0.0.1" /etc/dnsmasq.conf
echo "interface=$INTERFACE" /etc/dnsmasq.conf
echo "dhcp-range=10.0.0.10,10.0.0.250,12h" /etc/dnsmasq.conf
echo "no-resolv" /etc/dnsmasq.conf
echo "log-queries" /etc/dnsmasq.conf
