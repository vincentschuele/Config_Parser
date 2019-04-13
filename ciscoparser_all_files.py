import os
import re
from ciscoconfparse import CiscoConfParse
from ciscoconfparse.ccp_util import IPv4Obj

#update to appropriate directory

dir = '/Users/vince/Desktop/Lab'

#f = open(file, 'r')
#file_contents = f.read()
#print(file_contents)


#regex for IPv4Obj

IPv4_REGEX = r"ip\saddress\s(\S+\s+\S+)"

for file in os.listdir(dir):
        if file.endswith('.rtf'):
                #load config into parser
                parse = CiscoConfParse(file)
                for intf in parse.find_objects(r'^interface'):
                        print(str(intf.text))
                        ip_address = intf.re_match_iter_typed(IPv4_REGEX)
                        print(ip_address)
                        description = intf.re_search_children(r"^\s+description")
                        print(description)

                version = parse.find_objects(r'^version')
                print(version)

