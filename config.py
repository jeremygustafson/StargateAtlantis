# Configuration for Stargate Atlantis
# The top part of this file has values you may wish (or need) to change.
# At a minimum, you'll need to edit the LED ranges further below to match what is physically in your build.

# Import needed libraries. Do not edit this next line:
from rpi_ws281x import PixelStrip, Color


# Begin user-editable values


# Play the SGA theme after dialing the gate, before closing the wormhole
play_theme = 0


# How many seconds the wormhole should stay open after dialing (only used if play_theme is set to 0)
wormhole_duration = 7


# LED ranges
# Starting from the PCB's LED Data-Out, count the number of LEDs in each section and enter the starting and ending numbers. The first LED is 0. The ending number is actually the last LED+1.
leds = {
	# The third argument in each range() is an optional "step" value, indicating how much to increment when counting.
	# In the case of the chevrons we specify 3, since we want each set of 3 LEDs to light simultaneously as if they were one.
	'chevrons' : range(0, 27, 3), # 9*3 = 27 LEDs
	'symbols'  : range(27, 63), # 36 LEDs
	'wormhole' : range(63, 124), # 61 LEDs
	'stairs'   : list((
					range(124, 135), # Stair 1: 11 LEDs
					range(135, 143), # Stair 2: 8 LEDs
					range(143, 151), # Stair 3: 8 LEDs
					range(151, 159), # Stair 4: 8 LEDs
					range(159, 166), # Stair 5: 7 LEDs
					range(166, 173), # Stair 6: 7 LEDs
					range(173, 179), # Stair 7: 6 LEDs
					range(179, 184) # Stair 8: 5 LEDs
				)),
	'right_top_stairs' : range(184, 186), # 2 LEDs
	'right_side_panel' : range(186, 190), # 4 LEDs
	'left_top_stairs'  : range(190, 192), # 2 LEDs
	'left_side_panel'  : range(192, 196), # 4 LEDs
	'rear_window'      : range(196, 211) # 15 LEDs
}
total_number_LEDs = 211


# LED brightness settings
# Choose how bright each section of LEDs should be (on a scale of 0-255)
# For LED longevity, I suggest keeping maximum brightness below 80% (204).
brightness_chevron      = 204
brightness_symbol       = 224
brightness_wormhole_max = 204
brightness_wormhole_min = 129
brightness_stair        = 128
brightness_side_1       = 129
brightness_side_2       = 204
brightness_side_3       = 204
brightness_rear_window  = 204
brightness_rear_window_half = round(brightness_rear_window / 2)


# Milliseconds between lighting up individual symbols while dialing
dialing_delay_between_symbols = 100


# Color configuration
color_chevron = Color(0,0,brightness_chevron)
color_symbol = Color(brightness_symbol,brightness_symbol,brightness_symbol)
color_stair = Color(brightness_stair, brightness_stair, brightness_stair)
color_rear_window1 = Color(brightness_rear_window, brightness_rear_window_half, 0)
color_rear_window2 = Color(brightness_rear_window, brightness_rear_window, 0)
color_rear_window3 = Color(brightness_rear_window, 0, brightness_rear_window)
color_rear_window4 = Color(0,0,brightness_rear_window)
color_side_panel = Color(brightness_side_1, brightness_side_2, brightness_side_3)
color_off = Color(0,0,0)


# Variables to control the wormhole animation.
# Each LED will change its brightness/color every wormhole_led_sleep ms, incrementing or decrementing
# by a random value between speed_max and speed_min. The longer the sleep, then the faster the speed
# should be.
wormhole_led_speed_max = 15
wormhole_led_speed_min = 3
wormhole_led_sleep = 10


# I'm not going to lie, this next bit gets complicated. There might be an easier way, but this seems to work.
# The "real" Atlantis gate is purely digital, but that's difficult/impossible to represent in a 3D printed model
# (without the use of 36 miniature LCD panels). So instead, we need to map each LED to the physically-printed symbol
# in that spot, and furthermore map this against the official symbol filenames, as published by
# https://stargate.fandom.com/wiki/Glyph#Pegasus (to further complicate things, note that I'm mapping
# by the FILENAME, and NOT by the "position" listed on that wiki table).
# If you've assembled Glitch's model with sga_gate_front_1_cw.stl being at the top of the gate
# and working clockwise (so, sga_gate_front_2_cw.stl is attached to the right of sga_gate_front_1_cw.stl,
# and so on), then you won't need to edit this. If you used a different order, or if sga_gate_front_1_cw.stl
# is *not* at the top of your gate, then you WILL need to edit this.
# Caveat: my first physical LED in the symbols strand is actually the second symbol on sga_gate_front_6_cw.stl
# at the bottom of the gate, to the left of the opening at the bottom of the gate. Depending how you assembled
# your model you might have the first LED as the very bottom one / the first symbol on sga_gate_front_6_cw.stl.
# In that case, move the number "1" from the end of the symbol_values_as_list list to the beginning of the list.
# (and my apologies for any confusion my weird choice to use the left-of-bottom as my first LED may have caused!)

# These are the symbol filename numbers as defined from https://stargate.fandom.com/wiki/Glyph#Pegasus
# Starting from the 6 o'clock position, second symbol on sga_gate_front_6_cw.stl, going clockwise.
symbol_values_as_list = [
	23, 7,  30,     # sga_gate_front_6_cw.stl
	25, 13, 21, 18, # sga_gate_front_7_cw.stl
	8,  10, 15, 5,  # sga_gate_front_8_cw.stl
	34, 2,  28, 33, # sga_gate_front_9_cw.stl
	20, 11, 31, 12, # sga_gate_front_1_cw.stl
	3,  24, 22, 27, # sga_gate_front_2_cw.stl
	19, 26, 36, 4,  # sga_gate_front_3_cw.stl
	16, 17, 9,  29, # sga_gate_front_4_cw.stl
	35, 14, 32, 6,  # sga_gate_front_5_cw.stl
	1 # first one from sga_gate_front_6_cw.stl
	]

# This next variable is only used by the AnimClock.py script. Depending how you wired your symbols,
# your value might be 17 or 18 (zero-based). Count the number of symbols from the beginning of your
# symbols strand until you're at noon-o'clock, then subtract 1 because this is 0-based.
topmost_physical_symbol = 17



# Below are settings you shouldn't need to change
# Do not edit any lines below this point.


# Save the symbol and chevron LEDs into lists
symbol_leds_as_list = list(leds['symbols'])
chevrons_as_list = list(leds['chevrons'])

num_symbols = 36
num_chevrons = 9

# Order Chevrons will light up when dialing
chevron_light_order = [5, 6, 7, 1, 2, 3, 0, 8, 4]

# Time between playback request, and actual playback
audio_delay_time = 0.2

# Amount of time in seconds that the chevron will remain locked
chevron_engage_time = 1.5 - audio_delay_time

# LED strip configuration:
LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_MAX_BRIGHTNESS = 224 # Default 255
