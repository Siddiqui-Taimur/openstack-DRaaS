sudo ifconfig eth0 192.168.40.36 netmask 255.255.255.0
sudo route add default gw 192.168.40.3
#mysql keystone <<EOF
#update endpoint set url = REPLACE(url, '192.168.40.32', '192.168.40.32');
#commit;
#EOF
#if [ -f /etc/draas/keystone.conf ];
#then
#    mv /etc/draas/keystone.conf /recover/draas/keystone.conf
#fi

#grep -rl '192.168.40.32' /etc | xargs sed -i 's/192.168.40.32/192.168.40.32/g'
#grep -rl $2 /opt/stack | xargs sed -i 's/192.168.40.32/192.168.40.32/g'
#if [ -f /recover/draas/keystone.conf ];
#then
#    mv /recover/draas/keystone.conf /etc/draas/keystone.conf
#fi


scripts/switch.sh 192.168.40.36 192.168.40.35
