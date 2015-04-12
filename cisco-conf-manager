import Exscript
import os.path
import sys

from Exscript.util.interact import read_login
from Exscript.protocols import SSH2
from ciscoconfparse import CiscoConfParse

#Prompts for info
host_ip = raw_input("Remote Host IP: ")
account = read_login()   

#Logs in, pulls config, saves to file
conn = SSH2()                       
conn.connect(host_ip)     
conn.login(account)    
conn.execute("term len 0")            
conn.execute("sh run")
save_path = "/media/jonathan/DATA/Documents/CiscoConfParse/"
save_name = "conftest.txt"
complete_name = os.path.join(save_path, save_name)
target = open(complete_name, "w+")
target.write(conn.response)
target.close()

parse = CiscoConfParse(complete_name, factory=True)

#Execute commands
def run():
	print
	print "Available functions:"
	print "        List Int = 1    List CDP = 2    List VLANs = 3    Exit = X"
	print "        Change VLANs = 4"
	run_function = raw_input("Run Function #: ")    
	if run_function == "1":
		list_ints()
		run()
	elif run_function == "2":
		list_cdp()
		run()
	elif run_function == "3":
		list_vlans()
		run()
	elif run_function == "4":
		change_vlans()
		run()
	elif run_function == "X" or run_function == "x":
		print
		print "Have a great day!"
		sys.exit()
	else:
		print
		print "!!!Invalid Input!!!"
		run()  

#Lists interfaces on device
def list_ints():
	ints = parse.find_objects(r"^inter")
	print
	print "    Interfaces"
	for x in ints:
    		print "*" + x.text

#Lists CDP enabled interfaces
def list_cdp():
	if not bool(parse.find_objects(r"no cdp run")):
		cdp_ints = parse.find_objects_wo_child(r"^interface", r"no cdp enable")
		print
		for x in cdp_ints:
			print "*" + x.text
	else:
		print
		cdp_intfs = "*CDP disabled globally"
		print cdp_intfs

#Lists interface VLAN
def list_vlans():
	start_list = []
	ints = parse.find_objects(r"^inter")
	for i in ints:
		start_list.append(i.access_vlan)
	vlan = sorted(list(set(start_list)))
	for x in vlan:
		print
		if x == 0:
			print "    Default"
		else:
			print "    VLAN " + str(x)
		for y in ints:
			if y.access_vlan == x:
				print "*" + y.text

#Changes all vlans to default
def change_vlans():
	conf_change = []
	int_change = []
	ints = parse.find_objects(r"^inter")
	for i in ints:
		if i.access_vlan != 0:
			int_change.append(i.text)
			conf_change.append(i.text)
			conf_change.append("no switchport access vlan " + str(i.access_vlan))
	if not conf_change:
		print
		print "*There are no changes to be made"
		return
	else:
		conf_change.insert(0, "conf t")
		conf_change.append("exit")
		conf_change.append("exit")
		for x in int_change:
			print "*" + x + " will be changed" 
		choice = raw_input("Should config be saved? (y/n)")
		if choice == "Y" or choice == "y":
			conf_change.append("wr")
		for x in conf_change:
			conn.execute(x)		


run()
