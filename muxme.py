#!/usr/bin/env python

import time
import random
from sys import argv,exit
import os
import BaseHTTPServer

class TDL:

	fname = None
	data = {}

	def __init__(self, fname):
		self.fname = fname
		self.readTDL()
		self.getTaskList()

	def readTDL(self):

		lines = open(self.fname).readlines()

		self.data = {}
		group = None

		for line in lines:
			line = line.rstrip()

			if len(line) == 0:
				group = None;
				continue

			if line[0] == '#':
				continue

			if group == None:
				group = line
				self.data[group] = []
			else:
				self.data[group].append(line.lstrip())

	def getTaskList(self):
		
		taskList = []
		for group in self.data.keys():
			if len(self.data[group])>0:
				taskList.append(self.data[group][0])
			else:
				taskList.append(group)

		return taskList


class Schedule:

	tdl = None
	taskList = []

	timer = None

	def __init__(self, fname):

		self.tdl = TDL(fname)
		self.taskList = self.tdl.getTaskList()

		random.shuffle(self.taskList)
		self.timer = Timer()
	
	def rereadTDL(self):

		currentTask = self.getCurrentTask()
		self.tdl.readTDL()
		self.taskList = self.tdl.getTaskList()
		random.shuffle(self.taskList)

		if currentTask in self.taskList:
			self.taskList.remove(currentTask)
			self.taskList.append(currentTask)
			self.taskList.reverse()
		else:
			self.timer.reset()
	
	def getCurrentTask(self):
		if len(self.taskList)==0:
			return None

		idx = (int(self.timer.getElapsed())/3600)%len(self.taskList)
		return self.taskList[idx]

	def getTimeRemaining(self):
		return 3600-self.timer.getElapsed()%3600

	def markDone(self):
		if len(self.taskList)==0:
			return

		idx = int(self.timer.getElapsed()/3600)%len(self.taskList)
		self.taskList.pop(idx)
	
	def pauseTimer(self):
		self.timer.pause()
	
	def isPaused(self):
		return self.timer.paused

	def shuffle(self):
		random.shuffle(self.taskList)


class Timer:

	elapsed = 0
	unpauseTime = 0
	paused = False

	def __init__(self):
		self.elapsed = 0
		self.paused = False
		self.unpauseTime = time.time()
	
	def timeSinceUnpaused(self):
		return time.time() - self.unpauseTime
	
	def pause(self):
		if not self.paused:
			self.paused = True
			self.elapsed += self.timeSinceUnpaused()
		else:
			self.paused = False
			self.unpauseTime = time.time()
	
	def getElapsed(self):
		if not self.paused:
			return self.elapsed + self.timeSinceUnpaused()
		else:
			return self.elapsed

	def reset(self):
		self.elapsed = 0
		self.pause = False
		self.unpauseTime = time.time()



class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	usage = """<html>
<body>
<h1>MuxMe v0.1</h1>
<table border="1">
<tr><th>Command</th><th>Description</th></tr>
<tr><td>task</td><td>Get current task</td></tr>
<tr><td>time</td><td>Get time remaining on current task</td></tr>
<tr><td>next</td><td>Mark complete + move to next task</td></tr>
<tr><td>pause</td><td>Pause task timer</td></tr>
<tr><td>ispaused</td><td>Check state of task timer</td></tr>
<tr><td>status</td><td>Print status summary</td></tr>
<tr><td>reload</td><td>Re-read to-do list</td></tr>
<tr><td>shuffle</td><td>Re-shuffle task list</td></tr>
<tr><td>help</td><td>Print this help message</td></tr>
</table>
</body>
"""
	def log_message(*args):
		"""Turn off logging of server messages."""
		return

	def write_headers(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_GET(self):

		if self.path=='/task':
			self.write_headers()
			task = schedule.getCurrentTask()
			if task == None:
				self.wfile.write('None\n')
			else:
				self.wfile.write(task)
			return

		if self.path=='/time':
			self.write_headers()
			self.wfile.write('{:d}\n'.format(int(schedule.getTimeRemaining())/60))
			return

		if self.path=='/next':
			schedule.markDone()
			self.write_headers()
			self.write('done.')
			return

		if self.path=='/pause':
			schedule.pauseTimer()
			self.write_headers()
			self.write('done.')
			return

		if self.path=='/ispaused':
			self.write_headers()
			self.wfile.write('{}\n'.format(str(schedule.isPaused())))
			return

		if self.path=='/status':
			statStr = ''
			task = schedule.getCurrentTask()
			if task == None:
				statStr += 'None '
			else:
				statStr += task + ' '

			if schedule.isPaused():
				statStr += '[PAUSED]\n'
			else:
				statStr += '({:d} min)\n'.format(int(schedule.getTimeRemaining())/60)

			self.write_headers()
			self.wfile.write(statStr)
			return

		if self.path=='/reload':
			schedule.rereadTDL()
			self.write_headers()
			self.write('done.')
			return

		if self.path=='/shuffle':
			schedule.shuffle()
			self.write_headers()
			self.write('done.')
			return

		if self.path=='/help' or self.path=='/':
			self.write_headers()
			self.wfile.write(self.usage)
			return

		self.send_error(404, "File not found")

### MAIN ###
if __name__ == '__main__':

	if len(argv) < 2:
		print "Usage: {} todo.txt [port]".format(argv[0])
		exit(0)
	
	if len(argv) >2:
		port = int(argv[2])
	else:
		port = 9999
	
	# Create schedule:
	schedule = Schedule(argv[1])
	
	# Fire up server:
	server = BaseHTTPServer.HTTPServer(("localhost",port), RequestHandler)
	server.serve_forever()
