ovs-vsctl del-br ovs-e0
ifconfig eno2 10.10.2.1 netmask 255.255.255.0 broadcast 10.10.2.255
ifconfig eno3 10.10.6.2 netmask 255.255.255.0 broadcast 10.10.6.255
ifconfig eno4 10.10.1.1 netmask 255.255.255.0 broadcast 10.10.1.255
ifconfig enp5s0f0 10.10.5.2 netmask 255.255.255.0 broadcast 10.10.5.255
