

# configure launcher script
echo  '#!/bin/sh'  >  "$SERVERPATH/launcher-raspberryphish-server.sh"
echo  '# launcher for raspberryphish server'  >>  "$SERVERPATH/launcher-raspberryphish-server.sh"
echo  "cd $SERVERPATH"  >>  "$SERVERPATH/launcher-raspberryphish-server.sh"
echo  "python3 main.py > ./logs/log-$(date +%Y-%m-%d_%H-%M)"  >>  "$SERVERPATH/launcher-raspberryphish-server.sh"

# make it launchable
chmod 755 "$SERVERPATH/launcher-raspberryphish-server.sh"


# copy server in the given directory
cp -r  ./server/*  "$SERVERPATH/"

# make a log folder
mkdir  "$SERVERPATH/logs"

# configure cron-file
echo  "@reboot sh $SERVERPATH/launcher-raspberryphish-server.sh > $SERVERPATH/logs/cronlog 2>&1"  >  ./install/cron-file

# load it
crontab ./install/cron-file
