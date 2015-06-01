
echo "interface=$INTERFACE" > /etc/hostapd/hostapd.conf
echo "driver=$DRIVER" >> /etc/hostapd/hostapd.conf
echo "channel=$CHANNEL" >> /etc/hostapd/hostapd.conf
echo "ssid=$SSID" >> /etc/hostapd/hostapd.conf

# radius
if [[ $ACTIVATERADIUS ]]
then
    echo 'ieee8021x=1' >> /etc/hostapd/hostapd.conf
#    echo "nas_identifier=$NASID" >> /etc/hostapd/hostapd.conf
    echo "auth_server_addr=$AUTHSERVER" >> /etc/hostapd/hostapd.conf
    echo "auth_server_port=$AUTHPORT" >> /etc/hostapd/hostapd.conf
    echo "acct_server_addr=$ACCTSERVER" >> /etc/hostapd/hostapd.conf
    echo "acct_server_port=$ACCTPORT" >> /etc/hostapd/hostapd.conf
    echo "auth_server_shared_secret=$RADIUSSECRET" >> /etc/hostapd/hostapd.conf
    echo "acct_server_shared_secret=$RADIUSSECRET" >> /etc/hostapd/hostapd.conf
fi

sed -i '/DAEMON_CONF=/c DAEMON_CONF=/etc/hostapd/hostapd.conf' /etc/init.d/hostapd
