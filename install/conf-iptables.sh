
iptables -F
iptables -i wlan0 -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -i wlan0 -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -i wlan0 -A INPUT -p udp --dport 53 -j ACCEPT
iptables -i wlan0 -A INPUT -p udp --dport 67:68 -j ACCEPT
iptables -i wlan0 -A INPUT -j DROP
sh -c "iptables-save > /etc/iptables.rules"
