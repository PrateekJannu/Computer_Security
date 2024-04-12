#!bin/sh



#1
#Clears and deletes all rules within the raw table.
sudo iptables -t raw -F
sudo iptables -t raw -X

#Clears and deletes all rules within the nat table.
sudo iptables -t nat -F
sudo iptables -t nat -X

#Clears and deletes all rules within the mangle table.
sudo iptables -t mangle -F
sudo iptables -t mangle -X

#Clears and deletes all rules within the filter table.
sudo iptables -t filter -F
sudo iptables -t filter -X



#2

#Accepts incoming traffic from the source f1.com
sudo iptables -t filter -A INPUT -s f1.com -j ACCEPT



#3

#Applies NAT to outgoing packets, masquerading them
sudo iptables -t nat -A POSTROUTING -j MASQUERADE




#4

#Limits incoming TCP traffic
sudo iptables -t filter -A INPUT -p tcp --tcp-flags SYN,ACK,FIN,RST NONE -m limit --limit 1/s -j ACCEPT





#5

#Limits incoming SYN packets.
sudo iptables -t filter -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 500 -j ACCEPT



#6

# Accepts all loopback traffic.

sudo iptables -t filter -A INPUT -i lo -j ACCEPT
sudo iptables -t filter -A OUTPUT -o lo -j ACCEPT




#7

#Redirects incoming TCP traffic on port 8888 to port 25565.

sudo iptables -t nat -A PREROUTING -p tcp --dport 8888 -j REDIRECT --to-ports 25565




#8

# Accepts SSH connections from engineering.purdue.edu (128.46.104.20) in the established state.
sudo iptables -t filter -A INPUT -p tcp --dport 22 -s 128.46.104.20 -m state --state ESTABLISHED -j ACCEPT

sudo iptables -t filter -A OUTPUT -p tcp --dport 22 -d 128.46.104.20 -m state --state NEW,ESTABLISHED -j ACCEPT



#9

# Drops other traffic.



sudo iptables -t filter -A INPUT -j DROP


sudo iptables -t filter -A OUTPUT -j DROP



sudo iptables -t filter -A FORWARD -j DROP
