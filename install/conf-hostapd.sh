
echo "interface=$INTERFACE" > /etc/hostapd/hostapd.conf
echo "driver=$DRIVER" >> /etc/hostapd/hostapd.conf
echo "channel=$CHANNEL" >> /etc/hostapd/hostapd.conf
echo "ssid=$SSID" >> /etc/hostapd/hostapd.conf

# radius
if [[ $ACTIVATERADIUS ]]
then
    echo 'ieee8021x=1' >> /etc/hostapd/hostapd.conf


## WPA ##

cat <<EOF >> /etc/hostapd/hostapd.conf
wpa=3
wpa_key_mgmt=WPA-EAP
wpa_pairwise=TKIP CCMP
wpa_ptk_rekey=300

nas_identifier=localhost
auth_server_addr=$AUTHSERVER
auth_server_port=$AUTHPORT
auth_server_shared_secret=$RADIUSSECRET
auth_algs=3
acct_server_addr=$ACCTSERVER
acct_server_port=$ACCTPORT
acct_server_shared_secret=$RADIUSSECRET
own_ip_addr=127.0.0.1
EOF

fi

sed -i '/DAEMON_CONF=/c DAEMON_CONF=/etc/hostapd/hostapd.conf' /etc/init.d/hostapd
