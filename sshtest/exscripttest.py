import sys
import argparse
import Exscript
from Exscript.util.interact import read_login
from Exscript.protocols import SSH2
from Exscript import Account

parser = argparse.ArgumentParser()
parser.add_argument("ip", help = "IP address of remote device")
parser.add_argument("username", help = "Login username")
parser.add_argument("password", help = "Login password")
args = parser.parse_args()

conn = SSH2()
conn.connect(args.ip)
conn.login(Account(args.username, args.password))
conn.execute ("en")
conn.execute("sh ver")
print conn.response

