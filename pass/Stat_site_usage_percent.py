#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os,sys,time
import urllib2
import json
import datetime
import shutil

stat_file = "/var/lib/stat_site_usage_percent.json"
log_file = "/var/log/stat_site_usage_percent.log"
stat_result_file = "%s_%s.%s" % (stat_file.split(".")[0],time.strftime("%Y-%m-%d"),stat_file.split(".")[1])


if os.path.exists(os.path.split(stat_file)[0]) is not True:
    os.makedirs(os.path.split(stat_file)[0])
if os.path.exists(os.path.split(log_file)[0]) is not True:
    os.makedirs(os.path.split(stat_file)[0])

the_check_site_list = \
    [
        [ "http://www.baidu.com","百度"],
        [ "http://www.google.com/","谷歌"]
    ]

def deal_with_the_stat_file():
    which_day = datetime.date.today().isoweekday()
    #if which_day == 7:
    if time.strftime("%H") == "23" and int(time.strftime("%M")) >= 59:
    #if time.strftime("%H") == "23" and int(time.strftime("%M")) >= 59 and int(time.strftime("%M")) <= 57:
        if os.path.exists(stat_file) is True:
            #shutil.copy(stat_file,stat_result_file)
            os.remove(stat_file)
        else:
            log_to("No stat_file now")

def log_to(log_str):
    f = open(log_file,"a+")
    f.write("%s --- %s\n" % (time.strftime("[%Y-%m-%d %H:%M:%S]"),str(log_str).strip()))
    f.close()

def print_json(json_obj,indent_=4):
    print "-" * 50
    print json.dumps(json_obj,indent=indent_,ensure_ascii=False,sort_keys=True)
    print "-" * 60

def get_to_site(site_url):
    site_url = str(site_url).strip()
    if site_url.startswith("http://"):
        site_url_with_https = "https://" + site_url.split('http://')[1]
        site_url_without_https = site_url
    elif site_url.startswith("https://"):
        site_url_with_https = site_url
        site_url_without_https = "http://" + site_url.split('https://')[1]
    else:
        site_url_with_https = "https://" + site_url
        site_url_without_https = "http://" + site_url

    try:
        response = urllib2.urlopen(site_url_without_https,timeout=10)

        response_code = response.getcode()
        response_headers = response.headers.items()
        response_msg = response.msg
        response_url = response.geturl()
        response_content = response.read()
    except (urllib2.URLError,urllib2.HTTPError),e:
        log_to("Error info : %s ----- [%s]" % (str(e),site_url))
        response_code = ""
        response_headers = ""
        response_msg = ""
        response_url = ""
        response_content = ""
    except:
        log_to("Error info : something I don't know ----- [%s]" % site_url)
        response_code = ""
        response_headers = ""
        response_msg = ""
        response_url = ""
        response_content = ""


    return {'code':response_code,'headers':response_headers,'msg':response_msg,'url':response_url,'content':response_content}


if __name__ == '__main__':
    while True:
        result_dic = {}
        if os.path.exists(stat_file) is not True:
            for i in the_check_site_list:
                result_dic["%s" % i[0]] = {}
                result_dic["%s" % i[0]]['site_url'] = "%s" % i[0]
                result_dic["%s" % i[0]]['OK'] = 0
                result_dic["%s" % i[0]]['PROBLEM'] = 0
                result_dic["%s" % i[0]]['key_word_not_match'] = 0
                result_dic["%s" % i[0]]['TOTAL'] = 1440
                result_dic["%s" % i[0]]['ok_percent'] = 0
                result_dic["%s" % i[0]]['problem_percent'] = 0
        else:
            if len(open(stat_file).read()) != 0:
                result_dic = json.loads(open(stat_file).read())
            else :
                for i in the_check_site_list:
                    result_dic["%s" % i[0]] = {}
                    result_dic["%s" % i[0]]['site_url'] = "%s" % i[0]
                    result_dic["%s" % i[0]]['OK'] = 0
                    result_dic["%s" % i[0]]['PROBLEM'] = 0
                    result_dic["%s" % i[0]]['key_word_not_match'] = 0
                    result_dic["%s" % i[0]]['TOTAL'] = 1440
                    result_dic["%s" % i[0]]['ok_percent'] = 0
                    result_dic["%s" % i[0]]['problem_percent'] = 0

        for i in the_check_site_list:
            response = get_to_site(i[0])
            if response['code'] == 200 and i[1] in response['content']:
                result_dic['%s' % i[0]]['OK'] = result_dic["%s" % i[0]]['OK'] + 1
            elif response['code'] == 200 and i[1] not in response['content']:
                result_dic['%s' % i[0]]['PROBLEM'] = result_dic["%s" % i[0]]['PROBLEM'] + 1
                result_dic['%s' % i[0]]['key_word_not_match'] = result_dic["%s" % i[0]]['key_word_not_match'] + 1
            else:
                result_dic['%s' % i[0]]['PROBLEM'] = result_dic["%s" % i[0]]['PROBLEM'] + 1

            result_dic['%s' % i[0]]['ok_percent'] = str(float(float(result_dic['%s' % i[0]]['OK']) / float(result_dic['%s' % i[0]]['TOTAL'])) * 100)
            result_dic['%s' % i[0]]['problem_percent'] = str(float(float(result_dic['%s' % i[0]]['PROBLEM']) / float(result_dic['%s' % i[0]]['TOTAL'])) * 100)
            result_dic['%s' % i[0]]['ok_percent'] = result_dic['%s' % i[0]]['ok_percent'][:5] + "%"
            result_dic['%s' % i[0]]['problem_percent'] = result_dic['%s' % i[0]]['problem_percent'][:5] + "%"

        print_json(result_dic)
        open(stat_file,'w+').write(json.dumps(result_dic,indent=4,ensure_ascii=False,sort_keys=True))
        shutil.copy(stat_file,stat_result_file)

        deal_with_the_stat_file()

        time.sleep(60)
