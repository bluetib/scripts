#!/usr/bin/env python

#author: tib
#date: 2014-9-9
#desc: This script is used to get the most result file of all different password.tib

import os,sys,glob,json

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
        return get_the_num(_New_ID,_tmp_l)

def check_and_append_to_biggest(littler,bigger):
    New_ID = get_the_num(len(bigger),bigger.keys())
    for k,v in littler.items():
        if k in bigger.keys() and k == "42":
            if v["password"] != bigger[k]["password"] or v["username"] != bigger[k]["username"] or v["type"] != bigger[k]["type"]:
                bigger["%s" % New_ID] = v
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
            print "Opps...for key: %s" % get_the_num(len(bigger),bigger.keys())
            bigger["%s" % get_the_num(len(bigger),bigger.keys())] = v_litter
    return bigger


def get_list_from_remove(file_list,file_name):
    if len(file_list) == 0:
        return file_list
    file_list.remove(file_name)
    return file_list


def main():
    file_filter_str = '''password.tib.*'''
    all_file_list = get_list_of_all(file_filter_str)
    Biggest_File = get_the_biggest_file(all_file_list)
    last_list = get_list_from_remove(all_file_list,Biggest_File)
    Biggest_File_Json = json.loads(open(Biggest_File).read())
    for single_file_in_last_list in last_list:
        single_file_in_last_list_Json = json.loads(open(single_file_in_last_list).read())
        Biggest_File_Json = check_and_append_to_biggest_2(single_file_in_last_list_Json,Biggest_File_Json)
    last_info = json.dumps(Biggest_File_Json,ensure_ascii=False,sort_keys=True,indent=4)
    f = open("password.tib","w")
    f.write(last_info)
    f.close()

if __name__ == '__main__':
    main()
