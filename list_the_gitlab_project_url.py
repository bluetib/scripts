#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,os,time,json
try:
    if os.path.exists('func.py'):
        import func
        print_json = func.print_json
except:
    def print_json(json_str):
        print "+" * 100
        print json.dumps(json_str,indent=4,sort_keys=True,ensure_ascii=False)
        print "+" * 100
        print "\n"
    print_json = print_json

try:
    import gitlab
except:
    print "Sorry. Import module gitlab failed."
    print "\nMaybe you need install gitlab first.You can use this command to install the module."
    print "[For Mac: sudo pip install python-gitlab]"
    print "[For Linux: pip install python-gitlab]"
    sys.exit()

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print "Usage:\n\t%s \"%s\" [%s]" % (sys.argv[0],"Group Name","Project Name")
    sys.exit()

group_name = None
project_name = None

if len(sys.argv) == 2:
    group_name = str(sys.argv[1]).lower()
elif len(sys.argv) == 3:
    group_name = str(sys.argv[1]).lower()
    project_name = str(sys.argv[2]).lower()
else:
    print "Usage:\n\t%s \"%s\" [%s]" % (sys.argv[0],"Group Name","Project Name")
    sys.exit()

######################################################
# 把你的gitlab地址和个人的Private Token写在这里
gitlab_url = "https://gitlab.xxxx.net"
private_token = '''3333333333333333'''
need_local_file = True
######################################################

if str(gitlab_url) == "" or str(private_token) == "":
    print "Sorry. Please 填写gitlab_url 和 私人Token [直接写在文件里面]"
    sys.exit()



def make_a_json(data):
    love = {}
    for i in range(len(data)):
        tmp_dic = json.loads(data[i].json())
        a = {"created_at":tmp_dic["created_at"],"default_branch":tmp_dic["default_branch"],"description":tmp_dic["description"],"http_url_to_repo":tmp_dic["http_url_to_repo"],"last_activity_at":tmp_dic["last_activity_at"],"name":tmp_dic["name"],"name_with_namespace":tmp_dic["name_with_namespace"],"namespace.name":tmp_dic["namespace"]["name"],"namespace.description":tmp_dic["namespace"]["description"],"path_with_namespace":tmp_dic["path_with_namespace"],"ssh_url_to_repo":tmp_dic["ssh_url_to_repo"],"web_url":tmp_dic["web_url"],u"负责人":"",u"备注其他信息":""}
        #a = decode_dict(a)
        love[i] = a
    with open("all_projects.json","w") as f:
        #f.write(json.dumps(love,indent=4,ensure_ascii=False,sort_keys=True))
        f.write(func.json_dumps_unicode_to_string(love).encode("UTF-8"))
    return love

def check_file():
    if os.path.exists("all_projects.json") and func.get_file_size("all_projects.json")[0] > 0:
        return func.json_loads_unicode_to_string(open("all_projects.json").read())
    else:
        print "I am getting all projects. Please just wait for a while"
        all_projects = gl.projects.all(all=True)
        return make_a_json(all_projects)

def get_all_group_name_1(data):
    l_1 = []
    for k,v in data.items():
        if str(v['namespace.name']).strip() != "":
            l_1.append(str(v['namespace.name']).strip())
    return set(l_1)

def get_all_projects_by_group_name(g_name,total_projects):
    l_2 = []
    for k,v in total_projects.items():
        if str(g_name).strip().lower() == v['path_with_namespace'].split('/')[0]:
            l_2.append(v['ssh_url_to_repo'])
    return l_2

def just_get_one_project_by_group_name_and_project_name(g_name,p_name,total_projects):
    l_3 = []
    for k,v in total_projects.items():
        if str(g_name).strip().lower() == v['path_with_namespace'].split('/')[0] and str(p_name).strip().lower() == v['path_with_namespace'].split('/')[1]:
            l_3.append(v['ssh_url_to_repo'])
    return l_3


if __name__ == '__main__':
    gl = gitlab.Gitlab(gitlab_url, private_token)
    if need_local_file:
        result = check_file()
    else:
        print "I am getting all projects. Please just wait for a while"
        all_projects = gl.projects.all(all=True)
        result = make_a_json(all_projects)
    #func.print_json_with_sort_all_num_keys(result)
    #print get_all_group_name(result)
    #print just_get_one_project_by_group_name_and_project_name(group_name,project_name,result)
    if group_name and project_name:
        for i in just_get_one_project_by_group_name_and_project_name(group_name,project_name,result):
            print i
    elif group_name and not project_name:
        for i in get_all_projects_by_group_name(group_name,result):
            print i

