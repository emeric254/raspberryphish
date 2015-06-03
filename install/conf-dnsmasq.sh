
cat <<EOF > /etc/dnsmasq.conf
no-resolv
interface=$INTERFACE
dhcp-range=10.0.0.10,10.0.0.200,255.255.255.0,12h
dhcp-option=3,10.0.0.1
address=/#/10.0.0.1
log-queries
log-facility=/var/log/dnsmasq.log
dhcp-authoritative
dhcp-leasefile=/tmp/dhcp.leases
EOF
