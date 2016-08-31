#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import json
import time
import smtplib
import requests
import datetime
import mimetypes
import MySQLdb
import urllib
import functions as func
from tib import global_vars as vars
import Queue
import threading
from collections import OrderedDict
import matplotlib.pyplot as plt

#for draw pic
import numpy as np
import matplotlib.pyplot as plt

from pyh import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

#from sendmail_config import *


####
thread_num = 9
ExitFlag = 0
time_log_file = '/price_warning_script_running_cost_time.log'
N1 = 5
N2 = 7
the_boss_need_days = 30
bigger_rate = 1.8
flight_time = (9,13)


##
#cities = ["昆明","杭州","苏州","厦门","南京","西安","珠海","惠州"]
cities = ["北京","上海","广州","深圳"]
house_price_get_url = '''http://fangjia.fang.com/pinggu/ajax/chartajax.aspx?dataType=4&city=%s&Class=defaultnew&year=2'''
##

request_json_and_flight_url_last = None
###
def log_debug(str_tmp):
	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	f = open("/tib.log","a+")
	f.write("[%s]%s\n" %(now,str_tmp))
	f.close()

def from_chinese_to_utf8_str(name):
	#print repr(str(name).strip().decode('utf-8')).replace(r'\u',r'%u')[2:-1]
	return repr(str(name).strip().decode('utf-8')).replace(r'\u',r'%u')[2:-1]

def get_data_from_url(url):
	l1 = []
	l2 = []
	data = requests.get(url).content
	if len(data.split('&')) == 4:
		data_1 = data.split('&')[0].split('],[')
		data_2 = data.split('&')[1].split('],[')
		#print data_1
		#print data_2
		for i in range(24):
			if i == 0:
				l1.append(data_1[i][2:].split(',')[1])
			elif i == 23:
				l1.append(data_1[i][:-2].split(',')[1])
			else:
				l1.append(data_1[i].split(',')[1])
		for i in range(24):
			if i == 0:
				l2.append(data_2[i][2:].split(',')[1])
			elif i == 23:
				l2.append(data_2[i][:-2].split(',')[1])
			else:
				l2.append(data_2[i].split(',')[1])
		#print l1
		#print l2
		return (l1,l2)
	elif len(data.split('&')) == 2:
		print 2
		return ("","")
	else:
		print "Fuck"

def get_to_city_name(json_string):
	t_1 = json.loads(json_string)
	#return t_1['ToStr']
	return t_1['ToStr'].encode("UTF-8")

def get_from_city_name(json_string):
	t_1 = json.loads(json_string)
	#return t_1['FromStr']
	return t_1['FromStr'].encode("UTF-8")

def print_json(json_obj,indent_=4):
	print "-" * 50
	print json.dumps(json_obj,indent=indent_,ensure_ascii=False,sort_keys=True)
	print "-" * 60


def get_all_request_json_string(days):
	all_go_and_back_days = []
	only_date = []
	for i in range(days):
		a = vars.TODAY + vars.ONEDAY * i
		j = a + vars.ONEDAY * N1
		k = a + vars.ONEDAY * N2
		all_go_and_back_days.append((j.strftime("%d/%m/%Y"),k.strftime("%d/%m/%Y")))
	return all_go_and_back_days

def get_all_request_json_data(one_flight_direction,flight_url):
	global request_json_and_flight_url_last
	request_json_list = []
	for i in get_all_request_json_string(the_boss_need_days):
		data = one_flight_direction.replace("go_date",i[0]).replace("back_date",i[1])
		flight_url_last = flight_url % (i[0],i[1])
		request_json_result = request_json % urllib.quote_plus(data)
		request_json_list.append((request_json_result,flight_url_last,i))
	request_json_and_flight_url_last = request_json_result
	return request_json_list

def get_json_data_of_flight(flight,flight_url,need_check_airline_code):
	json_data_list = []
	header = {'Content-Type': 'application/x-www-form-urlencoded','User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
	flight_api_url = """http://flights.wingontravel.com/Api/AjaxGetFlightList"""
	for i in get_all_request_json_data(flight,flight_url):
		r = requests.post(flight_api_url,headers=header,data=i[0])
		json_data_list.append((r.content,i[1],i[2]))
	return (json_data_list,need_check_airline_code)

def get_lowest_price_with_tax_of_this_airline_code(airlinecode,all_json_data):
	tax_price = []
	fuel_price = []
	for every_flight in all_json_data['flightList']:
		if str(every_flight['airlineCode']).lower() == str(airlinecode).lower():
			tax_price.append(int(every_flight['seats'][0]['adultTax']))
			fuel_price.append(int(every_flight['seats'][0]['adultFuel']))
			tax_price.sort()
			fuel_price.sort()
	return (airlinecode,tax_price[0],fuel_price[0])

def sendmail_for_no_flight_warning(email_content):
	#mail_to = ['xh_liu@ctrip.com']
	mail_to = ['']
	email_host = ''
	email_user = ''
	email_pass = ''
	mail_from = ''
	msg = MIMEMultipart()
	msg['From'] = ""
	msg['To'] = ';'.join(mail_to)
	msg['Subject'] = ""
	html = MIMEText(email_content,'html','utf-8')
	msg.attach(html)
	try:
		smtp = smtplib.SMTP()
		smtp.connect(email_host)
		smtp.login(email_user, email_pass)
		smtp.sendmail(mail_from, mail_to, msg.as_string())
		smtp.quit()
		print 'Send email successful.'
		log_debug('Send email successful.')
		return True
	except Exception,e:
		print str(e)
		log_debug('Send email error:'+str(e))
		return False

def sendmail_for_price_warning(email_content):
	#mail_to = ['xh_liu@ctrip.com']
	mail_to = ['']
	email_host = ''
	email_user = ''
	email_pass = ''
	mail_from = ''
	msg = MIMEMultipart()
	msg['From'] = ""
	msg['To'] = ';'.join(mail_to)
	msg['Subject'] = ""
	html = MIMEText(email_content,'html','utf-8')
	msg.attach(html)
	try:
		smtp = smtplib.SMTP()
		smtp.connect(email_host)
		smtp.login(email_user, email_pass)
		smtp.sendmail(mail_from, mail_to, msg.as_string())
		smtp.quit()
		print 'Send email successful.'
		log_debug('Send email successful.')
		return True
	except Exception,e:
		print str(e)
		log_debug('Send email error:'+str(e))
		return False

def get_one_piece_from_queue(queue,lock_name):
	one_piece = queue.get()
	return one_piece


class my_worker(threading.Thread):

	def __init__(self,queue,response_dic,id,lock):
		threading.Thread.__init__(self)
		self.queue = queue
		self.response_dic = response_dic
		self.id = id
		self.lock = lock

	def run(self):
		print "Thread [%s] Started" % self.id
		while True:
			one_query = get_one_piece_from_queue(self.queue,self.lock)
			res = get_json_data_of_flight(one_query[0],one_query[1],one_query[2])
			no_flight = check_if_has_flight(res)
			price_warning = check_price_warning(res)
			flight_airline_name = "%s_%s" % (get_from_city_name(one_query[0]),get_to_city_name(one_query[0]))
			self.lock.acquire()
			self.response_dic["%s" % flight_airline_name] = {"no_flight":{},"price_warning":{}}
			self.response_dic["%s" % flight_airline_name]['no_flight'] = no_flight
			self.response_dic["%s" % flight_airline_name]['price_warning'] = price_warning
			self.lock.release()
			self.queue.task_done()
		print "Thread [%s] Ended" % self.id

class my_worker_2(threading.Thread):

	def __init__(self,queue,response_dic,id,lock):
		threading.Thread.__init__(self)
		self.queue = queue
		self.response_dic = response_dic
		self.id = id
		self.lock = lock

	def run(self):
		print "Thread [%s] Started" % self.id
		while True:
			one_query = get_one_piece_from_queue(self.queue,self.lock)
			res = get_data_from_url(one_query[0],one_query[1],one_query[2])
			no_flight = check_if_has_flight(res)
			price_warning = check_price_warning(res)
			flight_airline_name = "%s_%s" % (get_from_city_name(one_query[0]),get_to_city_name(one_query[0]))
			self.lock.acquire()
			self.response_dic["%s" % flight_airline_name] = {"no_flight":{},"price_warning":{}}
			self.response_dic["%s" % flight_airline_name]['no_flight'] = no_flight
			self.response_dic["%s" % flight_airline_name]['price_warning'] = price_warning
			self.lock.release()
			self.queue.task_done()
		print "Thread [%s] Ended" % self.id

if __name__ == '__main__':
	check_ = []
	od = OrderedDict()
	for i in cities:
		#plt.axis([0, 24, 5000, 100000])
		#x_pos = [f for f in range(1,25)]
		print from_chinese_to_utf8_str(i)
		#time.sleep(1)
		a = house_price_get_url % ("%s" % from_chinese_to_utf8_str(i))
		bb = get_data_from_url(a)
		if bb == ("",""):
			print "Fuck Oh No."
			sys.exit()
		#print bb
		#print len(bb[0]),len(bb[1])
		#plt.plot(bb[0],'b-',bb[1],'r--')
		#plt.plot(x_pos,bb[0],'b-',x_pos,bb[1],'r--')
		#plt.savefig('11.png',bbox_inches='tight')
		#time.sleep(1)
		#plt = None
		#check_.append(bb)
		od[i] = {}
		od[i]['second'] = []
		od[i]['new'] = []
		for fk in bb[0]:
			od[i]['second'].append(fk)
		for fr in bb[1]:
			od[i]['new'].append(fr)

	fb = json.dumps(od,indent=4,ensure_ascii=False)
	print fb
	open("/tmp/4_first_cities.txt","w").write(fb)
	#deal_with_flight_data()
	#sys.exit()
	#print from_chinese_to_utf8_str("你好")
