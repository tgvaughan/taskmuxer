class ToDoList:

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

