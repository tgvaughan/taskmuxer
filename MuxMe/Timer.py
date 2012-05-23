import time

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

