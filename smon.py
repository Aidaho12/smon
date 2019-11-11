#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import socket
import argparse
import sql
import subprocess
import requests
from contextlib import closing

#Logging

import logging
logger = logging.getLogger("SMON")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("smon.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_config_var(sec, var):
	from configparser import ConfigParser, ExtendedInterpolation
	try:
		path_config = "/opt/smon/smon.cfg"
		config = ConfigParser(interpolation=ExtendedInterpolation())
		config.read(path_config)
	except:
		logger.fatal('Check the config file, whether it exists and the path. Must be: /opt/smon/smon.cfg')
	try:
		return config.get(sec, var)
	except:
		logger.fatal('Check the config file. Presence section %s and parameter %s' % (sec, var))


def telegram_send_mess(mess, **kwargs):
	import telebot
	from telebot import apihelper
	
	token_bot = get_config_var('telegram', 'token')
	channel_name = get_config_var('telegram', 'channel_name')
	proxy = get_config_var('main', 'proxy')
	mess = 'SMON: '+mess
	
	if proxy != 'None':
		apihelper.proxy = {'https': proxy}
	
	try:
		bot = telebot.TeleBot(token=token_bot)
		bot.send_message(chat_id=channel_name, text=mess)
	except Exception as e:
		logger.error("Can't send message. Add Telegram channel before use alerting")
		logger.error(e)
		pass
		

def send_and_loggin(mes):
	logger.warning(mes)
	telegram_send_mess(mes)
	

def check_socket(ip, port, first_run):
	with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
		status = sql.select_status(ip, port)
		start = time.time()
		interval = get_config_var('main', 'interval')
		interval = int(interval)
		
		if sock.connect_ex((ip, port)) == 0:
			end = (time.time()-start)*1000 

			sql.response_time(ip, port, end)
			sql.add_sec_to_state_time(ip, port, interval)
			if status == 0:
				sql.change_status(ip, port, 1)
				if not first_run:
					sql.set_to_zero_time_state(ip, port)
					mes = 'Now port: '+str(port)+' on host '+str(ip)+' is UP'
					send_and_loggin(mes)
			return True
			
		else:
			sql.add_sec_to_state_time(ip, port, interval)
			if status == 1:
				sql.change_status(ip, port, 0)
				if not first_run:
					sql.set_to_zero_time_state(ip, port)
					mes = 'Now port: '+str(port)+' on host '+str(ip)+' is DOWN'
					send_and_loggin(mes)
					try:
						script = sql.select_script(ip, port)
						subprocess.check_call(script, shell=True)
					except subprocess.CalledProcessError as e:
						logger.warning('Can not run the script for: '+str(port)+' on host '+str(ip)+', error: '+e)
			return False
			
			
def check_port_status(ip, port, first_run, http):
	status = sql.select_http_status(ip, port)
	try:
		http_uri = http.split(":")[1]
		http_method = http.split(":")[0]
	except:
		http_method = 'http'
		try:
			http_uri = http
		except:
			http_uri = '/'
	try:
		response = requests.get('%s://%s:%s/%s' % (http_method, ip, port, http_uri))
		response.raise_for_status()
		
		if status == 0:
			sql.change_http_status(ip, port, 1)
			mes = 'Now HTTP port: '+str(port)+' on host '+str(ip)+' is UP'
			send_and_loggin(mes)
			
		body_answer = sql.select_body(ip, port)
		if body_answer is not None:
			status = sql.select_body_status(ip, port)
			
			if body_answer not in response.content.decode(encoding='UTF-8'):
				if status == 1:
					sql.change_body_status(ip, port, 0)
					
					i = 0
					body = ''
					for l in response.content.decode(encoding='UTF-8'):
						body += l
						i += 1
						if i >145:
							break

					if not first_run:
						mes = 'Found out '+str(port)+' on host '+str(ip)+' is failure: ' + body
						send_and_loggin(mes)			
			else:
				if status == 0:
					sql.change_body_status(ip, port, 1)
					if not first_run:
						mes = 'Now answer from '+str(port)+' on host '+str(ip)+' is well'
						send_and_loggin(mes)
			
	except requests.exceptions.HTTPError as err:
		if status == 1:
			sql.change_http_status(ip, port, 0)
			mes = 'Response is: {content} from {ip} port {port}'.format(content=err.response.status_code, ip=ip, port=port)
			send_and_loggin(mes)
	except requests.exceptions.ConnectTimeout:
		if status == 1:
			sql.change_http_status(ip, port, 0)
			mes = 'HTTP connection timeout to {0} port {1}'.format(ip, port)
			send_and_loggin(mes)
	
			
if __name__ == "__main__":	
	first_run = True
	while True:
		services = sql.select_en_service()
		for s in services:
			ip = s[0]
			port = s[1]
			if check_socket(ip, port, first_run):
				http = sql.select_http(ip, port)
				if http is not None:
					check_port_status(ip, port, first_run, http)
			
		first_run = False
		
		interval = get_config_var('main', 'interval')
		interval = int(interval)
		time.sleep(interval)