#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys,os,time

try:
    from tib import funcs
except Exception as e:
    print "Sorry..no tib found in this machine"
    sys.exit(2)

funcs.cd_into_cwd_dir(sys.argv[0])

if len(sys.argv) != 4:
    print '''Usage:\n\t%s repository commit [file/content]''' % sys.argv[0]
    sys.exit(1)
else:
    repository = "%s" % sys.argv[1]
    commit = "%s" % sys.argv[2]
    choice = "%s" % sys.argv[3]

if choice == "file":
    cmd_string = '''cd %s && git show --pretty="" --name-only %s''' % (repository,commit)
elif choice == "content":
    cmd_string = '''cd %s && git show %s''' % (repository,commit)
else:
    print '''Usage:\n\t%s repository commit [file/content]''' % sys.argv[0]
    sys.exit(1)
ret = funcs.run_shell_command_2(cmd_string)
if ret[0] == "ok":
    print ret[1]
    print "-" * 50
else:
    print "some error.."
    print ret[2]

