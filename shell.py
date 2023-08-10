# coding=utf-8
import subprocess
import select
import os, signal
import psutil
import sys
from queue import Queue

MAX_MSG_NUM = 100
#[flv @ 0x55b7d2d96a80] Non-monotonous DTS in output stream 0:1; previous: 739658, current: 420381; changing to 739658. This may result in incorrect timestamps in the output file.
ignore_msgs = ['mp3float','Last message','frame=','configuration:','[flv @']
print('shell v5.6.0',MAX_MSG_NUM,ignore_msgs)
##################################################
def ShellRun( cmd, stdout=False,  stderr=False, lastmsgout=False):
	"""
	新shell，便于优化输出，提高性能
	:param cmd: cmd string
	:param stdout: False
	:param stderr: False
	:param lastmsgout: False
	:return: returncode
	"""
	if stdout:
		return OutputShell(cmd,True)	#need
	else:
		if stderr:
			return OutputShell(cmd,True)	#ok
		else:
			if lastmsgout:
				# 仅输出最后100条消息
				return OutputShell(cmd,False)	#need
			else:
				# 什么都不输出
				print( 'ShellRun:stdout={} stderr={} lastmsgout={}'.format(stdout,stderr,lastmsgout),cmd[0:400])
				result = subprocess.Popen(
					[ cmd ],
					shell=True,
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				)
				# read date from pipe
				select_rfds = [ result.stdout, result.stderr ]
				while len( select_rfds ) > 0:
					(rfds, wfds, efds) = select.select( select_rfds, [ ], [ ] ) #select函数阻塞进程，直到select_rfds中的套接字被触发
					if result.stdout in rfds:
						readbuf_msg = result.stdout.readline()      #行缓冲
						if len( readbuf_msg ) == 0:
							select_rfds.remove( result.stdout )     #result.stdout需要remove，否则进程不会结束
					if result.stderr in rfds:
						readbuf_errmsg = result.stderr.readline()
						if len( readbuf_errmsg ) == 0:
							select_rfds.remove( result.stderr )     #result.stderr，否则进程不会结束
				result.wait() # 等待字进程结束( 等待shell命令结束 )
				print('ShellRun exit:',result.returncode)
				return result.returncode

def OutputShell( cmd, msgout=True ):
	# msgout, if False, print last 100 msg
	msg_queue_obj = Queue(MAX_MSG_NUM)  # 创建一个队列对象
	print( 'shell:',msgout,cmd[0:400])
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
							if 'frame='!=last_msg[0:6]:
								if '[flv @'!=last_msg[0:6]:
									print(last_msg,end='')
					else:
						msg_queue_obj = fifo_msg(msg_queue_obj,last_msg)
				except:
					msg_queue_obj = fifo_msg(msg_queue_obj,'OutputShell:error last_msg utf8')

		if result.stderr in rfds:
			readbuf_errmsg = result.stderr.readline()
			if len( readbuf_errmsg ) == 0:
				select_rfds.remove( result.stderr )     #result.stderr，否则进程不会结束
			else:
				try:
					last_errmsg = str(readbuf_errmsg, 'utf8')
					if msgout:
							if 'frame='!=last_errmsg[0:6]:
								if '[flv @'!=last_errmsg[0:6]:
									print(last_errmsg,end='')
					else:
						msg_queue_obj = fifo_msg(msg_queue_obj,last_errmsg)
				except:
					msg_queue_obj = fifo_msg(msg_queue_obj,'OutputShell:error readbuf_errmsg utf8')
	result.wait() # 等待字进程结束( 等待shell命令结束 )
	#print result.returncode
	##(stdoutMsg,stderrMsg) = result .communicate()#非阻塞时读法.
	if not msgout:
		while not msg_queue_obj.empty():
			print('last_msg:',msg_queue_obj.get(),end='')
	return result.returncode

##################################################
def OutputShell_Old( cmd, msgout=True ):
	# output twice ignore_msgs
	# if print last 20 msg
	ignore_msgs_times = [0,0,0,0]
	msg_queue_obj = Queue(MAX_MSG_NUM)  # 创建一个队列对象
	print( 'shell:',msgout,cmd[0:400])
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
					msg_queue_obj = fifo_msg(msg_queue_obj,last_msg)
					if msgout:
							info_ignore = include_ignore_msg(last_msg)
							if info_ignore:
								if ignore_msgs_times[info_ignore.get('index')] < 2:
									print(last_msg,end='')
								ignore_msgs_times[info_ignore.get('index')] += 1
							else:
								print(last_msg,end='')
				except:
					msg_queue_obj = fifo_msg(msg_queue_obj,'OutputShell:error last_msg utf8')

		if result.stderr in rfds:
			readbuf_errmsg = result.stderr.readline()
			if len( readbuf_errmsg ) == 0:
				select_rfds.remove( result.stderr )     #result.stderr，否则进程不会结束
			else:
				try:
					last_errmsg = str(readbuf_errmsg, 'utf8')
					msg_queue_obj = fifo_msg(msg_queue_obj,last_errmsg)
					if msgout:
							info_ignore = include_ignore_msg(last_errmsg)
							if info_ignore:
								if ignore_msgs_times[info_ignore.get('index')] < 2:
									print(last_errmsg,end='')
								ignore_msgs_times[info_ignore.get('index')] += 1
							else:
								print(last_errmsg,end='')
				except:
					msg_queue_obj = fifo_msg(msg_queue_obj,'OutputShell:error readbuf_errmsg utf8')
	result.wait() # 等待字进程结束( 等待shell命令结束 )
	#print result.returncode
	##(stdoutMsg,stderrMsg) = result .communicate()#非阻塞时读法.
	if not msgout:
		while not msg_queue_obj.empty():
			print('last_msg:',msg_queue_obj.get(),end='')
	return result.returncode


# {'memory_info': pmem(rss=158830592, vms=1099399168, shared=33619968, text=258048, lib=0, data=392126464, dirty=0), 'name': 'ffmpeg', 'cpu_percent': 0.0, 'status': 'sleeping', 'cmdline': ['ffmpeg', '-re', '-i', 'aux/coco/192k-CoCo-想你的365天.m4a', '-ss', '0', '-t', '3260.95', '-f', 'lavfi', '-i', 'color=c=0x000000:s=770x432:r=25', '-i', 'img/art_coco103.jpg', '-filter_complex', '[1:v][2:v]overlay=x=0:y=0[outv];[0:0]concat=n=1:v=0:a=1[outa]', '-map', '[outv]', '-map', '[outa]', '-vcodec', 'libx264', '-acodec', 'aac', '-b:a', '192k', '-f', 'mp4', 'test.mp4'], 'pid': 10782}
def process_info(name="ffmpeg"):
	"""
	进程信息
	:param name:
	:return: process_info
	"""
	pids = psutil.pids()
	for pid in pids:
		p = psutil.Process(pid)
		if p.name() == name:
			return p.as_dict(attrs=['pid', 'name', 'status','cpu_percent', 'memory_info','cmdline'])
	return None

# {'pid': 538, 'name': 'ffmpeg', 'status': 'sleeping'}
# {'pid': 538, 'name': 'ffmpeg', 'status': 'disk-sleep'}
def procs_info(name="ffmpeg"):
	"""
	进程信息
	:param name:
	:return: process_info
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
	for idx in range(0,len(ignore_msgs)):
		keyword = ignore_msgs[idx]
		if msg.find(keyword) != -1:
			return {"index":idx,"key":keyword}
	return None

def fifo_msg(queue_obj,msg):
	if queue_obj.qsize()< MAX_MSG_NUM:
		queue_obj.put(msg)
	else:
		queue_obj.get()
		queue_obj.put(msg)
	return queue_obj

if __name__ == '__main__':
	OutputShell('ls -l',True)
