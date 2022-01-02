# Stargate Atlantis Troubleshooting Notes

These are some troubleshooting notes I kept while building my gate. If you run into issues, hopefully something in here will be helpful.


--------------------
## Issue: Not hearing any sound after installing sound software

**Possible resolution:**

Re-run the Adafruit installer script, but disable /dev/zero playback when prompted.





--------------------
## Issue: Speaker repeatedly plays a low-quality recording saying "To install the screenreader, press control-alt-space."

After rebooting, my Pi started repeating (every minute or so) a poor quality recording that said "To install the screenreader, press control-alt-space." Apparently this is due to the headless setup (described in the README).

**To resolve:**

```
sudo rm /etc/xdg/autostart/piwiz.desktop
sudo reboot
```





--------------------
## Issue: Some of the "sudo apt install" commands fail

When installing packages via "sudo apt install", I saw the following error messages:

```
Err:1 http://raspbian.raspberrypi.org/raspbian buster/main armhf libtiffxx5 armhf 4.1.0+git191117-2~deb10u2
  404  Not Found [IP: 93.93.128.193 80]
Err:2 http://raspbian.raspberrypi.org/raspbian buster/main armhf libtiff-dev armhf 4.1.0+git191117-2~deb10u2
  404  Not Found [IP: 93.93.128.193 80]
E: Failed to fetch http://raspbian.raspberrypi.org/raspbian/pool/main/t/tiff/libtiffxx5_4.1.0+git191117-2~deb10u2_armhf.deb  404  Not Found [IP: 93.93.128.193 80]
E: Failed to fetch http://raspbian.raspberrypi.org/raspbian/pool/main/t/tiff/libtiff-dev_4.1.0+git191117-2~deb10u2_armhf.deb  404  Not Found [IP: 93.93.128.193 80]
E: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
```

**To resolve:**

Re-run the "apt-get update/upgrade" commands:

```
sudo apt-get update
sudo apt-get upgrade
sudo apt autoremove
```

Then retry your "sudo apt install".





--------------------
## Issue: Web controls only accessible by IP address, but not http://atlantispi.local/

After setting up my Pi and installing the Stargate code, I could only access the web page control panel by my Pi's local 10-dot IP address, but not "http://atlantispi.local/".

**To resolve:**

Install the apache2 software (including the "disable" and "stop" commands) as explained in the README.





--------------------
## Issue: When refreshing the web page, it fails to load every-other time

**To resolve:**

In the WebServer.py file, make sure any `print()` commands are commented out. For reasons I don't understand, printing anything from inside the `do_POST(self)` function causes the web server thread only to respond to every-other request.

```
    def do_POST(self):
        # For debugging:
        # print('POST: {}'.format(self.path))
        ...
```





--------------------
## Issue: LEDs cycle colors then turn all white

**To resolve:**

Add the `core_freq` and `core_freq_min` values to your `/boot/config.txt`:

```
sudo vi /boot/config.txt
# For LEDs over SPI
# https://github.com/jgarff/rpi_ws281x/issues/381#issuecomment-629495220
# https://github.com/jgarff/rpi_ws281x/issues/194
core_freq=400
core_freq_min=400
```

Then reboot your Pi.

```sudo reboot```





--------------------
## Issue: LEDs light up but occasionally flash/blink

**To resolve:**

Add a 300-500 Ohm resistor (I used 470) on the data line before your first LED. (this is marked on my PCB but you don't need to use my PCB)





--------------------
## Issue: "Disco Party" (LEDs spazzing out and flashing random colors)
or
## Issue: None of my LEDs are lighting up!

As obvious as it sounds, check to make sure your connections haven't come loose, either where the jumper wires plug in together, or the solder points on the PCBs/LEDs. Even if you think the connections are secure, check them anyway. More than once I wasted a lot of time troubleshooting what I was *sure* was a software issue, only to discover a wire that looked like it was solidly connected, wasn't.

If all your connections are solid, next check that none of your 5V and Ground connections are reversed, and that you have a continuous flow of Data-Out to Data-In throughout the entire string of LEDs. Keeping track of the pin directions ends up being trickier than it feels like it should be.

Typically when I had a disco dance party happen, it was because one of my ground wires had come loose from a PCB.

It's also possible an LED might be bad in the middle of a PCB. I did have one or two LEDs on the staircase PCBs come loose from their solder pads while I was cutting the PCBs apart. In that case you can either re-solder/replace the individual LED or replace the whole PCB with a spare. If you do add solder for an individual LED on a PCB, be quick about it and use minimal heat - the LEDs melt very easily.

Lastly, I'm convinced that sometimes an LED might just be "bad" straight out of manufacturing. I spent hours troubleshooting another dance party and I'm pretty sure I ended up fixing it just by replacing two individual LEDs in the middle of my strand. It's worth noting that the dance party always will be either at or "downstream" of the bad connection/solder point/LED.





--------------------
## Issue: When lighting up a section of LEDs, such as the left side panel of the staircase, one LED inexplicably flashes on then off, and remains off while all the other LEDs in that section remain on

I cannot claim to fully understand the root cause of this, but I do have a possible solution/workaround.

I had an issue where when I turned on the left side panel of the staircase (either individually, or by calling the `all_on()` function), the topmost LED would flash on for a split second, then turn off, while all the other LEDs remained on. If I turned the LED on by itself, it stayed on. If I did a strand test, the LED worked fine. If I coded it to turn red, green, or blue, it worked fine. If I turned the side on followed by turning on the wormhole, for instance, the single LED would flicker as if it was being told both to turn on and off at the same time.  I'm pretty sure at one point I replaced the LED, though I'm not 100% sure so I can't completely rule out a hardware issue. In any case, it was baffling.

After many hours of troubleshooting and experimenting, I eventually tried setting the 4 LEDs in that side panel to a different color, and the top LED stayed on. So, for reasons I don't understand, that particular LED (#192 on my strand) simply can't be set to `Color(128,128,128)`. It appears it can be set to almost anything else, just not that particular color. Whether that's because it's a defective LED, bad wiring/soldering, or perhaps there's some weirdly specific bug in the rpi_ws281x python library regarding LED #192 in a strand, or for some other reason, I don't know. But the workaround if you're experiencing a similar issue may be as simple as "choose a different color."

(and if you're wondering why I didn't see the issue when turning the LED on individually, it's because my `light_LED()` function defaults to the blue chevron color instead of the `brightness_side` color; when I manually coded the LED to turn on with `Color(128,128,128)`, it flashed and went out.)





--------------------
## Issue: When dialing, the symbols that light up are are off by one from what I dialed

**To resolve:**

Double check your `symbol_leds_as_list` variable in config.py, you may need to move the "1" from the end of the list to the beginning. Read the full comments above `symbol_leds_as_list` in config.py for more details.