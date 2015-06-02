
# configure /etc/freeradius/radiusd.conf

mkdir $RADIUSLOGPATH

sed -i "/logdir = /c\logdir = $RADIUSLOGPATH" /etc/freeradius/radiusd.conf

sed -i '/hostname_lookups = /c\hostname_lookups = no' /etc/freeradius/radiusd.conf

sed -i '/destination = /c\destination = files' /etc/freeradius/radiusd.conf

sed -i '/file = ${logdir}/c\file = ${logdir}/radius.log' /etc/freeradius/radiusd.conf

sed -i '/stripped_names = /c\stripped_names = yes' /etc/freeradius/radiusd.conf

sed -i '/stripped_names = /c\stripped_names = yes' /etc/freeradius/radiusd.conf

sed -i '/auth = /c\auth = yes' /etc/freeradius/radiusd.conf

sed -i '/auth_goodpass = /c\auth_goodpass = yes' /etc/freeradius/radiusd.conf
sed -i '/auth_badpass = /c\auth_badpass = yes' /etc/freeradius/radiusd.conf

sed -i '/reject_delay = /c\reject_delay = 3' /etc/freeradius/radiusd.conf

sed -i '/status_server = /c\status_server = yes' /etc/freeradius/radiusd.conf



sed -i '/use_tunneled_reply = /c\use_tunneled_reply = no' /etc/freeradius/eap.conf

sed -i '/copy_request_to_tunnel = /c\copy_request_to_tunnel = yes' /etc/freeradius/eap.conf



# configure /etc/freeradius/clients.conf

cat <<EOF > /etc/freeradius/clients.conf
# -*- text -*-
client localhost {
    ipaddr = 127.0.0.1
    secret      = $RADIUSSECRET
    require_message_authenticator = no
    nastype     = other # localhost isn't usually a NAS...
}
EOF
