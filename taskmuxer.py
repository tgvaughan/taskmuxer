#!/usr/bin/env python

from TaskMuxer import Schedule
from TaskMuxer import RequestHandler
from sys import argv,exit
import BaseHTTPServer
import argparse

parser = argparse.ArgumentParser(description="Personal task multiplexer.")
parser.add_argument("-p", dest="port", type=int, default=9999, help="TCP port for web server to listen on.")
parser.add_argument("todo", metavar="todo.txt", help="File containing to-do list.")

if len(argv) < 2:
	parser.print_help()
	exit(0)

args = parser.parse_args(argv[1:])

# Create schedule and add to RequestHandler's global namespace:
RequestHandler.schedule = Schedule.Schedule(argv[1])

# Fire up server:
server = BaseHTTPServer.HTTPServer(("localhost", args.port), RequestHandler.RequestHandler)
server.serve_forever()
