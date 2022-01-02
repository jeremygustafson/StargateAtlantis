#!/usr/bin/env python3

import config
import strandtestfunctions

# Init WS2812 LEDs
strip = PixelStrip(total_number_LEDs, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_MAX_BRIGHTNESS, LED_CHANNEL)
strip.begin()

try:
	while True:
		print('Color wipe animations.')
		colorWipe(strip, Color(255, 0, 0))  # Red wipe
		colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		colorWipe(strip, Color(0, 0, 255))  # Green wipe

		print('Rainbow animations.')
		rainbow(strip)
		rainbowCycle(strip)

except KeyboardInterrupt:
	colorWipe(strip, Color(0, 0, 0), 10)