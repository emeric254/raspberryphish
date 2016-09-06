
cat <<EOF > $SERVERPATH/hostapd.conf
interface=$INTERFACE
driver=$DRIVER
channel=$CHANNEL
ssid=$SSID
ignore_broadcast_ssid=0
auth_algs=1
hw_mode=g
macaddr_acl=0

dtim_period=2
max_num_sta=255
rts_threshold=2347
fragm_threshold=2346
wmm_enabled=0
EOF


# radius
if [ $ACTIVATERADIUS -eq 1 ]
then

cat <<EOF > $SERVERPATH/hostapd.conf
interface=$INTERFACE
driver=$DRIVER
channel=$CHANNEL
ssid=$SSID
ignore_broadcast_ssid=0
hw_mode=g
macaddr_acl=0

dtim_period=2
max_num_sta=255
rts_threshold=2347
fragm_threshold=2346
wmm_enabled=0

auth_algs=3
wpa=3
wpa_key_mgmt=WPA-EAP
wpa_pairwise=TKIP CCMP
wpa_ptk_rekey=300
ieee8021x=1
eap_server=0
own_ip_addr=10.0.0.1
nas_identifier=localhost
auth_server_addr=$AUTHSERVER
auth_server_port=$AUTHPORT
auth_server_shared_secret=$RADIUSSECRET
acct_server_addr=$ACCTSERVER
acct_server_port=$ACCTPORT
acct_server_shared_secret=$RADIUSSECRET
EOF

fi

