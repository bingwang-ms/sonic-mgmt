def _port_alias_to_name_map_50G(all_ports, s100G_ports,):
    new_map = {}
    # 50G ports
    s50G_ports = list(set(all_ports) - set(s100G_ports))

    for i in s50G_ports:
        new_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 1) * 4)
        new_map["Ethernet%d/3" % i] = "Ethernet%d" % ((i - 1) * 4 + 2)

    for i in s100G_ports:
        new_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 1) * 4)

    return new_map

def get_port_alias_to_name_map(hwsku, asic_id=None):
    port_alias_to_name_map = {}
    port_alias_asic_map = {}
    if hwsku == "Force10-S6000":
        for i in range(0, 128, 4):
            port_alias_to_name_map["fortyGigE0/%d" % i] = "Ethernet%d" % i
    elif hwsku == "Force10-S6100":
        for i in range(0, 4):
            for j in range(0, 16):
                port_alias_to_name_map["fortyGigE1/%d/%d" % (i+1, j+1)] = "Ethernet%d" % (i * 16 + j)
    elif hwsku in ["Force10-Z9100-C32", "DellEMC-S5232f-C32"]:
        for i in range(0, 128, 4):
            port_alias_to_name_map["hundredGigE1/%d" % (i / 4 + 1)] = "Ethernet%d" % i
    elif hwsku == "DellEMC-Z9332f-M-O16C64":
        # 100G ports
        s100G_ports = [x for x in range(0, 96, 2)] + [x for x in range(128, 160, 2)]

        # 400G ports
        s400G_ports = [x for x in range(96, 128, 8)] + [x for x in range(160, 256, 8)]

        # 10G ports
        s10G_ports = [x for x in range(256, 258)]

        for i in s100G_ports:
            alias = "hundredGigE1/{}/{}".format(((i + 8) // 8), ((i // 2) % 4) + 1)
            port_alias_to_name_map[alias] = "Ethernet{}".format(i)
        for i in s400G_ports:
            alias = "fourhundredGigE1/{}".format((i // 8) + 1)
            port_alias_to_name_map[alias] = "Ethernet{}".format(i)
        for i in s10G_ports:
            alias = "tenGigE1/{}".format(33 if i == 256 else 34)
            port_alias_to_name_map[alias] = "Ethernet{}".format(i)
    elif hwsku == "DellEMC-Z9332f-O32":
        for i in range(0, 256, 8):
            alias = "fourhundredGigE1/{}".format((i // 8) + 1)
            port_alias_to_name_map[alias] = "Ethernet{}".format(i)
        for i in range(256, 258):
            alias = "tenGigE1/{}".format(33 if i == 256 else 34)
            port_alias_to_name_map[alias] = "Ethernet{}".format(i)
    elif hwsku == "Arista-7050-QX32":
        for i in range(1, 25):
            port_alias_to_name_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 1) * 4)
        for i in range(25, 33):
            port_alias_to_name_map["Ethernet%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "Arista-7050-QX-32S":
        for i in range(5, 29):
            port_alias_to_name_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 5) * 4)
        for i in range(29, 37):
            port_alias_to_name_map["Ethernet%d" % i] = "Ethernet%d" % ((i - 5) * 4)
    elif hwsku in ["Arista-7260CX3-C64", "Arista-7170-64C", "Arista-7260CX3-Q64"]:
        for i in range(1, 65):
            port_alias_to_name_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "Arista-7060CX-32S-C32" or hwsku == "Arista-7060CX-32S-Q32" or hwsku == "Arista-7060CX-32S-C32-T1" or hwsku == "Arista-7170-32CD-C32":
        for i in range(1, 33):
            port_alias_to_name_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "Arista-7050CX3-32S-C32":
        for i in range(1, 33):
            port_alias_to_name_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 1) * 4)
        for i in range(33, 35):
            port_alias_to_name_map["Ethernet%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "Mellanox-SN2700-D40C8S8":
        # 10G ports
        s10G_ports = range(0, 4) + range(8, 12)

        # 50G ports
        s50G_ports = [x for x in range(16, 24, 2)] + [x for x in range(40, 88, 2)] + [x for x in range(104, 128, 2)]

        # 100G ports
        s100G_ports = [x for x in range(24, 40, 4)] + [x for x in range(88, 104, 4)]

        for i in s10G_ports:
            alias = "etp%d" % (i / 4 + 1) + chr(ord('a') + i % 4)
            port_alias_to_name_map[alias] = "Ethernet%d" % i
        for i in s50G_ports:
            alias = "etp%d" % (i / 4 + 1) + ("a" if i % 4 == 0 else "b")
            port_alias_to_name_map[alias] = "Ethernet%d" % i
        for i in s100G_ports:
            alias = "etp%d" % (i / 4 + 1)
            port_alias_to_name_map[alias] = "Ethernet%d" % i
    elif hwsku == "Mellanox-SN2700-D48C8":
        # 50G ports
        s50G_ports = [x for x in range(0, 24, 2)] + [x for x in range(40, 88, 2)] + [x for x in range(104, 128, 2)]

        # 100G ports
        s100G_ports = [x for x in range(24, 40, 4)] + [x for x in range(88, 104, 4)]

        for i in s50G_ports:
            alias = "etp%d" % (i / 4 + 1) + ("a" if i % 4 == 0 else "b")
            port_alias_to_name_map[alias] = "Ethernet%d" % i
        for i in s100G_ports:
            alias = "etp%d" % (i / 4 + 1)
            port_alias_to_name_map[alias] = "Ethernet%d" % i
    elif hwsku == "Mellanox-SN3800-D112C8":
        x_ports = [x for x in range(0, 95, 2)]
        for i in x_ports:
            alias = "etp%d" % (i / 4 + 1) + ("a" if i % 4 == 0 else "b")
            # print alias, "Ethernet%d" % i
            port_alias_to_name_map[alias] = "Ethernet%d" % i
        x_ports = [x for x in range(96, 101, 4)] + [x for x in range(104, 111, 2)] + [x for x in range(112, 117, 4)] + [x for x in range(120, 127, 2)] + [x for x in range(128, 133, 4)] + [x for x in range(136, 143, 2)] + [x for x in range(144, 149, 4)] + [x for x in range(152, 159, 2)]
        i = 0
        while i < len(x_ports):
            for j in range (0, 2):
                alias = "etp%d" % (x_ports[i] / 4 + 1)
                port_alias_to_name_map[alias] = "Ethernet%d" % x_ports[i]
                # print alias, "Ethernet%d" % ports[i]
                i += 1
            for j in range (0, 2):
                alias = "etp%d" % (x_ports[i] / 4 + 1) + "a"
                port_alias_to_name_map[alias] = "Ethernet%d" % x_ports[i]
                # print alias, "Ethernet%d" % ports[i]
                i += 1
                alias = "etp%d" % (x_ports[i] / 4 + 1) + "b"
                port_alias_to_name_map[alias] = "Ethernet%d" % x_ports[i]
                # print alias, "Ethernet%d" % ports[i]
                i += 1
        x_ports = [x for x in range(160, 255, 2)]
        for i in x_ports:
            alias = "etp%d" % (i / 4 + 1) + ("a" if i % 4 == 0 else "b")
            # print alias, "Ethernet%d" % i
            port_alias_to_name_map[alias] = "Ethernet%d" % i
    elif hwsku == "Mellanox-SN2700" or hwsku == "ACS-MSN2700":
        for i in range(1, 33):
            port_alias_to_name_map["etp%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "ACS-MSN3800":
        for i in range(1, 65):
            port_alias_to_name_map["etp%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku in ["Arista-7060CX-32S-D48C8", "Arista-7050CX3-32S-D48C8"]:
        # All possible breakout 50G port numbers:
        all_ports = [ x for x in range(1, 33)]

        # 100G ports
        s100G_ports = [ x for x in range(7, 11) ]
        s100G_ports += [ x for x in range(23, 27) ]

        port_alias_to_name_map = _port_alias_to_name_map_50G(all_ports, s100G_ports)
    elif hwsku == "Arista-7260CX3-D108C8" or hwsku == "Arista-7260CX3-D108C8-AILAB" or hwsku == "Arista-7260CX3-D108C8-CSI":
        # All possible breakout 50G port numbers:
        all_ports = [ x for x in range(1, 65)]

        # 100G ports
        s100G_ports = [ x for x in range(13, 21) ]

        if hwsku == "Arista-7260CX3-D108C8-AILAB":
            s100G_ports = [ x for x in range(45, 53) ]
        elif hwsku == "Arista-7260CX3-D108C8-CSI":
            # Treat 40G port as 100G ports
            s100G_ports = [ x for x in range(45, 53) ] + [64]

        port_alias_to_name_map = _port_alias_to_name_map_50G(all_ports, s100G_ports)
    elif hwsku == "INGRASYS-S9100-C32":
        for i in range(1, 33):
            port_alias_to_name_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "INGRASYS-S9100-C32" or hwsku == "INGRASYS-S9130-32X" or hwsku == "INGRASYS-S8810-32Q":
        for i in range(1, 33):
            port_alias_to_name_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "INGRASYS-S8900-54XC":
        for i in range(1, 49):
            port_alias_to_name_map["Ethernet%d" % i] = "Ethernet%d" % (i - 1)
        for i in range(49, 55):
            port_alias_to_name_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 49) * 4 + 48)
    elif hwsku == "INGRASYS-S8900-64XC":
        for i in range(1, 49):
            port_alias_to_name_map["Ethernet%d" % i] = "Ethernet%d" % (i - 1)
        for i in range(49, 65):
            port_alias_to_name_map["Ethernet%d/1" % i] = "Ethernet%d" % ((i - 49) * 4 + 48)
    elif hwsku == "Accton-AS7712-32X":
        for i in range(1, 33):
            port_alias_to_name_map["hundredGigE%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "Celestica-DX010-C32":
        for i in range(1, 33):
            port_alias_to_name_map["etp%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "Seastone-DX010":
        for i in range(1, 33):
            port_alias_to_name_map["Eth%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "Celestica-E1031-T48S4":
        for i in range(1, 53):
            port_alias_to_name_map["etp%d" % i] = "Ethernet%d" % ((i - 1))
    elif hwsku == "et6448m" or hwsku == "Nokia-7215":
        for i in range(0, 52):
            port_alias_to_name_map["Ethernet%d" % i] = "Ethernet%d" % i
    elif hwsku == "Nokia-7215":
        for i in range(0, 52):
            port_alias_to_name_map["Ethernet%d" % i] = "Ethernet%d" % i
    elif hwsku == "newport":
        for i in range(0, 256, 8):
            port_alias_to_name_map["Ethernet%d" % i] = "Ethernet%d" % i
    elif hwsku == "multi_asic_hwksu":
        if asic_id is not None:
            asic_offset = int(asic_id) * 16
            backplane_offset = 15
            for i in range(1, 17):
                port_alias_to_name_map["Ethernet1/%d"%(asic_offset+i)] = "Ethernet%d"%((asic_offset + i -1) *4)
                port_alias_asic_map["Eth%d-ASIC%d"%(i-1, int(asic_id))] = "Ethernet%d"%((asic_offset + i -1) *4)
                port_alias_to_name_map["Eth%d-ASIC%d"%((backplane_offset+i), int(asic_id))] = "Ethernet-BP%d"%((asic_offset + i -1) *4)
                port_alias_asic_map["Eth%d-ASIC%d"%((backplane_offset+i), int(asic_id))] = "Ethernet-BP%d"%((asic_offset + i -1) *4)
        else:
            for i in range(1,65):
                port_alias_to_name_map["Ethernet1/%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku in ["Nexus-3132-GE-Q32", "Nexus-3132-GX-Q32"]:
        for i in range(1, 33):
            port_alias_to_name_map["Ethernet1/%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "Nexus-3164":
        for i in range(1, 65):
            port_alias_to_name_map["Ethernet1/%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "Celestica-DX010-C32":
        for i in range(1, 33):
            port_alias_to_name_map["etp%d" % i] = "Ethernet%d" % ((i - 1) * 4)
    elif hwsku == "Celestica-E1031-T48S4":
        for i in range(1, 53):
            port_alias_to_name_map["etp%d" % i] = "Ethernet%d" % ((i - 1))
    elif hwsku == "Arista-7260QX-64":
        for i in range(1, 67):
            port_alias_to_name_map["Et%d" % i] = "Ethernet%d" % i
    elif hwsku == "ACS-MSN4600C":
        for i in range(1, 65):
            port_alias_to_name_map["etp%d" % i] = "Ethernet%d" % ((i - 1) * 8)
    else:
        for i in range(0, 128, 4):
            port_alias_to_name_map["Ethernet%d" % i] = "Ethernet%d" % i

    return port_alias_to_name_map, port_alias_asic_map


def get_port_indices_for_asic(asic_id, port_name_list_sorted):
    front_end_port_name_list = [p for p in port_name_list_sorted if 'BP' not in p]
    back_end_port_name_list = [p for p in port_name_list_sorted if 'BP' in p]
    index_offset = 0
   # Create mapping between port alias and physical index
    port_index_map = {}
    if asic_id:
        index_offset = int(asic_id) *len(front_end_port_name_list)
    for idx, val in enumerate(front_end_port_name_list, index_offset):
        port_index_map[val] = idx
    for idx, val in enumerate(back_end_port_name_list, index_offset):
        port_index_map[val] = idx

    return port_index_map
