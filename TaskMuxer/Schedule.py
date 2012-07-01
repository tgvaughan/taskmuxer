from ToDoList import ToDoList
from Timer import Timer
import random

class Schedule:

	tdl = None
	taskList = []

	timer = None

	def __init__(self, fname):

		self.tdl = ToDoList(fname)
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
		return int((3600-self.timer.getElapsed()%3600)/60)

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

