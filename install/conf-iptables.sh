
echo "1" > /proc/sys/net/ipv4/ip_forward


iptables -F

iptables -i wlan0 -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

iptables -i wlan0 -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -i wlan0 -A INPUT -p tcp --dport $SSHPORT -j ACCEPT
iptables -i wlan0 -A INPUT -p udp --dport 53 -j ACCEPT
iptables -i wlan0 -A INPUT -p udp --dport 67:68 -j ACCEPT

iptables -t nat -A PREROUTING -p tcp -i wlan0 --dport 443 -j DNAT --to-destination 127.0.0.1:80
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE

iptables -i wlan0 -A INPUT -j DROP

sh -c "iptables-save > /etc/iptables.rules"
