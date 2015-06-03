
echo "1" > /proc/sys/net/ipv4/ip_forward
sed -i "/net.ipv4.ip_forward/c\net.ipv4.ip_forward=1" /etc/sysctl.conf


iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain

iptables -i wlan0 -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

iptables -i wlan0 -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -i wlan0 -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -i wlan0 -A INPUT -p tcp --dport $SSHPORT -j ACCEPT
iptables -i wlan0 -A INPUT -p udp --dport 53 -j ACCEPT
iptables -i wlan0 -A INPUT -p udp --dport 67:68 -j ACCEPT

#sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
#sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
#sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

iptables -i wlan0 -A INPUT -j DROP


sh -c "iptables-save > /etc/iptables.rules"
