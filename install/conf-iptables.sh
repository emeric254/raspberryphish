
echo "1" > /proc/sys/net/ipv4/ip_forward

iptables -F

sleep 1

iptables -i wlan0 -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

iptables -i wlan0 -A INPUT -j DROP

iptables -i wlan0 -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -i wlan0 -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -i wlan0 -A INPUT -p tcp --dport $SSHPORT -j ACCEPT
iptables -i wlan0 -A INPUT -p udp --dport 53 -j ACCEPT
iptables -i wlan0 -A INPUT -p udp --dport 67:68 -j ACCEPT


sh -c "iptables-save > /etc/iptables.rules"
