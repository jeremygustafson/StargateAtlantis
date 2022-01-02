#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
# With some threading-friendly edits by Jeremy Gustafson
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import PixelStrip, Color


# Used to cancel animations mid-stride
stopAnimation = False


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms / 1000.0)
		if stopAnimation:
			return


def colorWipeInstant(strip, color):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()


def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i + q, color)
			strip.show()
			time.sleep(wait_ms / 1000.0)
			if stopAnimation:
				return
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i + q, 0)


def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256 * iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i + j) & 255))
		strip.show()
		time.sleep(wait_ms / 1000.0)
		if stopAnimation:
			return


def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256 * iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(
				(int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms / 1000.0)
		if stopAnimation:
			return


def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i + q, wheel((i + j) % 255))
			strip.show()
			time.sleep(wait_ms / 1000.0)
			if stopAnimation:
				return
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i + q, 0)
