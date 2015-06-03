
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
