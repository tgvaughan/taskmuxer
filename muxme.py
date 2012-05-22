#!/usr/bin/env python

import time
import random
from sys import argv,exit
import os
import SocketServer

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



class SchedTCPHandler(SocketServer.StreamRequestHandler):

	usage = """Command		Description
--------------------------------------------------
task		Get current task
time		Get time remaining on current task
next		Mark complete + move to next task
pause		Pause task timer
ispaused	Check state of task timer
status		Print status summary
reload		Re-read to-do list
shuffle		Re-shuffle task list
help		Print this help message
"""

	def handle(self):
		cmd = self.rfile.readline().strip().lower()

		if cmd=='task':
			task = schedule.getCurrentTask()
			if task == None:
				self.wfile.write('None\n')
			else:
				self.wfile.write(task)
			return

		if cmd=='time':
			self.wfile.write('{:d}\n'.format(int(schedule.getTimeRemaining())/60))
			return

		if cmd=='next':
			schedule.markDone()
			return

		if cmd=='pause':
			schedule.pauseTimer()
			return

		if cmd=='ispaused':
			self.wfile.write('{}\n'.format(str(schedule.isPaused())))
			return

		if cmd=='status':
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

			self.wfile.write(statStr)
			return

		if cmd=='reload':
			schedule.rereadTDL()
			return

		if cmd=='shuffle':
			schedule.shuffle()
			return

		if cmd=='help':
			self.wfile.write(self.usage)
			return

### MAIN ###
if __name__ == '__main__':

	if len(argv) < 2:
		print "Usage: {} schedule_file.txt [port]".format(argv[0])
		exit(0)
	
	if len(argv) >2:
		port = int(argv[2])
	else:
		port = 9999
	
	# Create schedule:
	schedule = Schedule(argv[1])
	
	# Fire up server:
	server = SocketServer.TCPServer(("localhost",port), SchedTCPHandler)
	server.serve_forever()
