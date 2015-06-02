
sed -i "/DHCPD_ENABLED/c\DHCPD_ENABLED=\"yes\"" /etc/default/udhcpd

cat <<EOF > /etc/udhcpd.conf
start       10.0.0.2
end     10.0.0.254
interface   $INTERFACE
max_leases 254
auto_time  3600
decline_time   1800
conflict_time  1800
offer_time 60
min_lease  60
opt dns 10.0.0.1
option  subnet  255.255.255.0
opt router  10.0.0.1
option  domain  local
option  lease   1000
EOF
