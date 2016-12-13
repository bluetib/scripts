#!/usr/bin/env python
# -*- coding:utf-8 -*-

#
#
#

try:
    import time
    import sys
    import funcs as funcs
    import MySQLdb,sys,os,time
    import global_vars as vars
except ImportError,e:
    print "I catch a exception for you:",e
    sys.exit()

class mysql:

    def __init__(self):
        self.host = ""
        self.port = ""
        self.user = ""
        self.password = ""
        self.db = ""
        self.this_conn = None
        self.this_cursor = None
        self.charset = "utf8"

    def sql_conn(self,*args,**zidian):
        #global this_cursor,this_conn
        if  len(args) == 3 and len(zidian) == 0:
            host = args[0]
            user = args[1]
            password = args[2]
            self.this_conn = MySQLdb.connect(host=host,user=user,passwd=password,charset=self.charset)
            self.this_cursor = self.this_conn.cursor()
        elif len(args) == 4 and len(zidian) == 0:
            host = args[0]
            user = args[1]
            password = args[2]
            port = args[3]
            self.this_conn = MySQLdb.connect(host=host,user=user,passwd=password,port=port,charset=self.charset)
            self.this_cursor = self.this_conn.cursor()
        elif len(args) == 5 and len(zidian) == 0:
            host = args[0]
            user = args[1]
            password = args[2]
            port = args[3]
            db = args[4]
            self.this_conn = MySQLdb.connect(host=host,user=user,passwd=password,port=port,db=db,charset=self.charset)
            self.this_cursor = self.this_conn.cursor()
        elif len(args) == 2 and len(zidian) == 0:
            host = args[0]
            user = args[1]
            self.this_conn = MySQLdb.connect(host=host,user=user,charset=self.charset)
            self.this_cursor = self.this_conn.cursor()
        elif len(args) == 0 and len(zidian) == 0:
            #this_conn = MySQLdb.connect(db=self.db,host=self.host,port=self.port,user=self.user,passwd=self.password)
            self.this_conn = MySQLdb.connect(db=self.db,host=self.host,port=self.port,user=self.user,passwd=self.password,use_unicode=True,charset='utf8')
            self.this_cursor = self.this_conn.cursor()
        elif len(zidian) == 4:
            host = zidian["host"]
            port = zidian["port"]
            user = zidian["user"]
            password = zidian["password"]
            self.this_conn = MySQLdb.connect(host=host,user=user,passwd=password,port=port,charset=self.charset)
            self.this_cursor = self.this_conn.cursor()
        elif len(zidian) == 3:
            host = zidian["host"]
            user = zidian["user"]
            password = zidian["password"]
            self.this_conn = MySQLdb.connect(host=host,user=user,passwd=password,charset=self.charset)
            self.this_cursor = self.this_conn.cursor()
        elif len(args) == 1 and len(zidian) == 0:
            db = args[0]
            self.this_conn = MySQLdb.connect(db=db,host=self.host,port=self.port,user=self.user,passwd=self.password,charset=self.charset)
            self.this_cursor = self.this_conn.cursor()

    def sql_exec(self,*sql):
        self.this_cursor.execute(sql[0])

    def sql_get_result_only_one_list(self):
        return_tmp = []
        return_things = self.this_cursor.fetchall()
        for every_line in return_things:
            return_tmp.append(list(every_line))
        return return_tmp

    def sql_get_result(self):
        return_things = self.this_cursor.fetchall()
        return return_things

    def sql_close(self):
        if self.this_conn:
            self.this_conn.commit()
            self.this_cursor.close()
            self.this_conn.close()


if __name__ == '__main__':
    #try:
    new_conn = mysql()
    #new_conn.sql_conn()
    #new_conn.sql_conn('112.124.13.219','root','mys_66')
    new_conn.sql_conn(vars.DEV_DB_HOST,vars.DEV_DB_USER,vars.DEV_DB_PASSWORD,vars.DEV_DB_PORT,vars.DEV_DB_NAME)
    b = '''show databases;'''
    #a = '''replace into t_bankcard_info(id,userId,bankName,branchBankName,area,cardNo) values(54,1286,"中国农业银行","北京市分行昌平区支行南口分理处","北京北京市","6228480010944588614");'''
    #new_conn.sql_exec('''use tmp_for_test_xiaofeng;''')
    new_conn.sql_exec(b)
    #new_conn.sql_exec('''select p1.username,p2.realname,from_unixtime(p2.verify_time) as verify_time,p3.phone,p1.email,from_unixtime(p1.last_time) as last_time,p1.logintime from deayou_approve_realname as p2 left join deayou_users as p1 on p1.user_id=p2.user_id left join deayou_users_info as p3 on p1.user_id=p3.user_id where from_unixtime(p2.verify_time) between "2013-12-29" and "2013-12-30" and p2.status=1;''')
    all_result = funs.t_to_l(new_conn.sql_get_result())
    print all_result
    sys.exit()
    new_conn.sql_exec('''select count(*) from deayou_borrow_tender;;''')
    result_2 = new_conn.sql_get_result()
    new_conn.sql_close()
    for i in range(len(all_result[0])):
        print i,all_result[0][i]
        if i == 11:
            print all_result[0][i].decode("GB2312").encode("UTF8")
        time.sleep(1)
        #realname = all_result[i].decode("GB2312").encode("UTF8")
        #print realname
    sys.exit()
    time.sleep(1)
    for i in all_result:
        print i
        time.sleep(0.04)
    #except Exception,e:
    #   print "Oh..No...I catch exception...%s" % e
