from AnimChase import AnimChase
from AnimRing import AnimRing
from AnimClock import AnimClock
from time import sleep
import config
from rpi_ws281x import PixelStrip, Color

# self.state values:
# 0: animation chase
# 1: animation ring
# 2: dial
# 3: animation clock
# 4: testing/debug
# 5: all lights off
# 6: do nothing

STATE_ANIMATION_CHASE = 0
STATE_ANIMATION_RING = 1
STATE_DIALING = 2
STATE_ANIMATION_CLOCK = 3
STATE_TESTING_DEBUG = 4 # If changed here, it also must be changed in testing.htm
STATE_ALL_LIGHTS_OFF = 5
STATE_DO_NOTHING = 6


class StargateLogic:
	def __init__(self, audio, light_control, dial_program):
		self.audio = audio
		self.light_control = light_control
		self.dial_program = dial_program
		self.anim_chase = AnimChase(light_control)
		self.anim_ring = AnimRing(light_control)
		self.anim_clock = AnimClock(light_control)
		self.state = STATE_ALL_LIGHTS_OFF
		self.address = []
		self.state_changed = True
	
	
	# Destructor
	def __del__(self):
		return
	
	
	def execute_command(self, command):
		self.state_changed = True
		self.state = command['anim']

		if self.state == STATE_DIALING:
			address = command['sequence']
			#if len(address) != 7:
			if len(address) < 7:
				self.state = STATE_ALL_LIGHTS_OFF
				return
			self.address = address
		
		elif self.state == STATE_TESTING_DEBUG:
			self.state = STATE_DO_NOTHING
			action = command['action']
			
			if action == "spinBackward":
				self.light_control.stay_lit_physical_symbols.clear()
				self.light_control.move_to_physical_symbol(self.light_control.current_physical_symbol - 1, self.light_control.BACKWARD)
			
			elif action == "spinForward":
				self.light_control.stay_lit_physical_symbols.clear()
				self.light_control.move_to_physical_symbol(self.light_control.current_physical_symbol + 1, self.light_control.FORWARD)
			
			elif action == "spinForwardToNumericSymbol":
				self.light_control.move_to_numeric_symbol(command['symbol'], self.light_control.FORWARD)
			
			elif action == "spinBackwardToNumericSymbol":
				self.light_control.move_to_numeric_symbol(command['symbol'], self.light_control.BACKWARD)
			
			elif action == "spinForwardToPhysicalSymbol":
				self.light_control.move_to_physical_symbol(command['symbol'], self.light_control.FORWARD)
			
			elif action == "spinBackwardToPhysicalSymbol":
				self.light_control.move_to_physical_symbol(command['symbol'], self.light_control.BACKWARD)
			
			elif action == "wormholeOn":
				self.light_control.activate_wormhole(duration=60)
			
			elif action == "wormholeOff":
				self.light_control.deactivate_wormhole()
			
			elif action == "strandTest":
				self.light_control.do_strandtest()
				
			elif action == "allLightsOn":
				self.light_control.all_on()
				
			elif action == "allLightsOff":
				self.light_control.all_off()
			
			elif action == "chevronsOn":
				self.light_control.light_all_chevrons()
			
			elif action == "chevronsOff":
				self.light_control.light_all_chevrons(color=config.color_off)
			
			elif action == "individualLEDOn":
				self.light_control.light_LED(command['led'])
			
			elif action == "individualLEDOff":
				self.light_control.light_LED(command['led'], config.color_off)
				
			elif action == "symbolsOn":
				self.light_control.stay_lit_physical_symbols.clear()
				self.light_control.light_all_symbols()
			
			elif action == "symbolsOff":
				self.light_control.stay_lit_physical_symbols.clear()
				self.light_control.light_all_symbols(0, config.color_off)
			
			elif action == "stairsOn":
				self.light_control.light_all_stairs(50)
			
			elif action == "stairsOff":
				self.light_control.light_all_stairs(50, config.color_off)
			
			elif action == "rightStairsOn":
				self.light_control.light_right_side_panel(show=False)
				self.light_control.light_right_top_stairs()
			
			elif action == "rightStairsOff":
				self.light_control.light_right_side_panel(color=config.color_off, show=False)
				self.light_control.light_right_top_stairs(color=config.color_off)
			
			elif action == "leftStairsOn":
				self.light_control.light_left_side_panel(show=False)
				self.light_control.light_left_top_stairs()
			
			elif action == "leftStairsOff":
				self.light_control.light_left_side_panel(color=config.color_off, show=False)
				self.light_control.light_left_top_stairs(color=config.color_off)
			
			elif action == "rearWindowOn":
				self.light_control.light_rear_window()
			
			elif action == "rearWindowOff":
				self.light_control.darken_rear_window()
				
			elif action == "chevron0":
				self.light_control.light_chevron(0)
			
			elif action == "chevron1":
				self.light_control.light_chevron(1)
			
			elif action == "chevron2":
				self.light_control.light_chevron(2)
			
			elif action == "chevron3":
				self.light_control.light_chevron(3)
			
			elif action == "chevron4":
				self.light_control.light_chevron(4)
			
			elif action == "chevron5":
				self.light_control.light_chevron(5)
			
			elif action == "chevron6":
				self.light_control.light_chevron(6)
			
			elif action == "chevron7":
				self.light_control.light_chevron(7)
			
			elif action == "chevron8":
				self.light_control.light_chevron(8)


	def loop(self):
		while True:
			state_changed = self.state_changed
			self.state_changed = False

			# Call relevant logic depending on state
			if self.state == STATE_DIALING:
				self.light_control.all_off()
				self.dial_program.dial(self.address)
				self.state = STATE_ALL_LIGHTS_OFF
			elif self.state == STATE_ANIMATION_CHASE:
				delay = self.anim_chase.animate(state_changed)
				sleep(delay)
			elif self.state == STATE_ANIMATION_RING:
				delay = self.anim_ring.animate(state_changed)
				sleep(delay)
			elif self.state == STATE_ANIMATION_CLOCK:
				delay = self.anim_clock.animate(state_changed)
				sleep(delay)
			elif self.state == STATE_ALL_LIGHTS_OFF:
				self.light_control.all_off()
				sleep(1)
			else:
				sleep(1)
