#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import argparse
import sql

#Logging
import logging
logger = logging.getLogger("SMON")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("/opt/smon/smon.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def list_service(args):	
	services = sql.list()

	print('\nNow there are the following services:\n')
	print('{:-^130s}'.format('-'))
	print('{1: <6}{0: <11}{2: <15}{3: <14}{4: <20}{5: <26}{6: <11}'.format('IP', '', 'Port', 'Status', 'Monitoring is','Group','Description'))
	print('{:-^130s}'.format('-'))
	for s in services:
		status = 'UP' if s[2] == 1 else 'Down'	
		en = 'Enabled' if s[3] == 1 else 'Disabled'	
		desc = '' if s[4] == 'None' else s[4]
		group = '' if s[7] == 'None' else s[7]
		print('%-16s %-15s %-14s %-17s %-25s %s ' % (str(s[0]), str(s[1]), status, en, group, desc))
		print('{:-^130s}'.format('-'))
		
	
def status_service(args):
	print('Here will be status')
	
	
def check_ip(ip):
	import ipaddress
	ipaddress.ip_address(ip)
	
	
def add_service(args):	
	check_ip(args.ip)
	if sql.check_exists(args.ip, args.port):
		sql.add_service(args.ip, args.port, args.desc, args.group)
		logger.info('Add new service with IP and port: %s %s' % (args.ip, args.port))
		print('New service waas added: ', args.ip)
	else:
		print('Service with IP and port: %s %s allready exists' % (args.ip, args.port))
	
	
def del_service(args):		
	check_ip(args.ip)
	if not sql.check_exists(args.ip, args.port):
		sql.del_service(args.ip, args.port)
		logger.info('Deleted service with IP and port: %s %s' % (args.ip, args.port))
		print('Service was deleted ', args.ip)
	else:
		print('Service with IP and port: %s %s does not exists' % (args.ip, args.port))

		
def edit_service(args):		
	check_ip(args.ip)
	if not sql.check_exists(args.ip, args.port):
		sql.edit_service(args.ip, args.port, args.desc, new_ip=args.new_ip, new_port=args.new_port, new_group=args.new_group)
		logger.info('Was edited service with IP and port: %s %s' % (args.ip, args.port))
		print('Service was edited ', args.ip)
	else:
		print('Service with IP and port: %s %s does not exists' % (args.ip, args.port))
		

def enable_service(args):
	check_ip(args.ip)
	if not sql.check_exists(args.ip, args.port):
		sql.enable_service(args.ip, args.port)
		logger.info('Service with IP and port: %s %s was enabled' % (args.ip, args.port))
		print('Service was enabled ', args.ip)
	else:
		print('Service with IP and port: %s %s does not exists' % (args.ip, args.port))
		
		
def disable_service(args):
	check_ip(args.ip)
	if not sql.check_exists(args.ip, args.port):
		sql.disable_service(args.ip, args.port)
		logger.info('Service with IP and port: %s %s was disabled' % (args.ip, args.port))
		print('Service was disabled ', args.ip)
	else:
		print('Service with IP and port: %s %s does not exists' % (args.ip, args.port))
	
	
def parse_args():
	parser = argparse.ArgumentParser(description='Simple service for monitoring TCP ports')
	subparsers = parser.add_subparsers()
	
	list_parser = subparsers.add_parser('list', help='List of services')
	list_parser.set_defaults(func=list_service)
	
	#status_parser = subparsers.add_parser('status', help='Status all active services')
	#status_parser.set_defaults(func=status_service)
	
	add_parser = subparsers.add_parser('add', help='Add new service to monitoring')
	add_parser.add_argument('ip', action='store', help='IP address')
	add_parser.add_argument('port', action='store', help='Port')
	add_parser.add_argument('--group', action='store', help='Grouping services')
	add_parser.add_argument('--desc', action='store', help='Description')
	add_parser.set_defaults(func=add_service)
	
	del_parser = subparsers.add_parser('del', help='Delete service from monitoring')
	del_parser.add_argument('ip', action='store', help='IP address')
	del_parser.add_argument('port', action='store', help='Port')
	del_parser.set_defaults(func=del_service)
	
	
	edit_parser = subparsers.add_parser('edit', help='Edit service description')
	edit_parser.add_argument('ip', action='store', help='IP address')
	edit_parser.add_argument('port', action='store', help='Port')
	edit_parser.add_argument('--new_ip', action='store', help='New IP address')
	edit_parser.add_argument('--new_port', action='store', help='New port')
	edit_parser.add_argument('--new_group', action='store', help='Edit group of services')
	edit_parser.add_argument('--desc', action='store', help='Description')
	edit_parser.set_defaults(func=edit_service)
	
	enable_parser = subparsers.add_parser('enable', help='Enable service monitoring')
	enable_parser.add_argument('ip', action='store', help='IP address')
	enable_parser.add_argument('port', action='store', help='Port')
	enable_parser.set_defaults(func=enable_service)
	
	disable_parser = subparsers.add_parser('disable', help='Disable service monitoring')
	disable_parser.add_argument('ip', action='store', help='IP address')
	disable_parser.add_argument('port', action='store', help='Port')
	disable_parser.set_defaults(func=disable_service)
		
	return parser.parse_args()
	
	
if __name__ == "__main__":	
	args = parse_args()
	try:
		args.func(args)
	except Exception as e:
		print('\nUsage: -h for help\n')
		print(e)