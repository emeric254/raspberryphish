
echo "interface=$INTERFACE" > /etc/hostapd/hostapd.conf
echo "driver=$DRIVER" >> /etc/hostapd/hostapd.conf
echo "channel=$CHANNEL" >> /etc/hostapd/hostapd.conf
echo "ssid=$SSID" >> /etc/hostapd/hostapd.conf

cat <<EOF >> /etc/hostapd/hostapd.conf
#ignore_broadcast_ssid=0
#auth_algs=1
#hw_mode=g
#macaddr_acl=0

#dtim_period=2
#max_num_sta=255
#rts_threshold=2347
#fragm_threshold=2346
#wmm_enabled=0
EOF


# radius
if [ $ACTIVATERADIUS -eq 1 ]
then
cat <<EOF >> /etc/hostapd/hostapd.conf
auth_algs=3
wpa=3
wpa_key_mgmt=WPA-EAP
wpa_pairwise=TKIP CCMP
wpa_ptk_rekey=300
ieee8021x=1
eap_server=0
own_ip_addr=10.0.0.254
nas_identifier=localhost
EOF
echo "auth_server_addr=$AUTHSERVER" >> /etc/hostapd/hostapd.conf
echo "auth_server_port=$AUTHPORT" >> /etc/hostapd/hostapd.conf
echo "auth_server_shared_secret=$RADIUSSECRET" >> /etc/hostapd/hostapd.conf
echo "acct_server_addr=$ACCTSERVER" >> /etc/hostapd/hostapd.conf
echo "acct_server_port=$ACCTPORT" >> /etc/hostapd/hostapd.conf
echo "acct_server_shared_secret=$RADIUSSECRET" >> /etc/hostapd/hostapd.conf
fi


sed -i '/DAEMON_CONF/c\DAEMON_CONF=/etc/hostapd/hostapd.conf' /etc/init.d/hostapd
sed -i '/DAEMON_CONF/c\DAEMON_CONF=/etc/hostapd/hostapd.conf' /etc/default/hostapd
