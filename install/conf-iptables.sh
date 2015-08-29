
sysctl net.ipv4.ip_forward=1
#sed -i "/net.ipv4.ip_forward/c\net.ipv4.ip_forward=1" /etc/sysctl.conf
echo "1" > /proc/sys/net/ipv4/ip_forward

iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain

iptables --append FORWARD --in-interface $INTERFACE -j ACCEPT
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1:80
#~ iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1:80
iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 10.0.0.1:443
#~ iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 443 -j DNAT --to-destination 10.0.0.1:443

sh -c "iptables-save > /etc/iptables.rules"

