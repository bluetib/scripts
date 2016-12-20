#!/usr/bin/env python

#author: tib
#date: 2014-9-9
#desc: This script is used to get the most result file of all different password.tib

import os,sys,glob,json

def help():
    print "Usage:\n\t%s password.tib" % sys.argv[0]
    sys.exit()

def get_list_of_all(file_filter):
    if os.path.sep not in file_filter:
        return [ os.getcwd() + os.sep + "%s" % i for i in glob.glob(file_filter) ]
    else:
        file_path = os.path.split(file_filter)[0]
        if os.path.exists(file_path) is not True:
            print "File Path %s not exist" % file_path
            sys.exit(1)
        return [ os.getcwd() + os.sep + "%s" % os.path.split(i)[1] for i in glob.glob(file_filter) ]

def get_the_biggest_file(file_list):
    first_file = file_list[0]
    tmp_list = file_list[:]
    for i in get_list_from_remove(tmp_list,first_file):
        if len(json.loads(open(first_file).read())) < len(json.loads(open(i).read())):
            first_file = i
    return first_file

def get_the_num(New_ID,tmp_list):
    _tmp_l = tmp_list
    _New_ID = int(New_ID) + 1
    if str(_New_ID) not in _tmp_l:
        #get_the_num(New_ID,tmp_list)
        return _New_ID
    else:
    #return get_the_num(New_ID,tmp_list)
    #print New_ID
    #return New_ID
        return get_the_num(_New_ID,_tmp_l)

def check_and_append_to_biggest(littler,bigger):
    New_ID = get_the_num(len(bigger),bigger.keys())
    for k,v in littler.items():
        if k in bigger.keys() and k == "42":
            if v["password"] != bigger[k]["password"] or v["username"] != bigger[k]["username"] or v["type"] != bigger[k]["type"]:
                bigger["%s" % New_ID] = v
                #print bigger["%s" % New_ID]
                #sys.exit()
        else:
            bigger[k] = v
    return bigger


def check_and_append_to_biggest_2(littler,bigger):
    for k_litter,v_litter in littler.items():
        for k_bigger,v_bigger in bigger.items():
            if v_bigger["password"].strip().lower() == v_litter["password"].strip().lower() and v_bigger["username"].strip().lower() == v_litter["username"].strip().lower() and v_bigger["keyword"].strip().lower() == v_litter["keyword"].strip().lower():
                append_choice = "no"
                break
            else:
                append_choice = "yes"
        if append_choice == "yes":
            bigger["%s" % get_the_num(len(bigger),bigger.keys())] = v_litter
    return bigger


def get_list_from_remove(file_list,file_name):
    if len(file_list) == 0:
        return file_list
    file_list.remove(file_name)
    return file_list


def main():
    Biggest_File_Json = json.loads(open(password_file).read())
    print "*_* " * 50
    #print Biggest_File_Json
    #for k in Biggest_File_Json.keys():
    #   print k
    a = Biggest_File_Json.keys()
    a.sort(key=int)
    for i in range(1,int(a[-1:][0])+1):
        if Biggest_File_Json.has_key("%s" % i):
            print "=" * 110
            print "%s has key : %s" % ("Biggest_File_Json",i)
            print "values: %s" % Biggest_File_Json["%s" % i]
            print "=" * 110
        else:
            print "#" * 110
            print "I can't find the key: %s |||||   X_X  |||||||" % i
            print "#" * 110
    print "*_* " * 50
    print '''\nPassword File [%s] has all [%s] records\n''' % (password_file,len(Biggest_File_Json))
    #print "password.tib.1 json is:%s" % len(json.loads(open("password.tib.1").read()))
    #print "password.tib.2 json is:%s" % len(json.loads(open("password.tib.2").read()))
    #print "password.tib.3 json is:%s" % len(json.loads(open("password.tib.3").read()))
    #print "password.tib.4 json is:%s" % len(json.loads(open("password.tib.4").read()))
    #print "password.tib.5 json is:%s" % len(json.loads(open("password.tib.5").read()))
    #print "password.tib.6 json is:%s" % len(json.loads(open("password.tib.6").read()))
    #print "Biggest_File_Json is %s" % len(Biggest_File_Json)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        help()
    password_file = sys.argv[1]
    if os.path.exists(password_file) is not True:
        print "File Not Exists .. [%s]" % password_file
        sys.exit()
    main()
