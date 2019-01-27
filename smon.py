#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import socket
import argparse
import sql
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
					logger.warning('Now port: '+str(port)+' on host '+str(ip)+' is UP')
					telegram_send_mess('Now port: '+str(port)+' on host '+str(ip)+' is UP')
		else:
			sql.add_sec_to_state_time(ip, port, interval)
			if status == 1:
				sql.change_status(ip, port, 0)
				if not first_run:
					sql.set_to_zero_time_state(ip, port)
					logger.warning('Now port: '+str(port)+' on host '+str(ip)+' is DOWN')
					telegram_send_mess('Now port: '+str(port)+' on host '+str(ip)+' is DOWN')
			
			
if __name__ == "__main__":	
	first_run = True
	while True:
		services = sql.select_en_service()
		for s in services:
			ip = s[0]
			port = s[1]
			check_socket(ip, port, first_run)
			
		first_run = False
		
		interval = get_config_var('main', 'interval')
		interval = int(interval)
		time.sleep(interval)