import BaseHTTPServer

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	usage = """<html>
<body>
<h1>MuxMe v0.1</h1>
<table border="1">
<tr><th>Command</th><th>Description</th></tr>
<tr><td>task</td><td>Get current task</td></tr>
<tr><td>time</td><td>Get time remaining on current task</td></tr>
<tr><td>ispaused</td><td>Check state of task timer</td></tr>
<tr><td>status</td><td>Status of current task</td></tr>
<tr><td>tasklist</td><td>List of tasks in queue</td></tr>
<tr><td>next</td><td>Mark complete + move to next task</td></tr>
<tr><td>pause</td><td>Pause task timer</td></tr>
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
				self.wfile.write(task + '\n')
			return

		if self.path=='/time':
			self.write_headers()
			self.wfile.write('{:d}\n'.format(schedule.getTimeRemaining()))
			return

		if self.path=='/ispaused':
			self.write_headers()
			self.wfile.write(str(schedule.isPaused()) + '\n')
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
				statStr += '({:d} min)\n'.format(schedule.getTimeRemaining())

			self.write_headers()
			self.wfile.write(statStr)
			return

		if self.path=='/tasklist':
			self.write_headers()
			self.wfile.write('<html><body>\n');
			self.wfile.write('<h2>Current task list</h2>\n')
			self.wfile.write('<ol>\n')
			for task in schedule.taskList:
				if task == schedule.getCurrentTask():
					self.wfile.write('<li><b>'+task+'</b>')
					self.wfile.write(' (remaining: ')
					self.wfile.write(str(schedule.getTimeRemaining()))
					self.wfile.write('min)</li>\n')
				else:
					self.wfile.write('<li>' + task + '</li>\n')
			self.wfile.write('</ol>\n')
			self.wfile.write('</body></html>\n')
			return

		if self.path=='/next':
			schedule.markDone()
			self.write_headers()
			self.wfile.write('done.\n')
			return

		if self.path=='/pause':
			schedule.pauseTimer()
			self.write_headers()
			if schedule.isPaused():
				self.wfile.write('Timer paused.\n')
			else:
				self.wfile.write('Timer unpaused.\n')
			return

		if self.path=='/reload':
			schedule.rereadTDL()
			self.write_headers()
			self.wfile.write('done.\n')
			return

		if self.path=='/shuffle':
			schedule.shuffle()
			self.write_headers()
			self.wfile.write('done.\n')
			return

		if self.path=='/help' or self.path=='/':
			self.write_headers()
			self.wfile.write(self.usage)
			return

		self.send_error(404, "Invalid command. See /help for instructions")
