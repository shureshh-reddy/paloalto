

r_config = {
    "header": [
        "! device: hq-it-lab-core-sw01 (DCS-7280SR-48C6-M, EOS-4.20.12M)\n!\n"
    ],
    "comments": [],
    "cmds": {
        "interface Ethernet37": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet36": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet35": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet34": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet33": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet32": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet31": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet30": {
            "comments": [],
            "cmds": {}
        },
        "transceiver qsfp default-mode 4x10G": "null",
        "interface Ethernet49/1": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet39": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet38": {
            "comments": [],
            "cmds": {}
        },
        "interface Port-Channel3": {
            "comments": [],
            "cmds": {
                "description MLAG to aruba-wlc01": "null",
                "switchport mode trunk": "null",
                "mlag 3": "null"
            }
        },
        "interface Port-Channel2": {
            "comments": [],
            "cmds": {
                "description MLAG to it-hq-lab-cfw02p": "null",
                "switchport mode trunk": "null",
                "mlag 2": "null"
            }
        },
        "interface Port-Channel1": {
            "comments": [],
            "cmds": {
                "mlag 1": "null",
                "description MLAG to it-hq-lab-cfw01p": "null",
                "switchport mode trunk": "null"
            }
        },
        "interface Port-Channel5": {
            "comments": [],
            "cmds": {
                "description MLAG to aruba-access-sw": "null",
                "switchport mode trunk": "null",
                "mlag 5": "null"
            }
        },
        "interface Port-Channel4": {
            "comments": [],
            "cmds": {
                "switchport mode trunk": "null",
                "mlag 4": "null",
                "description MLAG to aruba-wlc02": "null"
            }
        },
        "vlan 4094": {
            "comments": [],
            "cmds": {
                "trunk group mlagpeer": "null",
                "name MLAG-Keepalive": "null"
            }
        },
        "vlan 128": {
            "comments": [],
            "cmds": {
                "name wired-users": "null"
            }
        },
        "ip routing": "null",
        "snmp-server location sjc-hq-lab": "null",
        "snmp-server contact IT-Networking": "null",
        "ntp server 10.55.66.10 prefer": "null",
        "logging host 10.101.33.83 protocol tcp": "null",
        "interface Ethernet46": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet47": {
            "comments": [],
            "cmds": {}
        },
        "logging host 10.101.220.139 5525 protocol tcp": "null",
        "interface Ethernet45": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet42": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet51/1": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet40": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet41": {
            "comments": [],
            "cmds": {}
        },
        "snmp-server host 10.101.33.83 informs version 2c hq-it-lab": "null",
        "spanning-tree mode mstp": "null",
        "interface Ethernet48": {
            "comments": [],
            "cmds": {}
        },
        "interface Vlan110": {
            "comments": [],
            "cmds": {
                "ip address 10.55.10.181/23": "null"
            }
        },
        "hostname hq-it-lab-core-sw01": "null",
        "event-handler testing-lab": {
            "comments": [],
            "cmds": {
                "action bash python /mnt/flash/shutdown.py Ethernet4": "null"
            }
        },
        "ntp server 10.55.66.11": "null",
        "management api http-commands": {
            "comments": [],
            "cmds": {
                "protocol unix-socket": "null",
                "protocol http": "null",
                "no shutdown": "null"
            }
        },
        "router bgp 64496": {
            "comments": [],
            "cmds": {
                "vrf purple": {
                    "comments": [],
                    "cmds": {
                        "graceful-restart restart-time 300": "null",
                        "graceful-restart": "null"
                    }
                },
                "graceful-restart restart-time 300": "null",
                "graceful-restart": "null"
            }
        },
        "ip route 0.0.0.0/0 10.55.10.1": "null",
        "interface Ethernet19": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet18": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet50/1": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet15": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet14": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet17": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet16": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet11": {
            "comments": [],
            "cmds": {
                "switchport access vlan 110": "null",
                "description to-cg1-controller1": "null"
            }
        },
        "interface Ethernet10": {
            "comments": [],
            "cmds": {
                "description to-esxi": "null",
                "switchport access vlan 110": "null"
            }
        },
        "interface Ethernet13": {
            "comments": [],
            "cmds": {
                "switchport mode trunk": "null"
            }
        },
        "interface Ethernet12": {
            "comments": [],
            "cmds": {
                "switchport access vlan 110": "null",
                "description to-panorama-mgmt": "null"
            }
        },
        "vlan 319": {
            "comments": [],
            "cmds": {
                "name zoom": "null"
            }
        },
        "snmp-server community g3tpanstats ro": "null",
        "vlan 311": {
            "comments": [],
            "cmds": {
                "name corp-wireless01": "null"
            }
        },
        "vlan 350": {
            "comments": [],
            "cmds": {
                "name guest": "null"
            }
        },
        "interface Ethernet43": {
            "comments": [],
            "cmds": {}
        },
        "username cvpadmin privilege 15 role network-admin secret sha512 $6$Rkb3/UiKeZKSyRvn$JDElS8zhpn5kYG7slN476mq2.WfOQlZMD0Rgbq.xTytm4ebxoP3iyxyCtAZVPppkZSfPg.eF816irxQ0DHKx70": "null",
        "aaa authorization exec default local": "null",
        "interface Management1": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet1": {
            "comments": [],
            "cmds": {
                "channel-group 999 mode active": "null",
                "switchport mode trunk": "null",
                "description csw02p:eth1": "null"
            }
        },
        "interface Ethernet3": {
            "comments": [],
            "cmds": {
                "channel-group 1 mode active": "null",
                "description firewall01-eth": "null"
            }
        },
        "interface Ethernet2": {
            "comments": [],
            "cmds": {
                "channel-group 999 mode active": "null",
                "switchport mode trunk": "null",
                "description csw02p:2": "null"
            }
        },
        "interface Ethernet5": {
            "comments": [],
            "cmds": {
                "channel-group 3 mode active": "null",
                "description aruba-wlc01": "null"
            }
        },
        "interface Ethernet4": {
            "comments": [],
            "cmds": {
                "description firewall02-eth": "null",
                "channel-group 2 mode active": "null"
            }
        },
        "interface Ethernet7": {
            "comments": [],
            "cmds": {
                "channel-group 5 mode active": "null",
                "description aruba-sw": "null"
            }
        },
        "interface Ethernet6": {
            "comments": [],
            "cmds": {
                "description aruba-wlc02": "null",
                "channel-group 4 mode active": "null"
            }
        },
        "interface Ethernet9": {
            "comments": [],
            "cmds": {
                "description to-esxi": "null",
                "switchport access vlan 110": "null"
            }
        },
        "interface Ethernet8": {
            "comments": [],
            "cmds": {
                "switchport access vlan 110": "null",
                "description to-firewall01-mgmt": "null"
            }
        },
        "interface Port-Channel999": {
            "comments": [],
            "cmds": {
                "switchport mode trunk": "null",
                "description MLAG PEER LINK - DONT TOUCH": "null",
                "load-interval 5": "null",
                "switchport trunk group mlagpeer": "null"
            }
        },
        "interface Ethernet24": {
            "comments": [],
            "cmds": {}
        },
        "username admin privilege 15 role network-admin secret sha512 $6$CeRHD/SjBEbhtiSX$NMcrl4x4aKOnaOnRqbuZWeERRN6eqNMwby2P8knuSySsp/TPytN44seNL2nj.WQhk7OUsqsSkf5Cow1IkjCc00": "null",
        "interface Ethernet26": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet27": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet20": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet21": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet22": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet23": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet52/1": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet28": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet29": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet53/1": {
            "comments": [],
            "cmds": {}
        },
        "terminal length 20": "null",
        "daemon TerminAttr": {
            "comments": [],
            "cmds": {
                "no shutdown": "null",
                "exec /usr/bin/TerminAttr -ingestgrpcurl=10.58.10.21:9910 -taillogs -ingestauth=key, -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -ingestexclude=/Sysdb/cell/1/agent,/Sysdb/cell/2/agent -ingestvrf=default": "null"
            }
        },
        "vlan 111": {
            "comments": [],
            "cmds": {
                "name wired-users01": "null"
            }
        },
        "vlan 110": {
            "comments": [],
            "cmds": {
                "name corp-mgmt": "null"
            }
        },
        "interface Ethernet25": {
            "comments": [],
            "cmds": {}
        },
        "interface Ethernet54/1": {
            "comments": [],
            "cmds": {}
        },
        "mlag configuration": {
            "comments": [],
            "cmds": {
                "primary-priority 10": "null",
                "domain-id mlag-lab-csw": "null",
                "reload-delay mlag 900": "null",
                "peer-link Port-Channel999": "null",
                "local-interface Vlan4094": "null",
                "peer-address 10.255.255.2": "null"
            }
        },
        "interface Ethernet44": {
            "comments": [],
            "cmds": {}
        },
        "! boot system flash:/EOS-4.20.12M.swi": "null",
        "spanning-tree mst 0 priority 4096": "null",
        "ip domain-name paloaltonetworks.com": "null",
        "interface Vlan4094": {
            "comments": [],
            "cmds": {
                "no autostate": "null",
                "ip address 10.255.255.1/30": "null"
            }
        },
        "spanning-tree mst configuration": {
            "comments": [],
            "cmds": {
                "name sjc-hq-lab": "null",
                "revision 1": "null"
            }
        },
        "no spanning-tree vlan 4094": "null",
        "no aaa root": "null"
    }
}

#print(r_config["cmds"])
print(d_config["cmds"])
