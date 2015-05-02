import sys
import argparse

from fabric.api import *
from ciscoconfparse import CiscoConfParse

#ArgParse
parser = argparse.ArgumentParser()
parser.add_argument("ip", help = "IP address of remote device")
parser.add_argument("function", type=int, help = "Desired function to be run")
parser.add_argument("username", help = "Login username")
parser.add_argument("password", help = "Login password")
parser.add_argument("-p", "--enpass", help = "(Optional) Enable password")
args = parser.parse_args()

#Logs in, pulls and parses config
env.user=args.username
env.host_string=args.ip
env.password=args.password
run("en", shell=False)
if args.enpass:
	run(args.enpass, shell=False)
else:
	pass

config=[]
text = run("sh run", shell=False)
parse = CiscoConfParse(text.splitlines(), factory=True)

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
		print
	else:
		print
		print "*CDP disabled globally"
		print

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
	print

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
		print
		return
	else:
		conf_change.insert(0, "conf t")
		conf_change.append("exit")
		conf_change.append("exit")
		conf_change.append("wr")
		for x in int_change:
			print "*" + x + " will be changed"
		for x in conf_change:
			run(x, shell=False)


#Execute commands
run_function = args.function
if run_function == 1:
	list_ints()
elif run_function == 2:
	list_cdp()
elif run_function == 3:
	list_vlans()
elif run_function == 4:
	change_vlans()
