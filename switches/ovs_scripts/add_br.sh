ifconfig enp6s0f0 0
ifconfig enp6s0f1 0
ifconfig enp6s0f2 0
ifconfig enp6s0f3 0
ovs-vsctl add-br ovs-e3
ovs-vsctl set bridge ovs-e3 protocols=OpenFlow13
ovs-vsctl set bridge ovs-e3 other-config:datapath-id=0000000000000004
ovs-vsctl add-port ovs-e3 enp6s0f0
ovs-vsctl add-port ovs-e3 enp6s0f1
ovs-vsctl add-port ovs-e3 enp6s0f2
ovs-vsctl add-port ovs-e3 enp6s0f3
ovs-vsctl set-controller ovs-e3 tcp:128.105.145.234:6633
# ovs-vsctl set bridge ovs-e3 stp_enable=true
ovs-vsctl set-fail-mode ovs-e3 secure
ovs-vsctl show
