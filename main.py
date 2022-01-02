#!/usr/bin/env python3

# Working Stargate Atlantis by Glitch
# Code by Jeremy Gustafson (based on code by Dan Clarke created for Working Stargate Mk2)

#
# *** DON'T FORGET TO EDIT CONFIG.PY ***
#

import daemon, sys, threading, time, traceback
from rpi_ws281x import PixelStrip, Color
import config

from LightingControl import LightingControl
from DialProgram import DialProgram
from StargateAudio import StargateAudio
from StargateLogic import StargateLogic
from WebServer import StargateHttpHandler
from http.server import HTTPServer


# Stargate components
audio = StargateAudio()
light_control = LightingControl()
dial_program = DialProgram(light_control, audio)
logic = StargateLogic(audio, light_control, dial_program)


# Web control
print('Running web server...')
StargateHttpHandler.logic = logic
httpd = HTTPServer(('', 80), StargateHttpHandler)

httpd_thread = threading.Thread(name="HTTP", target=httpd.serve_forever)
httpd_thread.daemon = True
httpd_thread.start()


# Infinite loop
print('Running logic...')
try:
	logic.loop()
	
except KeyboardInterrupt:
	print(" ^C entered, stopping Stargate program...")
	httpd.socket.close()
	light_control.all_off()
	
except Exception as e:
	print(e)
	print(traceback.format_exc())
	print("Caught exception. Exiting gracefully")
	httpd.socket.close()
	light_control.all_off()
	exit(1)