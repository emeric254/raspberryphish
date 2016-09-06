
# configure launcher script
cat <<EOF > "$SERVERPATH/launcher-raspberryphish-server.sh"
#!/bin/bash
# launcher for raspberryphish server

echo "move to working directory"
cd $SERVERPATH
sleep 5 # sleep 5s to wait boot end

echo "stop dhcpcd"
/etc/init.d/dhcpcd stop
/usr/bin/killall dhcpcd
/usr/bin/killall /sbin/dhcpcd

echo "stop hostapd"
/etc/init.d/hostapd stop
/usr/bin/killall hostapd
echo "start hostapd"
#~ /etc/init.d/hostapd restart >> ./logs/hostapd &
/usr/sbin/hostapd -B hostapd.conf >> ./logs/hostapd &

sleep 2 # wait hostapd initialisation ...

echo "stop all network interfaces"
/sbin/ifdown $INTERFACE
/sbin/ifdown -i ./interfaces $INTERFACE

sleep 2 # wait ifstate changement ...

echo "start wlan0"
/sbin/ifup -i ./interfaces $INTERFACE

echo "stop dnsmasq"
/etc/init.d/dnsmasq stop
/usr/bin/killall dnsmasq
echo "start dnsmasq"
/usr/sbin/dnsmasq -C dnsmasq.conf >> ./logs/dnsmasq &

echo "launch the server"
python3 main.py >> ./logs/server &
EOF


# make it launchable
chmod 755 "$SERVERPATH/launcher-raspberryphish-server.sh"

# configure cron-file
echo  "@reboot sh $SERVERPATH/launcher-raspberryphish-server.sh 1> $SERVERPATH/logs/cronlog 2> $SERVERPATH/logs/cronlog-error &"  >  ./install/cron-file




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


# load the crontab file
crontab ./install/cron-file

