# import Overlord.Forwarding
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr, IPAddr

class Forwarding(object):
    """Create Forwarding rules for Host to Host communication"""
    def __init__(self):
        pass

    def Connect(self, log, db, devices, links, host1, host2):
        # Supply third arg to use a better strategy
        path = links.ResolvePath(host1, host2)
        
        # The hosts reside on the same switch
        if path == []:
            # host1 -> host2
            fmod = of.ofp_flow_mod(idle_timeout=600)
            fmod.match.dl_src = EthAddr(host1["mac"])
            #fmod.match.dl_type = 0x0800
            #fmod.match.nw_dst = IPAddr(str(host2["ip"]))
            fmod.match.dl_dst = EthAddr(host2["mac"])
            fmod.actions.append(of.ofp_action_output(port=int(host2["port_no"])))
            # THIS HAS TO CHANGE
            devices.Connection(log, host1["_parent"]).send(fmod)
            #event.connection.send(fmod)
            # host2 -> host1
            fmod = of.ofp_flow_mod(idle_timeout=600)
            fmod.match.dl_src = EthAddr(host2["mac"])
            #fmod.match.dl_type = 0x0800
            #fmod.match.nw_dst = IPAddr(str(host1["ip"]))
            fmod.match.dl_dst = EthAddr(host1["mac"])
            fmod.actions.append(of.ofp_action_output(port=int(host1["port_no"])))
            # THIS HAS TO CHANGE
            devices.Connection(log, host1["_parent"]).send(fmod)
            #event.connection.send(fmod)

            #msg = of.ofp_flow_mod(idle_timeout=5)
            #msg.match.dl_src = arp_pkt.hwsrc
            #msg.match.dl_src = EthAddr(host2["mac"])#arp_pkt.hwsrc
            #msg.match.dl_type = 0x0806
            #msg.match.protodst = arp_pkt.protodst
            #msg.match.dl_dst = EthAddr(host1["mac"])#arp_pkt.hwdst
            #msg.actions.append(of.ofp_action_output(port=int(host1["port_no"])))
            #event.connection.send(msg)

        log.info("Adding flows to connect devices: " + str(host1["_name"]) + " and " + str(host2["_name"]))

    def Disconnect(self, log, devices, host):
        conn = devices.Connection(log, host["_parent"])

        # Remove the from host rules
        fmod1 = of.ofp_flow_mod()
        fmod1.match.dl_src = EthAddr(host["mac"])
        fmod1.command = of.OFPFC_DELETE
        # Remove the to host rules
        fmod2 = of.ofp_flow_mod()
        fmod2.match.dl_dst = EthAddr(host["mac"])
        fmod2.command = of.OFPFC_DELETE

        try:
            conn.send(fmod1)
            conn.send(fmod2)
            log.info("Removing flows to disconnect device: " + str(host["_name"]))
        except AttributeError:
            pass

    def Group(self, log, db, devices, links, host):
        """
        Builds connections between host and all of his group members.
        """
        group_members = db.hosts.find({"group_no": host["group_no"]})
        for h in group_members:
            self.Connect(log, db, devices, links, host, h)

    def Ungroup(self):
        pass
