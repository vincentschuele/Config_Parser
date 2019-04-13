import os
import re
import json
from ciscoconfparse import CiscoConfParse
from ciscoconfparse.ccp_util import IPv4Obj

#update to appropriate directory

directory = '/Users/vince/Desktop/Lab'

#f = open(file, 'r')
#file_contents = f.read()
#print(file_contents)


#regex for IPv4Obj

IPv4_REGEX = r"ip\saddress\s(\S+\s+\S+)"

outputs = 'output.txt'

interface_info = {}
interface_name = str()
desc = str()
ipv4_add = str()
interfaces = []
general_info = {}

for file in os.listdir(directory):
        if file.endswith('.rtf'):
                #load config into parser
                parse = CiscoConfParse(file)
                hostname = parse.find_lines(r'^hostname')
                for intf in parse.find_objects(r'^interface'):
                        interfaces.append(str(intf.text))
                        interface_info[str(intf.text)]=(str(intf.re_search_children(r"^\s+description")),str(intf.re_match_iter_typed(IPv4_REGEX)))
                        #print(str(intf.text))
			#ip_address = intf.re_match_iter_typed(IPv4_REGEX)
                        #print(ip_address)
                        #description = intf.re_search_children(r"^\s+description")
                        #print(description)
                general_info[str(hostname)]=interface_info
                interface_info = {}
#                version = parse.find_objects(r'^version')
#                print(version)
#print(interfaces)
#print(interface_info)
#print(general_info)

with open('device_info.json', 'w') as handle:
     json.dump(general_info, handle, indent=4)

