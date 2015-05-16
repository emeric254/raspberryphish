
# cp launcher script
cp  ./install/launcher-raspberryphish-server.sh  "$SERVERPATH/"

# configure it
echo  "cd $SERVERPATH"  >>  $SERVERPATH."/launcher-raspberryphish-server.sh"
echo  "python3 main.py >> ./logs/log-$(date +%Y%m%d)"  >>  $SERVERPATH."/launcher-raspberryphish-server.sh"

# copy server in the given directory
cp -r  ./server/*  "$SERVERPATH/"

# make a log folder
mkdir  $SERVERPATH."/logs"
