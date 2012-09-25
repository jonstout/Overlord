# Overlord 2012

def learn_device(pkt):
    """ learn_device(pkt)
    Add device information to the database. Everything we can learn,
    src mac, src ip, in_port, and dpid.
    """
    add_device(pkt.src_mac, pkt.src_ip, pkt.in_port, pkt.dpid)
    push_drop_rule(pkt.src_mac)

def group_device(name, group_no):
    """ group_device(name, group_no)
    Use src_mac and group dst_mac's to build forwarding rules on
    dpid (when going cross switch be sure to include trunk ports).
    """
    push_group_rules(name, group_no)

def ungroup_device(name, group_no):
    """ ungroup_device(name, group_no)
    Destroy all src_mac and dst_mac matches removing the name'd
    device from the forwarding tables. Replace with drop rules.
    """
    src_mac = del_group_rules(name, group_no)
    push_drop_rule(src_mac)

def get_message(msg):
    cmd_parts = overlord.parse_msg(msg)

    if (cmd_parts.cmd == "ungroup"):
        pass
    else if (cmd_parts.cmd == "group"):
        pass
    else:
        pass