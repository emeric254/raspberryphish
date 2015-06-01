
echo "interface=$INTERFACE" > /etc/hostapd/hostapd.conf
echo "driver=$DRIVER" >> /etc/hostapd/hostapd.conf
echo "channel=$CHANNEL" >> /etc/hostapd/hostapd.conf
echo "ssid=$SSID" >> /etc/hostapd/hostapd.conf

# radius
if [$radius -eq 1]
then
    echo "nas_identifier=$NASID" >> /etc/hostapd/hostapd.conf
    echo "auth_server_addr=$AUTHSERVER" >> /etc/hostapd/hostapd.conf
    echo "auth_server_port=$AUTHPORT" >> /etc/hostapd/hostapd.conf
    echo "acct_server_addr=$ACCTSERVER" >> /etc/hostapd/hostapd.conf
    echo "acct_server_port=$ACCTPORT" >> /etc/hostapd/hostapd.conf

auth_server_shared_secret=supersecretradiuskey  # This is used to authenticate the hostapd to the radius server so none can use your raduis server
acct_server_shared_secret=supersecretradiuskey # Same as above

fi

sed -i '/DAEMON_CONF=/c DAEMON_CONF=/etc/hostapd/hostapd.conf' /etc/init.d/hostapd
