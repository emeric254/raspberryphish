
cat <<EOF > /etc/dnsmasq.conf
no-resolv
interface=$INTERFACE
address=/#/10.0.0.1
dhcp-range=10.0.0.10,10.0.0.200,12h
log-queries
log-facility=/var/log/dnsmasq.log
EOF
