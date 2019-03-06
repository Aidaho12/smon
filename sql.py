#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 as sqltool
import sys
import os

db = "/opt/smon/smon.db"
	
def get_cur():
	con = sqltool.connect(db, isolation_level=None)  
	cur = con.cursor()
	return con, cur
	
def create_table():
	con, cur = get_cur()
	sql = """
	CREATE TABLE IF NOT EXISTS `service` (
	`ip`	INTEGER,
	`port` INTEGER,
	`status` INTEGER DEFAULT 1,
	`en` INTEGER DEFAULT 1,
	`desc` varchar(64),
	`response_time` varchar(64),
	`time_state` integer default 0,
	`group` varchar(64),
	`script` varchar(64)
	);
	"""
	try:
		cur.executescript(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	cur.close() 
	con.close()
	
	
def add_service(ip, port, desc, group, script):
	con, cur = get_cur()
	sql = """ insert into service(ip, port, desc, `group``) values ('%s', '%s', '%s', '%s', '%s')""" % (ip, port, desc, group, script)
	try:
		cur.executescript(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	cur.close() 
	con.close()
	
	
def del_service(ip, port):
	con, cur = get_cur()
	sql = """ delete from service where ip = '%s' and port = '%s' """ % (ip, port)
	try:
		cur.executescript(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	cur.close() 
	con.close()
	
	
def edit_service(ip, port, desc, **kwargs):
	con, cur = get_cur()
	if desc:
		sql = """ update service set desc = '%s' where ip = '%s' and port = '%s' """ % (desc, ip, port)
		try:
			cur.executescript(sql)
		except sqltool.Error as e:
			print("An error occurred:", e)
	if kwargs.get('new_port'):
		sql = """ update service set port = '%s' where ip = '%s' and port = '%s' """ % (kwargs.get('new_port'), ip, port)
		try:
			cur.executescript(sql)
		except sqltool.Error as e:
			print("An error occurred:", e)
	if kwargs.get('new_ip'):
		sql = """ update service set ip = '%s' where ip = '%s' and port = '%s' """ % (kwargs.get('new_ip'), ip, port)
		try:
			cur.executescript(sql)
		except sqltool.Error as e:
			print("An error occurred:", e)
	if kwargs.get('new_group'):
		sql = """ update service set `group` = '%s' where ip = '%s' and port = '%s' """ % (kwargs.get('new_group'), ip, port)
		try:
			cur.executescript(sql)
		except sqltool.Error as e:
			print("An error occurred:", e)
	if kwargs.get('new_script'):
		sql = """ update service set `script` = '%s' where ip = '%s' and port = '%s' """ % (kwargs.get('new_script'), ip, port)
		try:
			cur.executescript(sql)
		except sqltool.Error as e:
			print("An error occurred:", e)
	cur.close() 
	con.close()
	
	
def list():
	con, cur = get_cur()
	sql = """ select * from service order by `group` desc """
	try:
		cur.execute(sql)		
	except sqltool.Error as e:
		out_error(e)
	else:
		return cur.fetchall()
		
		
def select_en_service():
	con, cur = get_cur()
	sql = """ select ip, port from service where en = 1"""
	try:
		cur.execute(sql)		
	except sqltool.Error as e:
		out_error(e)
	else:
		return cur.fetchall()
		
		
def select_status(ip, port):
	con, cur = get_cur()
	sql = """ select status from service where ip = '%s' and port = '%s' """ % (ip, port)
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	else:
		for status in cur:
			return status[0]
			
			
def select_script(ip, port):
	con, cur = get_cur()
	sql = """ select script from service where ip = '%s' and port = '%s' """ % (ip, port)
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	else:
		for script in cur:
			return script[0]
		
		
def change_status(ip, port, status):
	con, cur = get_cur()
	sql = """ update service set status = '%s' where ip = '%s' and port = '%s' """ % (status, ip, port)
	try:
		cur.executescript(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	cur.close() 
	con.close()
	
	
def add_sec_to_state_time(ip, port, interval):
	con, cur = get_cur()
	sql = """ update service set time_state = time_state + '%s' where ip = '%s' and port = '%s' """ % (interval, ip, port)
	try:
		cur.executescript(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	cur.close() 
	con.close()
	
	
def set_to_zero_time_state(ip, port):
	con, cur = get_cur()
	sql = """ update service set time_state = 0 where ip = '%s' and port = '%s' """ % (ip, port)
	try:
		cur.executescript(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	cur.close() 
	con.close()
	
	
def enable_service(ip, port):
	con, cur = get_cur()
	sql = """ update service set en = 1 where ip = '%s' and port = '%s' """ % (ip, port)
	try:
		cur.executescript(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	cur.close() 
	con.close()
	
	
def disable_service(ip, port):
	con, cur = get_cur()
	sql = """ update service set en = 0 where ip = '%s' and port = '%s' """ % (ip, port)
	try:
		cur.executescript(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	cur.close() 
	con.close()
		
	
def check_exists(ip, port):
	con, cur = get_cur()
	sql = """ select ip,port from service where ip = '%s' and port = '%s' """ % (ip, port)
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	else:
		for service in cur:
			if len(service[0]) > 0:
				return False
			else:
				return True
		else:
			return True
			
			
def response_time(ip, port, time):
	con, cur = get_cur()
	sql = """ update service set response_time = '%s' where ip = '%s' and port = '%s' """ % (time, ip, port)
	try:
		cur.executescript(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	cur.close() 
	con.close()
	
	
if __name__ == "__main__":	
	create_table()