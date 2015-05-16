
# cp launcher script
cp  ./install/launcher-raspberryphish-server.sh  "$SERVERPATH/"
chmod 755 "$SERVERPATH/launcher-raspberryphish-server.sh"

# configure it
echo  '#!/bin/sh'  >  "$SERVERPATH/launcher-raspberryphish-server.sh"
echo  '# launcher for raspberryphish server'  >  "$SERVERPATH/launcher-raspberryphish-server.sh"
echo  "cd $SERVERPATH"  >>  "$SERVERPATH/launcher-raspberryphish-server.sh"
echo  "python3 main.py >> ./logs/log-$(date +%Y%m%d)"  >>  "$SERVERPATH/launcher-raspberryphish-server.sh"

# copy server in the given directory
cp -r  ./server/*  "$SERVERPATH/"

# make a log folder
mkdir  "$SERVERPATH/logs"

# configure cron-file
echo  "@reboot sh $SERVERPATH/launcher-raspberryphish-server.sh > $SERVERPATH/logs/cronlog 2>&1"  >  ./install/cron-file

# load it
crontab ./install/cron-file
