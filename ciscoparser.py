import os
import re
from ciscoconfparse import CiscoConfParse
from ciscoconfparse.ccp_util import IPv4Obj

file = '/Users/vince/Desktop/Lab/CSR1.rtf'
#f = open(file, 'r')
#file_contents = f.read()
#print(file_contents)

#load config into parser

parse = CiscoConfParse(file)

#regex for IPv4Obj

IPv4_REGEX = r"ip\saddress\s(\S+\s+\S+)"

for intf in parse.find_objects(r'^interface'):
	print(str(intf.text))
	ip_address = intf.re_match_iter_typed(IPv4_REGEX)
	print(ip_address)
	description = intf.re_search_children(r"^ description")
	print(description)

version = parse.find_objects(r'^version')
print(version)

