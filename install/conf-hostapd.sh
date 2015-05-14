
echo "interface=$INTERFACE" >> /etc/hostapd/hostapd.conf
echo "driver=$DRIVER" >> /etc/hostapd/hostapd.conf
echo "channel=$CHANNEL" >> /etc/hostapd/hostapd.conf
echo "ssid=$SSID" >> /etc/hostapd/hostapd.conf

sed '/DAEMON_CONF=/c DAEMON_CONF=/etc/hostapd/hostapd.conf' /etc/init.d/hostapd
