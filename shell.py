# coding=utf-8
import subprocess
import select
import os, signal
import psutil
import sys

ignore_msgs = ['mp3float','Last message','frame=','configuration:','frame=']
##################################################
def OutputShell( cmd, msgout=True ):
	print( 'shell:',msgout,cmd[0:200])
	result = subprocess.Popen(
		#[ "ping 127.0.0.1" ],
		#[ "find /usr" ],
		[ cmd ],
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	)
	# read date from pipe
	select_rfds = [ result.stdout, result.stderr ]
	last_msg = ''
	last_errmsg = ''
	while len( select_rfds ) > 0:
		(rfds, wfds, efds) = select.select( select_rfds, [ ], [ ] ) #select函数阻塞进程，直到select_rfds中的套接字被触发
		if result.stdout in rfds:
			readbuf_msg = result.stdout.readline()      #行缓冲
			if len( readbuf_msg ) == 0:
				select_rfds.remove( result.stdout )     #result.stdout需要remove，否则进程不会结束
			else:
				#print( readbuf_msg.decode("utf-8"))
				try:
					last_msg = str(readbuf_msg, 'utf8')
					if msgout:
							print(last_msg,end='')
				except:
					last_msg = 'OutputShell:error last_msg utf8'

		if result.stderr in rfds:
			readbuf_errmsg = result.stderr.readline()
			if len( readbuf_errmsg ) == 0:
				select_rfds.remove( result.stderr )     #result.stderr，否则进程不会结束
			else:
				try:
					last_errmsg = str(readbuf_errmsg, 'utf8')
					if msgout:
							print(last_errmsg,end='')
				except:
					last_errmsg = 'OutputShell:error readbuf_errmsg utf8'
	result.wait() # 等待字进程结束( 等待shell命令结束 )
	#print result.returncode
	##(stdoutMsg,stderrMsg) = result .communicate()#非阻塞时读法.
	if not msgout:
		print('last_msg:',last_msg,end='')
		print('last_errmsg:',last_errmsg,end='')
	return result.returncode

# {'pid': 538, 'name': 'ffmpeg', 'status': 'sleeping'}
# {'pid': 538, 'name': 'ffmpeg', 'status': 'disk-sleep'}
def procs_info(name="ffmpeg"):
	"""
	进程信息
	:param name:
	:return:
	"""
	procs = []
	pids = psutil.pids()
	for pid in pids:
		p = psutil.Process(pid)
		if p.name() == name:
			procs.append({"pid":p.pid,"name":p.name(),"status":p.status()})
	return procs

# def kill_ffmpeg(parent=False):
# 	"""
# 	进程信息
# 	:param name:
# 	:return:
# 	"""
# 	pids = psutil.pids()
# 	for pid in pids:
# 		p = psutil.Process(pid)
# 		if p.name() == "ffmpeg":
# 			print("ffmpeg",p.pid,p.ppid())
# 			os.kill(int(p.ppid()),signal.SIGKILL)
# 			os.kill(int(p.pid),signal.SIGKILL)

def proc_kill(name="ffmpeg",parent=False):
	"""
	进程信息
	:param name:ffmpeg,python
	:param parent:kill parent
	:return:
	"""
	pids = psutil.pids()
	for pid in pids:
		p = psutil.Process(pid)
		if p.name() == name:
			print(name,p.pid,p.ppid())
			if parent:
				os.kill(int(p.ppid()),signal.SIGKILL)
			if 'python' == name:
				#cmd = 'kill {}&/usr/share/pyenv/versions/3.8.17/bin/python wsgi.py'
				cmd = 'kill {}&{} wsgi.py'
				pythonpath = sys.executable
				print(pythonpath)
				OutputShell(cmd.format(p.pid,pythonpath),True)
			else:
				os.kill(int(p.pid),signal.SIGKILL)

def include_ignore_msg(msg):
	for keyword in ignore_msgs:
		if msg.find(keyword) != -1:
			return True
	return False

if __name__ == '__main__':
	OutputShell('ls -l',True)