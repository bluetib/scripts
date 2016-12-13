#!/usr/bin/env python

#author: tib
#desc: this script is used to sort and uniq the txt file and store result to new file

import os,time,sys

if len(sys.argv) != 3:
    print "Opps...I need two args..\n"
    print "Usage:\t%s old_file_path result_file_path" % sys.argv[0]
    sys.exit()

old_file = sys.argv[1]
result_file = sys.argv[2]
result_file_dir = os.path.split(result_file)[0]
if os.path.exists(result_file_dir) != True:
    os.makedirs(result_file_dir)


if __name__ == '__main__':
    if os.path.exists(old_file) != True:
        print "Opps...The file not exist..[%s]" % old_file
        sys.exit()
    old_list = open(old_file).read().splitlines()
    new_list = []
    result_f_obj = open(result_file,"w")
    for i in old_list:
        if len(i.strip()) == 0:
            continue
        else:
            new_list.append(i.strip())
    result_new_list = list(set(new_list))
    result_new_list.sort()
    for j in result_new_list:
        result_f_obj.write("%s\n" % j)
    result_f_obj.close()

