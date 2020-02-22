# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import arp
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.ip_to_mac = {'10.10.1.1':'a0:36:9f:85:7f:2b',
                          '10.10.1.2':'a0:36:9f:85:7f:00',
                          '10.10.1.3':'a0:36:9f:85:7f:b1',
                          '10.10.1.4':'a0:36:9f:85:7f:c9',
                          '10.10.1.5':'a0:36:9f:85:c1:81',
                          '10.10.1.6':'a0:36:9f:85:7f:dd',
                          '10.10.1.7':'a0:36:9f:85:7f:55',
                          '10.10.1.8':'a0:36:9f:85:83:7d'}
        # self.mac_to_port = {1:{'00:24:e8:77:8d:5':1, '00:24:e8:77:8d:5b':2, '00:24:e8:77:8d:5':3, '00:10:18:56:90:9c':4}}
        self.mac_to_port = {1:{'a0:36:9f:85:7f:2b':4, 'a0:36:9f:85:7f:00':1, 'a0:36:9f:85:7f:b1':3, 'a0:36:9f:85:7f:c9':2, 'a0:36:9f:85:c1:81':3, 'a0:36:9f:85:7f:dd':2, 'a0:36:9f:85:7f:55':3, 'a0:36:9f:85:83:7d':2},
                            2:{'a0:36:9f:85:7f:2b':1, 'a0:36:9f:85:7f:00':2, 'a0:36:9f:85:7f:b1':4, 'a0:36:9f:85:7f:c9':3, 'a0:36:9f:85:c1:81':1, 'a0:36:9f:85:7f:dd':2, 'a0:36:9f:85:7f:55':1, 'a0:36:9f:85:83:7d':2},
                            3:{'a0:36:9f:85:7f:2b':1, 'a0:36:9f:85:7f:00':4, 'a0:36:9f:85:7f:b1':1, 'a0:36:9f:85:7f:c9':4, 'a0:36:9f:85:c1:81':2, 'a0:36:9f:85:7f:dd':3, 'a0:36:9f:85:7f:55':1, 'a0:36:9f:85:83:7d':4},
                            4:{'a0:36:9f:85:7f:2b':4, 'a0:36:9f:85:7f:00':2, 'a0:36:9f:85:7f:b1':4, 'a0:36:9f:85:7f:c9':2, 'a0:36:9f:85:c1:81':4, 'a0:36:9f:85:7f:dd':2, 'a0:36:9f:85:7f:55':1, 'a0:36:9f:85:83:7d':3},
                            5:{'a0:36:9f:85:7f:2b':3, 'a0:36:9f:85:7f:00':3, 'a0:36:9f:85:7f:b1':1, 'a0:36:9f:85:7f:c9':1, 'a0:36:9f:85:c1:81':4, 'a0:36:9f:85:7f:dd':2, 'a0:36:9f:85:7f:55':4, 'a0:36:9f:85:83:7d':2},
                            6:{'a0:36:9f:85:7f:2b':2, 'a0:36:9f:85:7f:00':2, 'a0:36:9f:85:7f:b1':3, 'a0:36:9f:85:7f:c9':3, 'a0:36:9f:85:c1:81':1, 'a0:36:9f:85:7f:dd':4, 'a0:36:9f:85:7f:55':1, 'a0:36:9f:85:83:7d':4},
                            7:{'a0:36:9f:85:7f:2b':2, 'a0:36:9f:85:7f:00':3, 'a0:36:9f:85:7f:b1':2, 'a0:36:9f:85:7f:c9':3, 'a0:36:9f:85:c1:81':1, 'a0:36:9f:85:7f:dd':1, 'a0:36:9f:85:7f:55':4, 'a0:36:9f:85:83:7d':4},
                            8:{'a0:36:9f:85:7f:2b':3, 'a0:36:9f:85:7f:00':1, 'a0:36:9f:85:7f:b1':3, 'a0:36:9f:85:7f:c9':1, 'a0:36:9f:85:c1:81':4, 'a0:36:9f:85:7f:dd':4, 'a0:36:9f:85:7f:55':2, 'a0:36:9f:85:83:7d':2},
                            9:{'a0:36:9f:85:7f:2b':1, 'a0:36:9f:85:7f:00':1, 'a0:36:9f:85:7f:b1':4, 'a0:36:9f:85:7f:c9':4, 'a0:36:9f:85:c1:81':2, 'a0:36:9f:85:7f:dd':2, 'a0:36:9f:85:7f:55':3, 'a0:36:9f:85:83:7d':3},
                            10:{'a0:36:9f:85:7f:2b':2, 'a0:36:9f:85:7f:00':2, 'a0:36:9f:85:7f:b1':4, 'a0:36:9f:85:7f:c9':4, 'a0:36:9f:85:c1:81':1, 'a0:36:9f:85:7f:dd':1, 'a0:36:9f:85:7f:55':3, 'a0:36:9f:85:83:7d':3},}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        self.add_initial_flow(ev)

    def add_initial_flow(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id
        # self.logger.info("switch %s" % dpid)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        #pkt = packet.Packet(msg.data)
        #pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        for dst in self.mac_to_port[dpid]:
            match = parser.OFPMatch(eth_dst=dst)
            out_port = self.mac_to_port[dpid][dst]
            action = [parser.OFPActionOutput(out_port)]
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, action)]
            mod = parser.OFPFlowMod(datapath=datapath, priority=1, match=match, instructions=inst)
            datapath.send_msg(mod)

        self.logger.info("Added Initial rules to switch %s" % dpid)


    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        pkt_arp = pkt.get_protocol(arp.arp)

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        elif dst == 'ff:ff:ff:ff:ff:ff':
            ip_dst = pkt_arp.dst_ip
            dst = self.ip_to_mac[ip_dst]
            out_port = self.mac_to_port[dpid][dst]

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        # if out_port != ofproto.OFPP_FLOOD:
        match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            # if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                # self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                # return
            # else:
                # self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
