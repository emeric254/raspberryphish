
update-rc.d hostapd defaults
update-rc.d dnsmasq defaults

if [[ $ACTIVATERADIUS ]]
then
    update-rc.d freeradius defaults
fi
