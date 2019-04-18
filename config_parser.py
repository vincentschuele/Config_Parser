import os
import re
import json
import csv
from ciscoconfparse import CiscoConfParse
from ciscoconfparse.ccp_util import IPv4Obj
import openpyxl
import ipaddress
import xlsxwriter

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
new = []

def prefix_conversion(ip):
     '''This function splits the ip and mask info passed into it
     and returns the CIDR representation as an IPv4Network object'''
     try:
          ip, mask = ip.split()
          mask = mask.replace('\\','')
     except:
          ip = None
          mask = None
     if ip and mask: 
          prefix = ipaddress.ip_network('{}/{}'.format(ip,mask), strict=False)
     else: 
          prefix = 'Not Assigned'
     return prefix


for files in os.listdir(directory):
        if files.endswith('.rtf'):
                #load config into parser
                parse = CiscoConfParse(files)
                hostname = str(parse.find_lines(r'^hostname'))
                myhost = hostname.split()[-1].split('\\')[0]
                for intf in parse.find_objects(r'^interface'):
                        interface = str(intf.text)
                        clean_interface = interface.split()[-1].replace('\\','')
                        interfaces.append(clean_interface)
                        description = intf.re_search_children(r"^\s+description")#returns list of objects, cannot index[0]
                        
                        for i in description:#loop through objects
                            #print(i)
                            desc = i.re_sub(r'<IOSCfgLine\s\#\s\d+\s+\'\s',r'') #remove junk before description TEST
                            desc = desc[1:].replace('\\','')#remove space
                            
                        ip_info = str(intf.re_match_iter_typed(IPv4_REGEX))
#                        print(ip_info)
                        interface_info[clean_interface]=(str(desc),str(prefix_conversion(ip_info)))
                        #print(str(intf.text))
                        new = str()
			#ip_address = intf.re_match_iter_typed(IPv4_REGEX)
                        #print(ip_address)
                        #description = intf.re_search_children(r"^\s+description")
                        #print(description)
                general_info[str(myhost)]=interface_info
                interface_info = {}
#                version = parse.find_objects(r'^version')
#                print(version)
#print(interfaces)
#print(interface_info)
#print(general_info)

with open('device_info.json', 'w') as handle:
     json.dump(general_info, handle, indent=4)

workbook = xlsxwriter.Workbook('Test_Output.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
worksheet.write(row, col, 'Hostname')
worksheet.write(row, col + 1, 'interface')
worksheet.write(row, col + 2, 'description')
worksheet.write(row, col + 3, 'prefix')
row += 1

with open(outputs, 'w') as f:
  
    for host in sorted( general_info):
      # cleanup hostname
      #     myhost = host.split()[-1].split('\\')[0]
      # check for empty hostname
#           if myhost:
          for interface, ip in general_info[host].items():
              desc = []
#                   clean_interface = interface.split()[-1].replace('\\','')
              desc = ip[0]
              if len(desc)==0:
                  desc = "No Description"
              prefix = ip[1]
              f.write("ROUTER {}: {} : {} : address {}\n".format(host, interface, desc, prefix))
          
              worksheet.write(row, col, host)
              worksheet.write(row, col + 1, clean_interface)
              worksheet.write(row, col + 2, desc)
              worksheet.write(row, col + 3, str(prefix))
              row += 1
workbook.close()                   
f.close()
