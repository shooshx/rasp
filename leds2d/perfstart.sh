#!/bin/bash

sudo service ntp stop
sudo service triggerhappy stop
sudo service dbus stop
sudo killall console-kit-daemon
sudo killall polkitd
sudo mount -o remount,size=128M /dev/shm
killall gvfsd
killall dbus-daemon
killall dbus-launch
echo -n performance | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
