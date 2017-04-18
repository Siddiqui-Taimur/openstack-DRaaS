#!/usr/bin/env bash


/home/linux/devstack/unstack.sh

mysql keystone <<EOF
update endpoint set url = REPLACE(url, '$2', '$1');
commit;
EOF

if [ -f /etc/draas/keystone.conf ];
then
    mv /etc/draas/keystone.conf /recover/draas/keystone.conf
fi

sudo grep -rl $2 /etc | xargs sed -i 's/'$2'/'$1'/g'
sudo grep -rl $2 /opt/stack | xargs sed -i 's/'$2'/'$1'/g'
echo "Files Replaced"
if [ -f /recover/draas/keystone.conf ];
then
    mv /recover/draas/keystone.conf /etc/draas/keystone.conf
fi


gnome-terminal -x /home/linux/devstack/rejoin-stack.sh
gnome-terminal -x keystone-all

sudo service apache2 start
echo "Script Done"
