
update-rc.d hostapd defaults
update-rc.d udhcpd defaults
update-rc.d dnsmasq defaults

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
# load it
crontab ./install/cron-file

fi
