sudo ifconfig eth0 192.168.40.35 netmask 255.255.255.0
sudo route add default gw 192.168.40.3
scripts/switch.sh 192.168.40.35 192.168.40.36
