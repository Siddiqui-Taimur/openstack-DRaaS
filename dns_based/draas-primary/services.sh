#!/usr/bin/env bash

if [[ -n `dpkg -l | grep vsftpd` ]]; then
echo "vsftpd already installed";
else apt-get -y install vsftpd
fi
sed -i 's/anonymous_enable=NO/anonymous_enable=YES/g' /etc/vsftpd.conf
sed -i 's/#write_enable=YES/write_enable=YES/g' /etc/vsftpd.conf
echo "Anonymous FTP enabled"
path="local_root=/etc/draas/"
result=$(grep "local_root" /etc/vsftpd.conf)
if [ -z $result ]
then
    sed -i -e '$a\'"$path" /etc/vsftpd.conf
else
    sed -i "s|"$result"|"$path"|" /etc/vsftpd.conf
fi
echo "Local root Added"
ip="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
sed -i "/local_ip=/c\local_ip="$ip /etc/draas/keystone.conf
service vsftpd restart
sed -i 's/#log_bin			= \/var\/log\/mysql\/mysql-bin.log/log_bin                      = \/var\/log\/mysql\/mysql-bin.log/g' /etc/mysql/my.cnf
echo "MySQL Logs Enabled"
service mysql restart
