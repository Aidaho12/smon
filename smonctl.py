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
	import texttable as tt
	services = sql.list()
	tab = tt.Texttable()
	tab.set_cols_width([14,5,20,6,8,20,20,17,19])
	tab.set_cols_align(['c','c','c','c','c','c','c','c','c'])
	headings = ['IP', 'Port', 'HTTP', 'Status', 'Monitoring is','Body','Script','Group','Description']
	tab.header(headings)
	ip_row = []
	port_row = []
	http_row = []
	status_row = []
	en_row = []
	body_row = []
	script_row = []
	group_row = []
	description_row = []
	

	print('\nNow there are the following services:\n')
	for s in services:
		status = 'UP' if s[2] == 1 else 'Down'	
		en = 'Enabled' if s[3] == 1 else 'Disabled'	
		desc = '' if s[4] == 'None' else s[4]
		group = '' if s[7] == 'None' else s[7]
		script = '' if s[8] == 'None' else s[8]
		http = '' if s[9] == 'None' else s[9]
		body = '' if s[11] == 'None' else s[11]
		ip_row.append(str(s[0]))
		port_row.append(str(s[1]))
		http_row.append(http)
		status_row.append(status)
		en_row.append(en)
		body_row.append(body)
		script_row.append(script)
		group_row.append(group)
		description_row.append(desc)

	for row in zip(ip_row,port_row,http_row,status_row,en_row,body_row,script_row,group_row,description_row):
		tab.add_row(row)

	print(tab.draw())	
	
def status_service(args):
	print('Here will be status')
	
	
def check_ip(ip):
	import ipaddress
	ipaddress.ip_address(ip)
	
	
def add_service(args):	
	check_ip(args.ip)
	if sql.check_exists(args.ip, args.port):
		sql.add_service(args.ip, args.port, args.desc, args.group, args.script, args.http, args.body)
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
		sql.edit_service(args.ip, args.port, args.desc, new_ip=args.new_ip, new_port=args.new_port, new_group=args.new_group, new_script=args.new_script, new_http=args.new_http, new_body=args.new_body)
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
	add_parser.add_argument('--http', action='store', help='Set URL for HTTP check. If will be answer not 200, will be error. Example usgae: --http \'https:test.html\' or --http \'http:test.html\'')
	add_parser.add_argument('--body', action='store', help='A phrase or word that have to consist in http answer, or will be raise error')
	add_parser.add_argument('--script', action='store', help='Run the script in case of a missing service. Specify full path to executive file')
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
	edit_parser.add_argument('--new_script', action='store', help='New script')
	edit_parser.add_argument('--new_http', action='store', help='New HTTP. Format: \'http:test.html\' or \'https:test.html\'')
	edit_parser.add_argument('--new_body', action='store', help='A new phrase or word that have to consist in http answer, or will be raise error')
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