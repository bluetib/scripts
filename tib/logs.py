#!/usr/bin/env python
# -*- coding:utf-8 -*-
# tibliu @ 2014-07-7
#

try:
    import time,os,sys
    import global_vars as vars
    import funcs as my_func
except ImportError,e:
    print "Hi,boss..I catch a exception:",e
    print "And we exit now"
    sys.exit()


class Logging_To_Print:
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __init__(self, *args, **kwargs):
        self.level = self.__class__.INFO
        self.__set_error_color = lambda: None
        self.__set_warning_color = lambda: None
        self.__set_debug_color = lambda: None
        self.__reset_color = lambda: None
        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            if os.name == 'nt':
                import ctypes
                SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute
                GetStdHandle = ctypes.windll.kernel32.GetStdHandle
                self.__set_error_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x04)
                self.__set_warning_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x06)
                self.__set_debug_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x002)
                self.__reset_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x07)
            elif os.name == 'posix':
                self.__set_error_color = lambda: sys.stderr.write('\033[31m')
                self.__set_warning_color = lambda: sys.stderr.write('\033[33m')
                self.__set_debug_color = lambda: sys.stderr.write('\033[32m')
                self.__reset_color = lambda: sys.stderr.write('\033[0m')

    @classmethod
    def getLogger(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def basicConfig(self, *args, **kwargs):
        self.level = int(kwargs.get('level', self.__class__.INFO))
        if self.level > self.__class__.DEBUG:
            self.debug = self.dummy
        #self.basicConfig(format='%(levelname)s - %(asctime)s %(message)s', datefmt='[%b %d %H:%M:%S]')

    def log(self, level, fmt, *args, **kwargs):
        sys.stderr.write('%s - [%s] %s\n' % (level, vars.NOW_TIME, fmt % args))

    def dummy(self, *args, **kwargs):
        pass

    def debug(self, fmt, *args, **kwargs):
        self.__set_debug_color()
        self.log('DEBUG', fmt, *args, **kwargs)
        self.__reset_color()

    def info(self, fmt, *args, **kwargs):
        self.log('INFO', fmt, *args)

    def warning(self, fmt, *args, **kwargs):
        self.__set_warning_color()
        self.log('WARNING', fmt, *args, **kwargs)
        self.__reset_color()

    def warn(self, fmt, *args, **kwargs):
        self.warning(fmt, *args, **kwargs)

    def error(self, fmt, *args, **kwargs):
        self.__set_error_color()
        self.log('ERROR', fmt, *args, **kwargs)
        self.__reset_color()

    def exception(self, fmt, *args, **kwargs):
        self.error(fmt, *args, **kwargs)
        sys.stderr.write(traceback.format_exc() + '\n')

    def critical(self, fmt, *args, **kwargs):
        self.__set_error_color()
        self.log('CRITICAL', fmt, *args, **kwargs)
        self.__reset_color()

class log2:
    def __init__(self,*logs):
        '''
        logs.log("/only/one/log/path")
        '''
        if len(logs) != 1:
            print "Sorry.. You must give one log path now OR you can set the default log_path in [global_vars.py]"
            sys.exit()
            #my_func.mk_dir(vars.LOG_PATH)
            #self.rlog = "%s" % vars.RER_HTML_RLOG
            #self.elog = "%s" % vars.RER_HTML_ELOG
            #my_func.mk_dir_if_not_exist(self.rlog)
            #my_func.mk_dir_if_not_exist(self.elog)
        else:
            rlog_path = os.path.split(logs[0])[0]
            elog_path = os.path.split(logs[0])[0]
            rlog_path = my_func.get_file_abs_path(rlog_path)
            elog_path = my_func.get_file_abs_path(elog_path)
            log_filename = os.path.split(logs[0])[1]
            self.rlog = "%s/log/%s/right_%s" % (rlog_path,vars.CURR_DATE_2,log_filename)
            self.elog = "%s/log/%s/error_%s" % (elog_path,vars.CURR_DATE_2,log_filename)
            #my_func.mk_dir(rlog_path)
            #my_func.mk_dir(elog_path)
            my_func.mk_dir_if_not_exist(self.rlog)
            my_func.mk_dir_if_not_exist(self.elog)
            if os.path.exists(self.rlog) is not True:
                my_func.touch(self.rlog)
            if os.path.exists(self.elog) is not True:
                my_func.touch(self.elog)
            #print self.rlog
            #print self.elog
            #sys.exit()

    def write_run(self,MESSAGE,LEVEL=2):
        if not MESSAGE:
            return -1
        if not LEVEL:
            return -1
        if (LEVEL == 1):
            #print "Don't show log info 1"
            print MESSAGE
        elif (LEVEL == 2):
            #print "Don't show log info 2"
            NEW_MESSAGE = "[%s %s] %s\n" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
            with open(self.rlog,'a+') as File_Object:
                File_Object.write(NEW_MESSAGE)
                File_Object.flush()
                File_Object.close()
        elif (LEVEL == 3):
            NEW_MESSAGE = "[%s %s] %s\n" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
            with open(self.rlog,'a+') as File_Object:
                File_Object.write(NEW_MESSAGE)
                File_Object.flush()
                File_Object.close()
            print "[%s %s] %s" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
        else:
            print "Sorry.. Some ERROR..[You must give me 1 or 2 or 3]"
            sys.exit()

    def write_err(self,MESSAGE,LEVEL=2):
        if not MESSAGE:
            return -1
        if not LEVEL:
            return -1
        if (LEVEL == 1):
            #print "Don't show log info 1"
            print MESSAGE
        elif (LEVEL == 2):
            #print "Don't show log info 2"
            NEW_MESSAGE = "[%s %s] %s\n" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
            with open(self.elog,'a+') as File_Object:
                File_Object.write(NEW_MESSAGE)
                File_Object.flush()
                File_Object.close()
        elif (LEVEL == 3):
            NEW_MESSAGE = "[%s %s] %s\n" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
            with open(self.elog,'a+') as File_Object:
                File_Object.write(NEW_MESSAGE)
                File_Object.flush()
                File_Object.close()
            print "[%s %s] %s" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
        else:
            print "Sorry.. Some ERROR..[You must give me 1 or 2 or 3]"
            sys.exit()

    def get_log_full_path(self):
        rlog = my_func.get_file_abs_path(self.rlog)
        elog = my_func.get_file_abs_path(self.elog)
        return (rlog,elog)

class log:
    def __init__(self,*logs):
        '''
        logs.log("/right_log_path","/error_log_path")
        '''
        if len(logs) != 2:
            #print "Sorry.. You must give two log path now OR you can set the default log_path in [global_vars.py]"
            #sys.exit()
            my_func.mk_dir(vars.LOG_PATH)
            self.rlog = "%s" % vars.RER_HTML_RLOG
            self.elog = "%s" % vars.RER_HTML_ELOG
            my_func.mk_dir_if_not_exist(self.rlog)
            my_func.mk_dir_if_not_exist(self.elog)
        else:
            rlog_path = os.path.split(logs[0])[0]
            elog_path = os.path.split(logs[1])[0]
            rlog_filename = os.path.split(logs[0])[1]
            elog_filename = os.path.split(logs[1])[1]
            self.rlog = "%s/log/%s/%s" % (rlog_path,vars.CURR_DATE_2,rlog_filename)
            self.elog = "%s/log/%s/%s" % (elog_path,vars.CURR_DATE_2,elog_filename)
            #my_func.mk_dir(rlog_path)
            #my_func.mk_dir(elog_path)
            my_func.mk_dir_if_not_exist(self.rlog)
            my_func.mk_dir_if_not_exist(self.elog)

            #print self.rlog
            #print self.rlog
            #sys.exit()

    def write_run(self,MESSAGE,LEVEL=3):
        if not MESSAGE:
            return -1
        if not LEVEL:
            return -1
        if (LEVEL == 1):
            #print "Don't show log info 1"
            print MESSAGE
        elif (LEVEL == 2):
            #print "Don't show log info 2"
            NEW_MESSAGE = "[%s %s] %s\n" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
            File_Object = open(self.rlog,'a+')
            File_Object.write(NEW_MESSAGE)
            File_Object.close()
        elif (LEVEL == 3):
            NEW_MESSAGE = "[%s %s] %s\n" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
            File_Object = open(self.rlog,'a+')
            File_Object.write(NEW_MESSAGE)
            File_Object.close()
            print "[%s %s] %s" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
        else:
            print "Sorry.. Some ERROR..[You must give me 1 or 2 or 3]"
            sys.exit()

    def write_err(self,MESSAGE,LEVEL=3):
        if not MESSAGE:
            return -1
        if not LEVEL:
            return -1
        if (LEVEL == 1):
            #print "Don't show log info 1"
            print MESSAGE
        elif (LEVEL == 2):
            #print "Don't show log info 2"
            NEW_MESSAGE = "[%s %s] %s\n" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
            File_Object = open(self.elog,'a+')
            File_Object.write(NEW_MESSAGE)
            File_Object.close()
        elif (LEVEL == 3):
            NEW_MESSAGE = "[%s %s] %s\n" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
            File_Object = open(self.elog,'a+')
            File_Object.write(NEW_MESSAGE)
            File_Object.close()
            print "[%s %s] %s" % (vars.CURR_DATE_1,vars.CURR_TIME_4,MESSAGE)
        else:
            print "Sorry.. Some ERROR..[You must give me 1 or 2 or 3]"
            sys.exit()


if __name__ == "__main__":
    pass
