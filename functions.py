#!/usr/bin/env python
# -*- coding:utf-8 -*-

#author: tib
#desc: all my functions created by myself.. :) Enjoy..

import os,time,sys,datetime
import signal
import platform
import urllib
import urllib2
import json
import socket,codecs,re
import sys
import datetime
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import socket
socket.setdefaulttimeout(15)
#reload(sys)
#sys.setdefaultencoding('utf8')

mailto_list=[""] #收件人列表
mail_host="smtp.gmail.com"  #设置服务器
mail_user=""    #用户名
mail_pass=""   #口令
mail_postfix="gmail.com"  #发件箱的后缀

def _decode_list(data):
	rv = []
	for item in data:
		if isinstance(item, unicode):
			item = item.encode('utf-8')
		elif isinstance(item, list):
			item = _decode_list(item)
		elif isinstance(item, dict):
			item = _decode_dict(item)
		rv.append(item)
	return rv

def _decode_dict(data):
	rv = {}
	for key, value in data.iteritems():
		if isinstance(key, unicode):
			key = key.encode('utf-8')
		if isinstance(value, unicode):
			value = value.encode('utf-8')
		elif isinstance(value, list):
			value = _decode_list(value)
		elif isinstance(value, dict):
			value = _decode_dict(value)
		rv[key] = value
	return rv

def json_loads_unicode_to_string(data):
	#return json.loads(data,object_hook=_decode_list)
	return json.loads(data,object_hook=_decode_dict)

def mk_dir_if_not_exist(path):
	dir_path = os.path.split(path)[0]
	if os.path.exists(dir_path) is not True:
		os.makedirs(dir_path)

def mk_dir(path):
	dir_path = path
	if os.path.exists(dir_path) is not True:
		os.makedirs(dir_path)

def t_to_l(t):
	new_list = []
	for i in t:
		new_list.append(list(i))
	for i in range(len(new_list)):
		for j in range(len(new_list[i])):
			new_list[i][j] = str(new_list[i][j])
	return new_list

def check_the_platform():
	if platform.system().lower() == "linux":
		return "linux"
	elif platform.system().lower() == "darwin":
		return "mac"
	elif platform.system().lower() == "windows":
		return "win"
	else:
		return "Unknown"

def get_monday_to_sunday():
	a = datetime.date.today()
	b = a.weekday()
	the_last = a + datetime.timedelta(6 - a.weekday())
	if b == 0:
		the_first = a
	else:
		the_first = get_the_one_date(b,"-")
	return (the_first,the_last)

def get_this_month_first_day_to_last():
	date1 = datetime.datetime.now()
	y=date1.year
	m = date1.month
	month_start_dt = datetime.date(y,m,1)
	if m == 12:
		month_end_dt = datetime.date(y+1,1,1) - datetime.timedelta(days=1)
	else:
		month_end_dt = datetime.date(y,m+1,1) - datetime.timedelta(days=1)
	return (month_start_dt,month_end_dt)

def get_this_quarter_first_day_and_last_day():
	date1 = datetime.datetime.now()
	y=date1.year
	month = date1.month
	if month in (1,2,3):
		quarter_start_dt = datetime.date(y,1,1)
		quarter_end_dt = datetime.date(y,4,1) - datetime.timedelta(days=1)
	elif month in (4,5,6):
		quarter_start_dt = datetime.date(y,4,1)
		quarter_end_dt = datetime.date(y,7,1) - datetime.timedelta(days=1)
	elif month in (7,8,9):
		quarter_start_dt = datetime.date(y,7,1)
		quarter_end_dt = datetime.date(y,10,1) - datetime.timedelta(days=1)
	else:
		quarter_start_dt = datetime.date(y,10,1)
		quarter_end_dt = datetime.date(y+1,1,1) - datetime.timedelta(days=1)
	return (quarter_start_dt,quarter_end_dt)

def get_this_quarter_total_days_and_remain_days():
	date1 = datetime.datetime.now().date()
	a = get_this_quarter_first_day_and_last_day()
	quarter_days = (a[1] - a[0]).days + 1
	quarter_rem = (a[1] - date1).days
	return (quarter_days,quarter_rem)

def get_last_month_first_day_to_last():
	date1 = datetime.datetime.now()
	y=date1.year
	m = date1.month
	if m==1:
		start_date=datetime.date(y-1,12,1)
	else:
		start_date=datetime.date(y,m-1,1)
	end_date=datetime.date(y,m,1) - datetime.timedelta(days=1)
	return (start_date,end_date)

def convert_seconds_to_time(second):
	a = "{:0>8}".format(datetime.timedelta(seconds=second))
	return a

def get_last_monday_to_sunday():
	date1 = datetime.datetime.now()
	last_week_start_dt = date1-datetime.timedelta(days=date1.weekday()+7)
	last_week_end_dt = date1-datetime.timedelta(days=date1.weekday()+1)
	return (last_week_start_dt,last_week_end_dt)

def get_the_date_of_last(days):
	TODAY = datetime.date.today()
	date_list =[]
	for i in range(days,0,-1):
		NUM_DAY = datetime.timedelta(days=i)
		date_list.append(TODAY - NUM_DAY)
	return date_list

def get_the_one_date(num,choice):
	TODAY = datetime.date.today()
	if str(choice) == '-':
		NUM_DAY = datetime.timedelta(days=(int(num)))
		the_date = TODAY - NUM_DAY
		return the_date
	elif str(choice) == '+':
		NUM_DAY = datetime.timedelta(days=(int(num)))
		the_date = TODAY + NUM_DAY
		return the_date
	else:
		print "ERROR! from functions.get_the_one_date"
		sys.exit()

def get_the_24_hour_format_for_mysql_query():
	time_list_before = []
	time_list_after = []
	for i in range(24):
		time_list_before.append("%s:00:00" % i)
		time_list_after.append("%s:59:59" % i)
	return time_list_before,time_list_after

#open the ip data file and store all in list
if os.path.exists("/tmp/all_ip_with_location.txt") is True:
	f = open("/tmp/all_ip_with_location.txt","r")
	all_ip_location_list = f.read().splitlines()
	f.close()

def check_ip_location_if_in_local_file(all_ip_info,check_ip):
	_all_ip = all_ip_info
	for i in _all_ip:
		if i.split(':')[0].strip() == check_ip.strip():
			return (10,i)
	return (8,i)

def get_match_substr_from_str(ori_string,re_compile_str):
	pattern = re.compile(r'%s' % re_compile_str)
	a = pattern.findall("%s" % ori_string)
	if len(a) != 0:
		return a
	else:
		return []


def get_ip_location(ip):
	re_ipaddress = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
	re_domain = re.compile(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?')
	if re_ipaddress.match(ip):
		url = "http://ip.taobao.com/service/getIpInfo.php?ip="
		#Use the file ip location
		#
		num_and_location = check_ip_location_if_in_local_file(all_ip_location_list,ip)
		if num_and_location[0] == 10:
			#print "File"
			return num_and_location[1].split(':')[1]
		#
		else:
			data = urllib.urlopen(url + ip).read()
			datadict=json.loads(data)
			for oneinfo in datadict:
				if "code" == oneinfo:
					if datadict[oneinfo] == 0:
						result = datadict["data"]["country"] + datadict["data"]["region"] + datadict["data"]["city"] + datadict["data"]["isp"]
						ll = "%s" % ip.strip() + ":" + result
						f = codecs.open("/tmp/all_ip_with_location.txt","a+","utf-8")
						f.write("%s\n" % ll)
						f.close()
						#print "Net"
						return datadict["data"]["country"] + datadict["data"]["region"] + datadict["data"]["city"] + datadict["data"]["isp"]
	else:
		raise SystemError,"The ip %s is wrong." % ip
		sys.exit()

def get_ip_from_domain(www):
	re_ipaddress = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
	re_domain = re.compile(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?')
	if re_domain.match(www):
		result = socket.getaddrinfo(www, None)
		ip_address = result[0][4][0]
		return ip_address
	else:
		raise SystemError,"The domain %s is wrong" % www
		sys.exit()

def get_the_time_now(sign):
	if sign == "begin":
		return datetime.datetime.now()
	elif sign == "end":
		return datetime.datetime.now()
	else:
		print "ERROR..Not the right sign...It should be begin OR end"
		sys.exit()

def caculate_the_seconds(begin,end):
	return end - begin

################################ send mail funcs #################################
#------------- 只有文字，可以发送中文
#
def send_mail_just_text(to_list,subject,content=None):
	if content == None:
		content = ""
	me="hello"+"<"+mail_user+"@"+mail_postfix+">"
	msg = MIMEText(content,_subtype='plain',_charset='UTF8')
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = ";".join(to_list)
	try:
		server = smtplib.SMTP()
		server.connect(mail_host)
		server.starttls()
		server.login(mail_user,mail_pass)
		server.sendmail(me, to_list, msg.as_string())
		server.close()
		return True
	except Exception, e:
		print str(e)
		return False

#------------  发送html格式的邮件
#
def send_mail_html(to_list,subject,content=None):  #to_list：收件人；subject：主题；content：邮件内容
	if content == None:
		content = ""
	me="hello"+"<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
	msg = MIMEText(content,_subtype='html',_charset='UTF8')    #创建一个实例，这里设置为html格式邮件
	msg['Subject'] = subject    #设置主题
	msg['From'] = me
	msg['To'] = ";".join(to_list)
	try:
		s = smtplib.SMTP()
		s.connect(mail_host)  #连接smtp服务器
		s.starttls()
		s.login(mail_user,mail_pass)  #登陆服务器
		s.sendmail(me, to_list, msg.as_string())  #发送邮件
		s.close()
		return True
	except Exception, e:
		print str(e)
		return False

# ------------- 可以发送附件，可以添加多个附件
#
def send_mail_with_att(to_list,subject,att=None):
	#创建一个带附件的实例
	msg = MIMEMultipart()

	if att != None:
		for i in att:
			if os.path.exists(i) != True:
				continue
			else:
				att_tmp = MIMEText(open(i,'rb').read(),'base64','utf8')
				att_tmp["Content-Type"] = 'application/octet-stream'
				att_tmp["Content-Disposition"] = 'attachment; filename="%s"' % os.path.split(i)[1] #这里的filename可以任意写，写什么名字，邮件中显示什么名字
				msg.attach(att_tmp)

	#msg['to'] = 'qq@qq.com'
	msg['to'] =";".join(to_list)
	msg['from'] = 'gg@gmail.com'
	msg['subject'] = subject
	#发送邮件
	try:
		server = smtplib.SMTP()
		server.connect(mail_host)
		server.starttls()
		server.login(mail_user,mail_pass)#XXX为用户名，XXXXX为密码
		server.sendmail(msg['from'], msg['to'],msg.as_string())
		server.quit()
		print '发送成功'
	except Exception, e:
		print str(e)


# ------------- 图片附件，可以发送图片附件。但是附件名称不对
#
def send_mail_with_pic(to_list,subject,pic=None):
	msg = MIMEMultipart()
	msg['To'] = ';'.join(to_list)
	msg['From'] = 'gg@gmail.com'
	msg['Subject'] = '%s' % subject

	txt = MIMEText("发送给你一些图片，瞧瞧吧，亲~~",'plain','utf8')
	msg.attach(txt)

	if pic == None:
		pic = ""
	else:
		for i in pic:
			if os.path.exists(i) != True:
				continue
			else:
				file1 = "%s" % i
				image = MIMEImage(open(file1,'rb').read())
				image.add_header('Content-ID','<image1>')
				msg.attach(image)

	server = smtplib.SMTP()
	server.connect(mail_host)
	server.starttls()
	server.login(mail_user,mail_pass)
	server.sendmail(msg['From'],msg['To'],msg.as_string())
	server.quit()

#------- all types

def send_mail_with_all(to_list,subject,html_content=None,att=None):
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject

	# Create the body of the message (a plain-text and an HTML version).
	if html_content == None:
		html_content = ""
	text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
	html = html_content

	# Record the MIME types of both parts - text/plain and text/html.
	#part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	msg.attach(part2)
	#构造附件
	if att == None:
		att = ""
	else:
		for i in att:
			if os.path.exists(i) != True:
				continue
			else:
				att_tmp = MIMEText(open(i, 'rb').read(), 'base64', 'utf-8')
				att_tmp["Content-Type"] = 'application/octet-stream'
				att_tmp["Content-Disposition"] = 'attachment; filename="%s"' % os.path.split(i)[1]
				msg.attach(att_tmp)

	##加邮件头
	msg['to'] = 'qq@qq.com'
	msg['from'] = 'gg@gmail.com'
	#msg['subject'] = 'hello world'

	server = smtplib.SMTP()
	server.connect(mail_host)
	server.starttls()
	server.login(mail_user,mail_pass)#XXX为用户名，XXXXX为密码
	server.sendmail(msg['from'], msg['to'],msg.as_string())
	server.quit()


def test():
	print "Hello Test"
	sys.exit()

def split_list(list_tmp,N):
	new_list = []
	try:
		N = abs(int(float(N)))
	except:
		print "From functions.py func split_list: N should be int"
		sys.exit()
	N_1 = len(list_tmp) / N
	N_2 = len(list_tmp) % N
	for i in range(N_1):
		new_list.append(list_tmp[i*N:(i+1)*N])
	if N_2 != 0:
		new_list.append(list_tmp[N_1*N:])
	return new_list

def a_list_of_date(given_date,months_num):
	year = int(str(given_date).strip().split('-')[0])
	month = int(str(given_date).strip().split('-')[1])
	out_list = []
	date1 = datetime.date(year,month,1)
	for i in range(int(months_num)):
		date2 = date1 - datetime.timedelta(days=1)
		out_list.append(date2.strftime("%Y-%m"))
		date1 = datetime.date(int(out_list[-1].split('-')[0]),int(out_list[-1].split('-')[1]),1)
	return out_list


def run_shell_command(command_string):
	from subprocess import Popen,PIPE
	cmd = "%s" % command_string.strip()
	p = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
	out,err = p.communicate()
	return (p.returncode,out.rstrip(),err.rstrip())

def is_valid_ip(ip_string):
	try:
		parts = ip_string.split('.')
		return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
	except ValueError:
		return False # one of the 'parts' not convertible to integer
	except (AttributeError, TypeError):
		return False # `ip` isn't even a string


def get_all_ip_from_string(string):
	ret = []
	import re
	ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
	aab = re.findall(ipPattern,string)
	for ip in aab:
		if is_valid_ip(ip):
			ret.append(ip)
	return ret

def get_all_ip_from_string_with_uniq_result(string):
	ret = []
	import re
	ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
	aab = re.findall(ipPattern,string)
	for ip in aab:
		if is_valid_ip(ip):
			ret.append(ip)
	return list(set(ret))

#################################################################################


if __name__ == '__main__':
	a = "2.3.4.5"
