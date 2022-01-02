import config
from gpiozero import PWMLED
import time
from rpi_ws281x import PixelStrip, Color
import strandtestfunctions
import random
import threading

class LightingControl:
	FORWARD = 1
	BACKWARD = -1

	# Constructor
	def __init__(self):
		# Set up the LED strip
		self.strip = PixelStrip(config.total_number_LEDs, config.LED_PIN, config.LED_FREQ_HZ, config.LED_DMA, config.LED_INVERT, config.LED_MAX_BRIGHTNESS, config.LED_CHANNEL)
		self.strip.begin()
		# Ensure LEDs are all initially off
		strandtestfunctions.colorWipeInstant(self.strip, config.color_off)
		
		# Variables to track which symbols are lit
		self.current_physical_symbol = 0
		self.stay_lit_physical_symbols = []
		
		# Threading variables
		self.wormhole_thread = False
		self.strandtest_thread = False
		
		# Wormhole variables
		self.closing_wormhole = False
		self.closing_wormhole_targets_set = False
		
		# Here are all the ways NOT to do this:
		#		self.active_wormhole = [*config.wormhole] # a list of all wormhole LEDs
		#		self.active_wormhole = list(config.wormhole) # a list of all wormhole LEDs
		#		self.active_wormhole = dict.fromkeys(
		#			config.wormhole,{
		#				"currentColor": [0,0,0],
		#				"targetColor": [0,0,0],
		#				"speed": 0
		#			}
		#		) # a dictionary of all wormhole LEDs

		# Here's a way that works, courtesy of
		# https://stackoverflow.com/questions/15516413/dict-fromkeys-all-point-to-same-list
		self.active_wormhole = dict((key, {
				"currentColor": [0,0,0],
				"targetColor": [0,0,0],
				"speed": 0
		}) for key in config.leds['wormhole']) # a dictionary of all wormhole LEDs		
	
	
	# Destructor
	def __del__(self):
		if self.wormhole_thread is not False:
			self.wormhole_thread.kill()
		if self.strandtest_thread is not False:
			self.strandtest_thread.kill()
		# Turn off LEDs
		strandtestfunctions.colorWipeInstant(self.strip, config.color_off)

	# Light an individual LED, mostly used for testing/debugging, but also used by AnimClock.py
	def light_LED(self, pixelID, color=config.color_chevron):
		self.strip.setPixelColor(pixelID, color)
		self.strip.show()
	
	# Move to a specific symbol on the gate, using the in-universe numeric index
	# This matches the svg filenames in web/chevrons/A__.svg
	def move_to_numeric_symbol(self, index, direction):
		#print("DEBUG: move_to_numeric_symbol: index: ", index)
		#print("DEBUG: move_to_numeric_symbol: physical symbol: ", config.symbol_values_as_list.index(index))
		self.move_to_physical_symbol( config.symbol_values_as_list.index(index) , direction)
		return
	
	# Move to a specific symbol on the gate
	def move_to_physical_symbol(self, index, direction):
		print("DEBUG: move_to_physical_symbol: index: ", index)
		#print("DEBUG: move_to_physical_symbol: self.current_physical_symbol: ", self.current_physical_symbol)
		print("DEBUG: move_to_physical_symbol: numeric symbol: ", config.symbol_values_as_list[index])
		delta = 0
		
		# Typically index will be in the range [0-35], but it's possible from the "debug / testing"
		# page that a "spin forward/backward" might give us a -1 or 36, so this corrects for that.
		while index < 0:
			index += config.num_symbols
		while index >= config.num_symbols:
			index -= config.num_symbols
		
		# First check if we're already at the right symbol
		if index == self.current_physical_symbol:
			self.strip.setPixelColor(config.symbol_leds_as_list[index], config.color_symbol)
			self.strip.show()
			return
		elif direction == self.FORWARD:
			if index >= self.current_physical_symbol:
				delta = index - self.current_physical_symbol
			else:
				delta = (config.num_symbols - self.current_physical_symbol) + index
		else:
			if index <= self.current_physical_symbol:
				delta = self.current_physical_symbol - index
			else:
				delta = self.current_physical_symbol + (config.num_symbols - index)
		
		self.stay_lit_physical_symbols.append(index)
		
		# For debugging:
		#print('Index: {}, Direction: {}, Delta: {}'.format(index, direction, delta))
		#print('stay_lit_physical_symbols: ', self.stay_lit_physical_symbols)
		
		for i in range(delta):
			if self.current_physical_symbol not in self.stay_lit_physical_symbols:
				self.strip.setPixelColor(config.symbol_leds_as_list[self.current_physical_symbol], config.color_off)
			
			if direction == self.FORWARD:
				self.current_physical_symbol += 1
				if self.current_physical_symbol >= config.num_symbols:
					self.current_physical_symbol = 0
			else:
				self.current_physical_symbol -= 1
				if self.current_physical_symbol < 0:
					self.current_physical_symbol = config.num_symbols - 1
			self.strip.setPixelColor(config.symbol_leds_as_list[self.current_physical_symbol], config.color_symbol)
			self.strip.show()
			time.sleep(config.dialing_delay_between_symbols / 1000)
	
	# Light an individual (physical) symbol on the gate
	def light_symbol(self, symbol, color=config.color_symbol, show=True):
		pixelID = config.symbol_leds_as_list[symbol]
		self.strip.setPixelColor(pixelID, color)
		if show:
			self.strip.show()
	
	# Light all 36 symbols on the gate
	def light_all_symbols(self, delay=0, color=config.color_symbol, show=True):
		for symbol in range(len(config.leds['symbols'])):
			self.light_symbol(symbol, color, show)
			time.sleep(delay / 1000)
	
	# Light one of the 9 chevrons; each chevron is 3 LEDs
	def light_chevron(self, chevron, color=config.color_chevron, show=True):
		pixelID = config.chevrons_as_list[chevron]
		self.strip.setPixelColor(pixelID, color)
		self.strip.setPixelColor(pixelID+1, color)
		self.strip.setPixelColor(pixelID+2, color)
		if show:
			self.strip.show()
	
	# Light all 9 chevrons
	def light_all_chevrons(self, color=config.color_chevron, show=True):
		for i in range(0,8):
			self.light_chevron(i, color=color, show=False)
		self.light_chevron(8, color=color, show=show)
	
	# Light all the LEDs in a single stair step
	def light_stair_step(self, step, color=config.color_stair, show=True):
		for led in config.leds['stairs'][step]:
			self.strip.setPixelColor(led, color)
		if show:
			self.strip.show()
	
	# Light all the stair steps
	def light_all_stairs(self, delay=0, color=config.color_stair, show=True):
		for step in range(len(config.leds['stairs'])):
			self.light_stair_step(step, color, show)
			time.sleep(delay / 1000)
	
	# Light the rear window
	def light_rear_window(self, color1=config.color_rear_window1, color2=config.color_rear_window2, 
						color3=config.color_rear_window3, color4=config.color_rear_window4, show=True):
		for i in range(3):
			self.strip.setPixelColor(config.leds['rear_window'][i], color1)
		for i in range(4):
			self.strip.setPixelColor(config.leds['rear_window'][i+3], color2)
		for i in range(4):
			self.strip.setPixelColor(config.leds['rear_window'][i+7], color3)
		for i in range(4):
			self.strip.setPixelColor(config.leds['rear_window'][i+11], color4)
		if show:
			self.strip.show()
	
	def darken_rear_window(self, show=True):
		for i in config.leds['rear_window']:
			self.strip.setPixelColor(i, config.color_off)
		if show:
			self.strip.show()
		
	# Light the right side panel
	def light_right_side_panel(self, color=config.color_side_panel, show=True):
		for i in config.leds['right_side_panel']:
			self.strip.setPixelColor(i, color)
			if show:
				self.strip.show()
	
	# Light the LEDs above and to the right of the staircase
	def light_right_top_stairs(self, color=config.color_side_panel, show=True):
		for i in config.leds['right_top_stairs']:
			self.strip.setPixelColor(i, color)
			if show:
				self.strip.show()
	
	# Light the left side panel
	def light_left_side_panel(self, color=config.color_side_panel, show=True):
		for i in config.leds['left_side_panel']:
			self.strip.setPixelColor(i, color)
			if show:
				self.strip.show()
	
	# Light the LEDs above and to the left of the staircase
	def light_left_top_stairs(self, color=config.color_side_panel, show=True):
		for i in config.leds['left_top_stairs']:
			self.strip.setPixelColor(i, color)
		if show:
			self.strip.show()
	
	# Light all the side panels
	def light_side_panels(self, show=True):
		self.light_right_side_panel(show=show)
		self.light_left_side_panel(show=show)
		self.light_right_top_stairs(show=show)
		self.light_left_top_stairs(show=show)
	
	def darken_side_panels(self, show=True):
		self.light_right_side_panel(color=config.color_off, show=show)
		self.light_left_side_panel(color=config.color_off, show=show)
		self.light_right_top_stairs(color=config.color_off, show=show)
		self.light_left_top_stairs(color=config.color_off, show=show)
	
	
	
	def wormhole_pick_new_color_for_single_led(self, led_index):
		# Choose a random target brightness, between brightness_wormhole_min and brightness_wormhole_max
		target = random.randrange(config.brightness_wormhole_min, config.brightness_wormhole_max)
		
		# Random choice: should target be all-white (0), all-blue (1-8), or blue-ish white (9)
		choice = random.randrange(0,10)
		
		# All white spectrum:
		if choice == 0:
			self.active_wormhole[led_index]["targetColor"] = [target, target, target]
		# Blue spectrum:
		elif choice > 0 and choice < 9:
			self.active_wormhole[led_index]["targetColor"] = [0,0,target]
		# Blue-ish white spectrum
		else:
			# A lower value than target
			if config.brightness_wormhole_min == target:
				lower_target = target
			else:
				lower_target = random.randrange(config.brightness_wormhole_min,target)
			self.active_wormhole[led_index]["targetColor"] = [lower_target,lower_target,target]
		
		# Speed: How fast should the LED change colors toward the target color
		self.active_wormhole[led_index]["speed"] = random.randrange(config.wormhole_led_speed_min, config.wormhole_led_speed_max)
	
	
	def wormhole_active(self, duration=7, animation=True, show=True):
		start_time = time.perf_counter()
		self.closing_wormhole = False
		self.closing_wormhole_targets_set = False
				
		while True:
			# Reference: led_dict = {"currentColor": [0,0,0], "targetColor": [0,0,0], "speed": 0}
			for index, led_dict in self.active_wormhole.items():
			
				# self.closing_wormhole can be set True outside of this function, so check for it at beginning of loop
				if self.closing_wormhole and not self.closing_wormhole_targets_set:
					duration = 1
					start_time = time.perf_counter()
					for led in self.active_wormhole:
						self.active_wormhole[led]["targetColor"] = [0,0,0]
					self.closing_wormhole_targets_set = True
				
				# If this LED has reached its target color, reset target to something new
				elif not self.closing_wormhole and self.active_wormhole[index]["currentColor"] == self.active_wormhole[index]["targetColor"]:
					self.wormhole_pick_new_color_for_single_led(index)
				
				# Increment the LED toward its target color
				for i in range(0,3):
					if self.active_wormhole[index]["currentColor"][i] > self.active_wormhole[index]["targetColor"][i]:
						self.active_wormhole[index]["currentColor"][i] -= self.active_wormhole[index]["speed"]
						# In case we overshot:
						if self.active_wormhole[index]["currentColor"][i] < self.active_wormhole[index]["targetColor"][i]:
							self.active_wormhole[index]["currentColor"][i] = self.active_wormhole[index]["targetColor"][i]
					
					# Now the same but in reverse:
					if self.active_wormhole[index]["currentColor"][i] < self.active_wormhole[index]["targetColor"][i]:
						self.active_wormhole[index]["currentColor"][i] += self.active_wormhole[index]["speed"]
						# In case we overshot:
						if self.active_wormhole[index]["currentColor"][i] > self.active_wormhole[index]["targetColor"][i]:
							self.active_wormhole[index]["currentColor"][i] = self.active_wormhole[index]["targetColor"][i]
				
				self.strip.setPixelColor(index, Color(
												self.active_wormhole[index]["currentColor"][0],
												self.active_wormhole[index]["currentColor"][1],
												self.active_wormhole[index]["currentColor"][2]
												)
										)

			# Used only in the case of all_on
			if show:
				self.strip.show()
			
			# If no wormhole animation requested, return now instead of looping
			if not animation:
				return
			
			# Otherwise, sleep and loop
			time.sleep(config.wormhole_led_sleep / 1000.0)
			now = time.perf_counter()
			if((now - start_time) >= duration):
				# If self.closing_wormhole wasn't set outside of this function, that means we've timed out on our own
				# Set self.closing_wormhole to True, and the next iteration through the while loop will set the
				# LED targets and new duration timeout
				self.closing_wormhole = True
				
				# If we've already been closing the wormhole and timed out again, then turn off any straggling LEDs
				if self.closing_wormhole_targets_set:
					for index, led_dict in self.active_wormhole.items():
						self.strip.setPixelColor(index, config.color_off)
					self.strip.show()
					break;
	
	def activate_wormhole(self, duration=7, animation=True, show=True):
		self.wormhole_thread = threading.Thread(target=self.wormhole_active, name="Wormhole", kwargs={'duration': duration, 'animation': animation, 'show': show})
		self.wormhole_thread.start()
	
	def deactivate_wormhole(self):
		self.closing_wormhole = True
		if self.wormhole_thread is not False:
			self.wormhole_thread.join()
	
	# Turn on ALL lighting
	def all_on(self):
		self.stay_lit_physical_symbols.clear()
		self.light_all_chevrons(show=False)
		self.light_all_symbols(show=False)
		self.light_side_panels(show=False)
		self.light_all_stairs(show=False)
		self.light_rear_window(show=False)
		self.activate_wormhole(animation=False)
		self.strip.show()
		
	# Turn off ALL lighting
	def all_off(self):
		self.closing_wormhole = True
		if self.wormhole_thread is not False:
			self.wormhole_thread.join()
		if self.strandtest_thread is not False:
			strandtestfunctions.stopAnimation = True
			#self.strandtest_thread.join() 
		self.stay_lit_physical_symbols.clear()
		strandtestfunctions.colorWipeInstant(self.strip, config.color_off)
	
	def all_off_elegant(self):
		colorWipe(self.strip, config.color_off, 10)

	def strandtest_all(self):
		strandtestfunctions.stopAnimation = False
		strandtestfunctions.colorWipe(self.strip, Color(255, 0, 0))  # Red wipe
		if not strandtestfunctions.stopAnimation:
			strandtestfunctions.colorWipe(self.strip, Color(0, 255, 0))  # Blue wipe
		if not strandtestfunctions.stopAnimation:
			strandtestfunctions.colorWipe(self.strip, Color(0, 0, 255))  # Green wipe
		if not strandtestfunctions.stopAnimation:
			strandtestfunctions.rainbow(self.strip)
		#if not strandtestfunctions.stopAnimation::
		#	strandtestfunctions.rainbowCycle(self.strip)
		self.all_off()
	
	def do_strandtest(self):
		self.strandtest_thread = threading.Thread(target=self.strandtest_all, name="Strand Test", args=[])
		self.strandtest_thread.start()