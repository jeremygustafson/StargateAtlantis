from LightingControl import LightingControl
from time import sleep
import config


class DialProgram:
	is_dialing = False

	def __init__(self, light_control, audio):
		self.light_control = light_control
		self.audio = audio

	def dial(self, address):
		length = len(address);
		if (length < 7) or (length > 9):
			raise ValueError('Address length must be 7, 8, or 9')

		DialProgram.is_dialing = True
		self.light_control.all_off()
		self.light_control.stay_lit_physical_symbols = [] # Run this both before and after dialing

		direction = self.light_control.FORWARD
		for i, symbol in enumerate(address):
			self.audio.play_roll()
			sleep(config.audio_delay_time)
			self.light_control.move_to_numeric_symbol(symbol, direction, skipSymbolOnFirstPassIfClose=True)
			self.audio.stop_roll()

			self.audio.play_chevron_lock()
			sleep(config.audio_delay_time)
			
			# If dialing a 7- or 8-symbol address, light up the top chevron for the final symbol
			if i == length-1:
				self.light_control.light_chevron(config.chevron_light_order[-1])
			else:
				self.light_control.light_chevron(config.chevron_light_order[i])
			
			while self.audio.is_playing():
				sleep(0.01)
				continue
			if i == length-1:
				break

			if direction == self.light_control.FORWARD:
				direction = self.light_control.BACKWARD
			else:
				direction = self.light_control.FORWARD

		self.audio.play_open()
		self.light_control.light_all_chevrons(show=False)
		self.light_control.light_side_panels()
		self.light_control.activate_wormhole(duration=90)
		self.light_control.light_rear_window()
		self.light_control.light_all_stairs(delay=100)
		while self.audio.is_playing():
			sleep(0.1)
			continue

		if config.play_theme:
			self.audio.play_theme()
			
		while self.audio.is_playing():
			sleep(0.1)
			continue

		self.audio.play_close()
		self.light_control.deactivate_wormhole()
		self.light_control.light_all_stairs(delay=100, color=config.color_off)
		self.light_control.all_off()
		DialProgram.is_dialing = False
		self.light_control.stay_lit_physical_symbols = []
