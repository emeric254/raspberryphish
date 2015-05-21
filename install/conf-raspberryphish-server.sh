

# configure launcher script
echo  '#!/bin/sh'  >  "$SERVERPATH/launcher-raspberryphish-server.sh"
echo  '# launcher for raspberryphish server'  >>  "$SERVERPATH/launcher-raspberryphish-server.sh"
echo  'sleep 10'  >>  "$SERVERPATH/launcher-raspberryphish-server.sh"
echo  "cd $SERVERPATH"  >>  "$SERVERPATH/launcher-raspberryphish-server.sh"
echo  "python3 main.py 1>> ./logs/log-$(date +%Y-%m-%d_%H-%M) 2>> ./logs/log-error-$(date +%Y-%m-%d_%H-%M) &"  >>  "$SERVERPATH/launcher-raspberryphish-server.sh"

# make it launchable
chmod 755 "$SERVERPATH/launcher-raspberryphish-server.sh"


# copy server in the given directory
cp -r  ./server/*  "$SERVERPATH/"

# replace the root page folder
sed -i "/pagePath = \"test\/\"/c pagePath = \"$PAGE\/\"" $SERVERPATH/main.py


# make a cert folder
#mkdir  "$SERVERPATH/cert"
#mkdir  "$SERVERPATH/cert/$PAGE"


# make a log folder
mkdir  "$SERVERPATH/logs"
mkdir  "$SERVERPATH/logs/dump"


# configure cron-file
echo  "@reboot sh $SERVERPATH/launcher-raspberryphish-server.sh 1> $SERVERPATH/logs/cronlog 2> $SERVERPATH/logs/cronlog-error &"  >  ./install/cron-file

# load it
crontab ./install/cron-file
