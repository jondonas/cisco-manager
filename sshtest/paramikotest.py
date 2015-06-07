import paramiko
import logging
import argparse
logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("ip", help = "IP address of remote device")
parser.add_argument("username", help = "Login username")
parser.add_argument("password", help = "Login password")
args = parser.parse_args()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
ssh.connect(args.ip, username=args.username, password=args.password)
stdin, stdout, stderr = ssh.exec_command('en')
type(stdin)
stdout.readlines()
stdin, stdout, stderr = ssh.exec_command('sh ver')
type(stdin)
stdout.readlines()
