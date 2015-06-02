
cat <<EOF > /etc/dnsmasq.conf
log-facility=/var/log/dnsmasq.log
address=/#/10.0.0.1
interface=$INTERFACE
dhcp-range=10.0.0.10,10.0.0.250,12h
no-resolv
log-queries
EOF
