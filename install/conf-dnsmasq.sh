
cat <<EOF > /etc/dnsmasq.conf

no-resolv
interface=$INTERFACE
dhcp-authoritative
dhcp-leasefile=/tmp/dhcp.leases

dhcp-option=1,255.255.255.0
dhcp-option=3,10.0.0.1	# default gateway
#dhcp-option=6,10.0.0.1	# dns server
dhcp-option=19,0
#dhcp-option=23,64	#ttl

dhcp-range=10.0.0.2,10.0.0.101,1h	#ips dispo et duree

address=/#/10.0.0.1
log-queries
log-facility=/var/log/dnsmasq.log

EOF

