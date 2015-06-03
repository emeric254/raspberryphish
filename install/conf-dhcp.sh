
sed -i "/DHCPD_ENABLED/c\DHCPD_ENABLED=\"yes\"" /etc/default/udhcpd

cat <<EOF > /etc/udhcpd.conf
start       10.0.0.2
end     10.0.0.254
interface   $INTERFACE
remaining yes
opt dns 10.0.0.1
option  subnet  255.255.255.0
opt router  10.0.0.1
option  lease   1800
EOF
