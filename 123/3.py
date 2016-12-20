#!/usr/bin/env /python
# -*- coding:utf-8 -*-

a = [u"北极",u"日本"]
a = ["北极","日本"]
print type(a[0])
print repr(a[0].decode('utf8')).replace(r'\u',r"%u")
#for i in a:
#   print type(i)
