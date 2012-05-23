#!/usr/bin/env python

from MuxMe import Schedule
from MuxMe import RequestHandler
from sys import argv,exit
import BaseHTTPServer

if len(argv) < 2:
	print "Usage: {} todo.txt [port]".format(argv[0])
	exit(0)
	
if len(argv) >2:
	port = int(argv[2])
else:
	port = 9999
	
# Create schedule and add to RequestHandler's global namespace:
RequestHandler.schedule = Schedule.Schedule(argv[1])
	
# Fire up server:
server = BaseHTTPServer.HTTPServer(("localhost",port), RequestHandler.RequestHandler)
server.serve_forever()
