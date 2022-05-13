#!/bin/sh

# My system IP/set ip address of server
MY_OWN_IP="YOUR.PUBLIC.IP.ADDR"

function flush_all_rules() {
    iptables -F
    iptables -X
}

function set_default_filter_policy() {
    iptables -P INPUT DROP
    iptables -P OUTPUT DROP
    iptables -P FORWARD DROP
}

function allow_unlimited_traffic_on_loopback() {
    iptables -A INPUT -i lo -j ACCEPT
    iptables -A OUTPUT -o lo -j ACCEPT
}

function allow_incoming_ssh_only() {
    iptables -A INPUT -p tcp -s $MY_OWN_IP  --sport 513:65535 --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -A OUTPUT -p tcp -d $MY_OWN_IP --sport 22 --dport 513:65535 -m state --state ESTABLISHED -j ACCEPT
}

# make sure nothing comes or goes out of this box
function jail_the_box() {
    iptables -A INPUT -j DROP
    iptables -A OUTPUT -j DROP
}

=========================================
function test_firewalld() {
    firewall-cmd --add-rich-rule="rule family="ipv4" source address="$MY_OWN_IP" service name="ssh" accept"
    firewall-cmd --zone=internal --add-service=ssh
    firewall-cmd --zone=internal --add-source=192.168.56.105/32
    firewall-cmd --zone=internal --add-source=192.168.56.120/32
    firewall-cmd --zone=public --remove-service=ssh
}

#test_firewalld
=========================================

function isolate_instance() {
    flush_all_rules
    set_default_filter_policy
    allow_unlimited_traffic_on_loopback
    allow_incoming_ssh_only
    jail_the_box
}


isolate_instance
