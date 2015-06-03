
#~ update-rc.d hostapd defaults
#~ update-rc.d dnsmasq defaults


# configure launcher script
cat <<EOF > "$SERVERPATH/launcher-raspberryphish-server.sh"
#!/bin/sh
# launcher for raspberryphish server
ifup $INTERFACE
/etc/init.d/dnsmasq start
/etc/init.d/hostapd start
sleep 5
cd $SERVERPATH
python3 main.py 1>> ./logs/log-$(date +%Y-%m-%d_%H-%M) 2>> ./logs/log-error-$(date +%Y-%m-%d_%H-%M) &
EOF

# make it launchable
chmod 755 "$SERVERPATH/launcher-raspberryphish-server.sh"

# configure cron-file
echo  "@reboot sh $SERVERPATH/launcher-raspberryphish-server.sh 1> $SERVERPATH/logs/cronlog 2> $SERVERPATH/logs/cronlog-error &"  >>  ./install/cron-file


if [ $ACTIVATERADIUS -eq 1 ]
then
# configure launcher script
cat <<EOF > "$SERVERPATH/launcher-radius-server.sh"
#!/bin/sh
# launcher for radius server
cd $SERVERPATH
freeradius -x &
EOF
# make it launchable
chmod 755 "$SERVERPATH/launcher-radius-server.sh"
# add this conf to cron-file
echo  "@reboot sh $SERVERPATH/launcher-radius-server.sh 1> $RADIUSLOGPATH/cronlog 2> $RADIUSLOGPATH/cronlog-error &"  >>  ./install/cron-file
fi


# load it
crontab ./install/cron-file
