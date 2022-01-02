# Useful links:
# https://docs.python.org/3/library/http.server.html
# https://stackoverflow.com/a/46332163

# Note that "self.end_headers()" is required after send_response() as of Python 3.3

import os
import json
from http.server import SimpleHTTPRequestHandler
from DialProgram import DialProgram

class StargateHttpHandler(SimpleHTTPRequestHandler):
	def translate_path(self, path):
		path = SimpleHTTPRequestHandler.translate_path(self, path)
		relpath = os.path.relpath(path, os.getcwd())
		fullpath = os.path.join('web', relpath)
		return fullpath

	def do_POST(self):
		# For debugging:
		# print('POST: {}'.format(self.path))
		if self.path == '/shutdown':
			os.system('systemctl poweroff')
			self.send_response(200, 'OK')
			self.end_headers()
			return

		if self.path == '/reboot':
			os.system('systemctl reboot')
			self.send_response(200, 'OK')
			self.end_headers()
			return
		
		# https://unix.stackexchange.com/questions/21089/how-to-use-command-line-to-change-volume
		if self.path == '/volumeup':
			os.system('amixer set PCM 5%+')
			self.send_response(200, 'OK')
			self.end_headers()
			return

		if self.path == '/volumedown':
			os.system('amixer set PCM 5%-')
			self.send_response(200, 'OK')
			self.end_headers()
			return

		if self.path == '/dialstatus':
			if DialProgram.is_dialing:
				self.send_response(200, '1')
				self.end_headers()
			else:
				self.send_response(204, '0')
				self.end_headers()
			return

		if self.path != '/update':
			self.send_error(404)
			self.end_headers()
			return

		content_len = int(self.headers.get('content-length', 0))
		body = self.rfile.read(content_len)
		data = json.loads(body)
		# For debugging
		# print('POST data: {}'.format(data))
		StargateHttpHandler.logic.execute_command(data)
		self.send_response(200, 'OK')
		self.end_headers()
