
echo "interface=$INTERFACE" > /etc/dnsmasq.conf

cat <<EOF >> /etc/dnsmasq.conf
dhcp-authoritative
dhcp-leasefile=/tmp/dhcp.leases

dhcp-option=1,255.255.255.0
dhcp-option=3,10.0.0.254 # default gateway
dhcp-option=6,10.0.0.254 # dns server
dhcp-range=10.0.0.10,10.0.0.99,255.255.255.0,12h

no-resolv
address=/#/10.0.0.254
log-queries
log-facility=/var/log/dnsmasq.log
EOF
