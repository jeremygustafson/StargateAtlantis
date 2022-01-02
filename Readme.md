# Working Stargate Atlantis Control Code with Raspberry Pi

Control code for [Glitch's Working Stargate Atlantis](https://www.thingiverse.com/thing:3153542) via a web browser.

Written by [Jeremy Gustafson](https://github.com/jeremygustafson), based on the original SG-1 gate code written by [Dan Clarke](https://github.com/danclarke) for [Glitch's Working Stargate Mk2](https://www.thingiverse.com/thing:1603423).

My background is in software, not electrical engineering. As such, I faced a steep learning curve when I worked on my [Stargate SG-1 build](https://www.thingiverse.com/make:749261) and [ST:TNG Warp Core](https://www.thingiverse.com/make:873584). In both instances, I was extremely lucky to have both my Dad, and also Dan Clarke (aka "Boogle" from Thingiverse), giving me guidance along the way. I've tried to write these directions with sufficient clarity that someone without significant software or electrical background will be able to work through them. As with my previous documentations, if you're already familiar with these subjects you'll undoubtedly find some of what I've written to be tediously over-explained. While this is NOT a beginner level project, I firmly believe that even a beginner *can* build this, given enough patience and willingness to learn (and fail, and try again). If you are a beginner, please note that this build involves a LOT of soldering, some updating of Python files, and basic configuration of Linux via command line (there is no GUI). While in some ways this is an easier project than the SG1 gate because there are no physical moving parts, it's worth re-iterating that there is a LOT of soldering required: even if you use the PCBs I've designed, there are still ~400 individual solder points just for the LEDs (plus another 40-50 or so on the main PCB, though those are far easier).

Last preface: I've tried hard to make these directions as complete as possible, but there might be things I missed or forgot about. If you find a mistake or something is missing, please let me know so I can try to fix it!

## Additional credit

Stargate Atlantis sound effects are all from https://github.com/RafaelDeJongh/cap_resources


## Shopping List

### Hardware
- 1x Raspberry Pi Zero W (the "W" stands for Wireless)
- 1x [Micro SD card for your Pi](https://smile.amazon.com/gp/product/B07WYXBNLH/)
- 1x set of [Adafruit Brass Standoffs](https://www.adafruit.com/product/2336)
- 1x [Adafruit I2S 3W Breakout](https://www.adafruit.com/product/3006)
- 1x [40mm Speaker](https://www.adafruit.com/product/3968)
- 1x [20A / 5V power supply](https://smile.amazon.com/gp/product/B07TZNMD8K/) (the 100W version is just fine)
- 1x [15A / 250V rocker switch](https://smile.amazon.com/gp/product/B07KS2TQ45/)
- Lots of wire (see the section on Wire below for more details)
- Optional: [6x2mm magnets](https://smile.amazon.com/gp/product/B079FLRQJP/) for control box and side panel tops


### LEDs and custom PCBs

The Atlantis Gate uses WS2812B addressable RGB LEDs (the same as Adafruit's NeoPixels, just un-branded), meaning that each individual LED can be turned on and off and changed to a specific color, independent of all the other LEDs in the string. (for those curious, they don't have "addresses" per se; a long string of bytes is sent to the LEDs, and each LED chomps off the first few bytes to use as its color/brightness values, then passes the rest of the bytes to the next LED; the downside is if any of your Data In or Data Out connections becomes loose, any LEDs downstream won't know when to turn on/off). I should also mention these particular LEDs are 4-pin not 6-pin, which means they don't have the data pass-through capability if one dies. If you have an issue where your LEDs stop turning on past a certain point in the strand, it could be the first "off" LED is dead and needs to be replaced.

My build of the gate has 211 LEDs. Each LED can use anywhere from [20 - 60mA of power](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels), depending how bright you drive it. With 211 LEDs x 60mA, the maximum potential draw is 12.6 Amps. From my research, the suggestions I read suggest not going above 80% brightness in order to lengthen the life of the LEDs (and apparently there's not much/any visible difference in brightness between 80% to 100%, anyway).

61 LEDs are for the wormhole, for which I used a 1-meter segment of this LED strip:
- 1x [LED Strip for Wormhole](https://smile.amazon.com/gp/product/B01CDTEG1O/)

Optionally, you can spray paint the wormhole LED strip silver so it blends in better with the gate. *Important*: before spraying the strip, you'll want to cover each individual LED so it doesn't get covered in paint. I cut small squares of Scotch tape and taped over the top of each LED. Then I taped down the whole strip to a long piece of cardboard so it wouldn't move while I sprayed it.

For the remainder of my LEDs, I designed several Printed Circuit Boards (PCBs), and then used [JLCPCB](https://jlcpcb.com)'s assembly services to take care of the surface mounting for me. In his build, I believe Glitch hand-soldered all the individual LEDs, so that's certainly an option, too, but the LEDs melt easily and are quite small and finicky, so I decided it was worth spending money to save on time and frustration. You can make the choice that's right for you.

If you are hand-soldering the LEDs, you will need between 131 (Glitch's model) to 150 (my model) of these LEDs:
- [WS2812B-B](https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_Worldsemi-WS2812B-B_C114586.html). I recommend buying plenty of spares, since as I mentioned they melt easily.

Or, you can order the following custom PCBs, with optional assembly services by [JLCPCB](https://jlcpcb.com). This is not the cheapest option, especially because due to JLCPCB's rules I had to design each type of PCB separately (honestly I'm lucky they let me slide with having all 8 unique stair PCBs in one design). But it can save some time and potential frustration.
- [Stairs and Rear Window PCB](https://oshwlab.com/jeremyrgustafson/stargate-atlantis) (minimum order of 5x boards, *2*x with assembly services - you'll only need one, but 2x is the minimum allowed for assembly)
- [Chevrons PCB](https://oshwlab.com/jeremyrgustafson/stargate-atlantis-chevrons) (minimum order of 5x boards, and all *5*x with assembly services; there are 4 chevrons per board, due to limitations of how many holes JLCPCB will drill without charging extra fees for drill bits, and so to get 9 chevrons you need 3x boards assembled; unfortunately JLCPCB only gives the option of 2x or 5x for assembly, so you're stuck with a bunch of extras.)
- [Individual LEDs](https://oshwlab.com/jeremyrgustafson/individual-ws2812-leds-10-up) (15x or more boards, all with assembly services; 15x will give you exactly 150 LEDs so I recommend 20x or more so you have spares)


Regardless of which option you choose for LEDs, you'll also need this PCB HAT ("Hardware Attached on Top"), along with associated components:

- 1x [PCB HAT](https://oshwlab.com/jeremyrgustafson/StargateAtlantis)
- 1x 470 Ohm resistor (a standard one, not surface mount)
- 2x 1000uF, 6.3V or higher Capacitor
- 1x 2.54mm 7-pin female header [C124418](https://lcsc.com/product-detail/Female-Header_Shenzhen-Cancome-Female-header-1-7P-2-54mm-Straight-line_C124418.html)
- 1x 2.54mm 2x20 female header - short [C50982](https://lcsc.com/product-detail/Female-Header_2-54mm-2-20PFemale-header_C50982.html)
- Optional: 2x 2x7 female header [C38844](https://lcsc.com/product-detail/Pin-Header-Female-Header_BOOMELE-Boom-Precision-Elec-C38844_C38844.html)
- Optional: 2x 2-pin terminals (such as [C8269](https://lcsc.com/product-detail/Screw-terminal_Ningbo-Kangnex-Elec-WJ128V-5-0-2P_C8269.html)) rated for 5V and bare-minimum 6 amps, though ideally much more

The 2x20 header needs to be soldered into the PCB, and then stacked on top of the Raspberry Pi. The Adafruit I2S 3W speaker board plugs into the 7-pin header on the PCB. The numerous LED 5V and ground connections plug into the 2x7 C38844's.

Power for the whole system is provided via the 5V/20A adapter. Do not plug the Raspberry Pi Zero W directly into power (except during initial setup, described later). You must connect *FOUR* wires from the power supply to the PCB, either directly soldered into the PCB or via the 2-pin terminals. Each 5V wire will carry up to 6 amps; to prevent the risk of fire, use thick wires (I suggest at least 14 gauge or thicker). I was able to buy 1 foot of both black and white wire from my local hardware store, rather than needing to buy an entire spool.


#### Ordering PCBs from JLCPCB

To order the above-mentioned PCBs from [JLCPCB](https://jlcpcb.com), here are the basic steps.

1. Open one of the PCB links above (I don't want to start a religious war, but you must use a supported browser to access EasyEDA; I used Chrome).

2. Scroll past the schematic and below that you'll see the PCB design; click on the "Open in editor" button next to the words "Stargate Atlantis PCB" (or whichever PCB you happen to have open). You should now see a circuit board in the middle of your window.

3. In the top menu bar, click the folder icon with a "G" and an arrow (it's to the right of the "BOM" button); the hover text will say "Generate PCB Fabrication File(Gerber)".

4. When prompted, choose "Yes, Check DRC". There should be no errors. If you get an error related to the "GND" net, you may need to tell EasyEDA to re-build the copper area; click anywhere in the PCB design area, then press Shift+B, then check DRC again and it should be resolved. If there are other issues besides that, that probably means a design rule has changed since I put this together; send me a note and I'll try to fix it.

5. Choose a PCB quantity, the minimum order is 5 boards. You can leave the rest of the settings default. In the lower right, click "Order at JLCPCB"

6. In the JLCPCB order, you can leave everything default and click "Save to Cart". Or, for a few extra monetary units, you can have JLCPCB do most of the soldering work for you (this is only needed on the LED PCBs, not the main Stargate Atlantis Pi HAT, as those components don't qualify for assembly services). Turn on "SMT Assembly", choose "Assemble top side," choose your quantity you want assembled, and click Confirm.

   - To generate a BOM file, open the PCB EasyEDA project again and click the "BOM" button, then "Export BOM". Upload that file to the JLCPCB prompt.

   - To generate a CPL file, open the PCB EasyEDA project again, hover over the file folder icon in the upper left, and choose "Export Pick and Place File...". *Important* You must check the checkbox for "Include panelized components' coordinates". Upload that file to the JLCPCB prompt.

7. After ordering the PCB, you can get discounted shipping for your additional parts from LCSC at checkout, as long as you're signed in on the same account.


### Wires

I used several gauges of wire throughout the project, roughly based on how much current I thought they'd need to carry, and how cautious I wanted to be not to set the house on fire. If you're [not familiar with wire gauges](https://learn.adafruit.com/wires-and-connections/wire-guages), the *lower* the number, the *thicker* the wire (and the thicker the wire, the harder it is to bend into place). Note you can always use a lower gauge/thicker wire in place of a thinner one, but I'd recommend checking your amperage before going thinner. You should plan a maximum of 60mA per LED.

In order to minimize the current flowing through any particular wire, I divided the LEDs into multiple sections, with each section having its own 5V and Ground connections (with one continuous Data signal going from the Raspberry Pi all the way through all the LED strings) :

- Gate chevrons
- Gate symbols
- Wormhole
- Stairs 1-8
- Left-side and left-front
- Right-side and right-front
- Rear window

Voltage can "flow" any direction, so for the chevrons, symbols, wormhole, and stairs, I connected 5V and Ground on both the "in" and the "out" ends of the strand. This has two benefits. First, since voltage is coming into the string from both ends, it prevents an issue where the last LEDs in a long string are slightly browner because they're not getting as much voltage as the LEDs earlier in the string. Second, it creates some redundancy if, say, a connection comes loose in the middle of your already-glued-together gate (which happened to me). By having voltage and ground on both ends of the string, you can tolerate up to one loose connection on each. (Though, if that happens it's worth making absolutely sure you don't have a short that could cause a "smoke event"... which also happened to me in a separate incident).

You will need:
- Short amount of thin wire (28-30 gauge or thereabouts) to connect the speaker to the Adafruit speaker breakout board
- Short amount of very thick wire (14 gauge or thicker) to connect the power supply to the PCB HAT
- Large amount of [less-thick wire (around 22 gauge)](https://smile.amazon.com/gp/product/B083DN2MW1/) for connecting individual LEDs (whether or not you use my LED PCB designs, the 5V connections will need to carry a fair amount of current - up to 60mA per connected LED - hence the thicker wire)

Optional but highly recommended, a lot of Male-Female jumper wires of various lengths:
- [19.7 inch](https://smile.amazon.com/gp/product/B07GD2SW11/)
- [7.8 inch](https://smile.amazon.com/gp/product/B07GD2BWPY/)
- [5.9 inch](https://smile.amazon.com/gp/product/B07GD25V8D/)
- [3.9 inch](https://smile.amazon.com/gp/product/B07GD1R5MS/)

Also optional but recommended is some cable management:

- [Cord protector](https://smile.amazon.com/gp/product/B07FW672R7/)

Why so many different lengths? And why a nearly 20-inch one? When I first assembled my gate's base, I tried fitting the Raspberry Pi Zero and speaker and all the wires into the base itself; long story short I couldn't do it (and ended up tearing loose a number of soldered connections in the process of trying to "force" things to fit). I really don't know how Glitch was able to fit his Arduino and all his wiring into the base, it's just such a small space. So, instead, I bought these 19.7-inch jumper wires and, for each of my 5V and Ground connections coming off the LED PCBs, I ran them out the side of the base to the Pi HAT which can now sit a few inches away in a separately-printed container box. As it is, the base is still quite crowded with wires, but less so than when I was trying to fix the Pi and speaker into there.

And very-lastly, it's probably obvious but you'll also need all the right tools, such as a soldering iron, multimeter, tweezers/pinchers/holders to assist with soldering, wire strippers, etc. If you use the PCBs I've designed, you'll also want a [hand nibbler like this one or similar](https://smile.amazon.com/Parts-Express-Nickel-Plated-Nibbling/dp/B0002KRACO/).

### Optional Touch Screen

You can control your Stargate using a web browser on your local wifi network (either on a computer or mobile device), or, you can connect a touch screen to the Pi itself. This is ideal if you will have your gate on display at, for instance, your cubicle, where workplace rules prevent you from connecting it to the network.

- Optional: 1x [WaveShare 7 inch HDMI touch screen](https://smile.amazon.com/gp/product/B077PLVZCX/)
- Optional: 1x [Mini-HDMI to HDMI cable, for monitor](https://smile.amazon.com/gp/product/B088BLPQSD/)
- Optional: 1x [Micro-USB to Micro-USB cable, for monitor](https://smile.amazon.com/gp/product/B076HGJGPK/)


## Some brief 3D printing and assembly advice

I highly, highly recommend that you test all your LED connections (everything daisy-chained together into one continuous string) before assembling the gate. See the "Testing the LEDs" section below for a simple test case that will light up all the LEDs in sequence. Troubleshooting any potential loose connections or broken LEDs now will save hours of headaches later.

This is totally optional, but I wanted to differentiate my SGA and SG1 gates, so I printed the gate in silver (but stuck with a dark grey for the base).

When assembling the gate ring, I suggest printing 4 or more of the "Gates_Parts_Jig.stl" from https://www.thingiverse.com/thing:2795518, as well as purchasing a pack of thick binder clips. The jig will make lining up the front and back pieces of the gate ring infinitely easier, and the clips will help hold things together tightly while the glue dries.

If you have a large enough printer bed, I suggest printing 4 of the `gate_1_ax2_x4.stl` (again from https://www.thingiverse.com/thing:2795518) in lieu of 8 of the 9 `sga_gate_back.stl`'s from Glitch's design. It's the same design on both Glitch's SG1 and SGA gates, and in my opinion the larger pieces make it easier to assemble the ring.

I suggest gluing the back and middle of the ring together into one complete circle, before inserting the LEDs and gluing the top pieces on. When gluing the top pieces, after clamping a section into place with the binder clips, I strongly suggest plugging in your LED strand and double checking all the lights still work. Numerous times when pressing the top gate pieces into place I caused a wire to come loose and the LEDs stopped working; by testing immediately, I was able to remove the top piece before the superglue dried, and fix the issue. The one time I didn't test, I ended up having to chip away glued-on plastic for an hour or two (and re-print the destroyed part), in order to gain access to re-solder a loose connection. That was not fun.

When assembling the stairs, if your side panels are pressing inward tightly enough, you might only need to glue in the stair back pieces, and then the tops and fronts will "snap" into place. (except for the bottom-most stair's front piece, which will also need to be glued). Note that for the top pieces, the "bump" part goes down; my first attempt I didn't watch Glitch's assembly video closely enough and mistakenly put the stair tops in upside down.

If using my staircase PCBs, you may need to trim them slightly to fit into the stairs. It's a tight squeeze. There are also a lot of wires all in a small amount of space so go slowly and use lots of tweezers.

### Wire assembly suggestions

For each of the LED PCBs, I cut male-male jumper wires in half and soldered the loose wire ends to the LED PCBs. In order to protect against short circuits, I (mostly) only used the male half of the jumper wires for any power/ground that was coming into the LED boards; that way the bundle of 19.7" jumpers that had the live power coming from the HAT all had female ends that couldn't touch. The exception is there were a couple very small strands of LEDs where I thought it would be easier to connect to each other for power, rather than running another 19.7" wire just for a couple LEDs. Specifically, I added power "out" from each of the 4-LED side strands and then plugged the top-front-side LEDs into those. Otherwise, all the 5V and Ground connections from inside the base I plugged into 19.7 inch jumpers that come out of the base, and plugged into the HAT's 5V and G headers.

Alternatively, you could solder all your LED wires directly to the PCB and not worry about all these jumpers connecting and potentially coming loose. I just wanted more flexibility so might have over-complicated mine a bit. No matter which option you choose, it probably goes without saying but keep close track of which color(s) of wire you use for 5V vs Ground vs Data. You can permanently damage your LEDs if you mix those up.

Lastly, let me over-explain the Data wires. There must be one continuous Data path from the Pi HAT to the very last LED. The Data Out from the Pi's PCB goes into the Data In on the first set of LEDs, and so on. It doesn't matter if you have the Data Out from the HAT as a male or female jumper, so long as you're consistent on every connection after that. All the Data wires will be connected inside the base, but it doesn't matter what order you connect the LED strands, as you'll be able to correct it in the software's config.py file later.

### Printing the control box, and other extras

#### Control box
To hold the power supply and Pi, I designed a container box. The files are included in the "STLs" folder. You will need to print the following:

SGA power adapter holder - cover.stl
SGA power adapter holder - cover - SGA logo.stl

And either: (with support, that is a pain to remove)
SGA power adapter holder - Whole box

or both of: (no/minimal support required)
SGA power adapter holder part 1.stl
SGA power adapter holder part 2.stl

I printed the cover.stl vertically with a 20mm brim, and discovered the logo didn't print nice vertically. So I separated the logo out to print horizontally, and then just glued it into place on the cover.

There are holes in the bottom of the cover and the top of the box for little magnets (link is in the shopping list section above) to help hold it in place securely. Superglue the magnets into the holes, and double check the polarities before glueing each one.

I'm not a 3D designer so the speaker hole doesn't really hold the speaker very well, so I just used some electrical tape to help hold it in place.

The lip on the top of the cover will hold the WaveShare monitor in place, if you chose to purchase one.

Once when I jiggled the HDMI cable in the Pi it seemed to short the Pi with the power supply's metal grating. My Pi shut down but fortunately wasn't permanently damaged. I stuck a spare not-perfect-print of one of the Stargate base's walls underneath the Pi, so there was a plastic barrier between the power supply's metal case and the Pi, and that seems to have solved it.

To attach the plug receptacle I just used some spare screws I had lying around.

#### sga_base_top_left_revised.stl

I wanted to retain access to the top left+right side panels in case a wire came loose (as happened several times to me). I also couldn't get the `sga_base_left_front_led_support.stl` to fit with my LEDs. So, I designed a different side-top file that could use more magnets to help hold both top/front compartments together nicely. Print `sga_base_top_left_revised.stl` once normally, and once again mirrored. Glue magnets into the holes. The attach another magnet to each of those, dab a spot of glue on the backside of the second magnets, and put the top pieces into place on the model, using a clamp or something to hold them in place. Let the glue dry, and now you'll have perfectly positioned magnets.

## Rasperry Pi Setup

### Install Raspbian Lite
First [install a fresh copy of Raspbian Lite](https://www.raspberrypi.org/documentation/installation/installing-images/). At the time of this writing, the latest release was "Buster" (build date May 7, 2021). Newer versions of Raspbian may require changes to portions of these directions.

### Headless setup
Before installing your SD card into the Pi, set it up for wireless access and ssh ("headless" setup). The exact steps here will differ depending if you're on a Mac or Windows. I've written these instructions based on macOS.

On your laptop, with the SD card inserted, open your Applications > Utilities > Terminal.app.

Perform step 3 from https://www.raspberrypi.org/documentation/remote-access/ssh/ to enable ssh:

```touch /Volumes/boot/ssh```

Then, follow these steps to set up wifi access: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

```vi /Volumes/boot/wpa_supplicant.conf```

(I use `vi` for my editor; if you're new to the command line, replace the word "vi" with "nano" in the command above, and anywhere else in this document that you see "vi")

Add these lines to the file, changing the ssid and psk variables for your own wifi network: (note that Pi Zero W's don't support 5GHz networks)

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
	ssid="YOUR WIFI NETWORK NAME"
	psk="YOUR WIFI PASSWORD"
}
```

Unmount the SD card and move it from your laptop to your Pi. Plug in the Pi (either directly, or, if you've already assembled your PCB HAT, you can attach the HAT onto the Pi and plug in the 5V/20A power adapter; DO NOT plug in BOTH the power adapter and also the Pi's power adapter).

**Important:** if you choose to use the optional WaveShare 7" monitor I listed above, don't plug it into the Pi until you've changed the required settings (described below).

Wait 5 minutes for the Pi to boot the first time. You should then be able to connect to it (in your Terminal) by typing `ssh pi@raspberrypi.local` (the default password is "raspberry"). Once connected, I suggest changing the hostname to `atlantispi`, changing the pi user's default password, and setting the timezone. To do all three of these, type `sudo raspi-config` and look for the appropriate menu items. After rebooting, you can then connect with `ssh pi@atlantispi.local`.


### Passwordless SSH
If desired, you can also set up passwordless ssh at this time.

```
pi$ ssh-keygen
# Hit enter at each of the prompts

pi$ nano .ssh/authorized_keys
```

Into that authorized_keys file, paste the contents of this next command, then save the file:

```your laptop$ cat .ssh/id_rsa.pub```


### Run updates

Even though you just installed a brand new image, check for (and install) any software updates. Follow the prompts after each of these three commands:

```
pi$
sudo apt-get update
sudo apt-get upgrade
sudo apt autoremove
```

### Optional: Install vi text editor

```
sudo apt-get install vim
sudo update-alternatives --config editor
```

```
vi ~/.vimrc
# Add this line:
set mouse-=a
```

```
sudo vi /root/.vimrc
# Add this line:
set mouse-=a
```

### Install required packages:

Some of these may already be at the newest version.

```sudo apt install python3 python3-daemon python3-pip python3-gpiozero python3-dev git```

Not required but recommended is to set python3 to be default (over python2) :

```
sudo update-alternatives --install /usr/bin/python python $(which python2) 1
sudo update-alternatives --install /usr/bin/python python $(which python3) 2
sudo update-alternatives --config python  # Verify python3 is listed first, then hit return
```

In order to access the web interface by hostname (http://atlantispi.local) instead of IP address, install (and then disable+stop) apache:

```
sudo apt-get install apache2 apache2-utils
sudo systemctl disable apache2
sudo systemctl stop apache2
```

Install one more package (it may already be installed), required for controlling the speaker volume from the web page interface:

```sudo apt install alsa-utils```

Next install required Python (pip3) packages:

```sudo pip3 install pygame gpiozero daemon daemontools python-daemon```


### Install speaker software

Follow Adafruit's instructions for the I2S Breakout: https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-usage

On my Pi, I had to disable the /dev/zero playback; I spent 2 hours trying to get this working (through various hacks of /etc/systemd/system/aplay.service), but to no avail.

After rebooting, my Pi started repeating (every minute or so) a poor quality recording that said "To install the screenreader, press control-alt-space." Apparently this is due to the headless setup (described earlier). To turn it off:

```
sudo rm /etc/xdg/autostart/piwiz.desktop
sudo reboot
```

If you've heard the annoying voice mentioned above, then you already know your speaker is working. But if you'd like to double-check that, you can test the speaker by installing mpg123 (an mp3 decoder) and then playing a stream:

```
sudo apt install mpg123
mpg123 http://ice1.somafm.com/u80s-128-mp3
```

Press "q" to quit.


### Configure /boot/config.txt

There are several changes needed in /boot/config.txt.

```sudo vi /boot/config.txt```

Uncomment and/or add the following lines:
```
hdmi_force_hotplug=1
hdmi_force_edid_audio=1

dtparam=spi=on
```

Comment out this line if it's not already:
```#dtparam=audio=on```

Add these lines if they aren't already there:
```
dtoverlay=hifiberry-dac
dtoverlay=i2s-mmap
```

Add these lines:
```
# For LEDs over SPI
core_freq=400
core_freq_min=400
```

The `core_freq=400` and `core_freq_min=400` are **very important** so the LEDs work properly over SPI, otherwise the Pi's clock speed can dip lower than the LEDs are expecting and the lights will not light up correctly.

After making all the above changes, reboot.

```sudo reboot```

After rebooting, make sure these files show up:

```ls -l /dev/spi*```

If you don't get output from that command, something isn't right and you'll have to troubleshoot.

### snd-blacklist.conf

This is required to control the WS2812 LEDs over SPI. Edit this file and add the one line, then reboot:

```sudo vi /etc/modprobe.d/snd-blacklist.conf
blacklist snd_bcm2835
```

```sudo reboot```

### /boot/cmdline.txt

This shouldn't require editing. Double check your /boot/cmdline.txt contains the following:

```
cat /boot/cmdline.txt
console=serial0,115200 console=tty1 root=PARTUUID=........-.. rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```

### Set up WaveShare monitor

If using the WaveShare 7" monitor, follow these directions from [https://www.waveshare.com/w/upload/5/58/7inch_HDMI_LCD_%28H%29_User_Manual.pdf](https://www.waveshare.com/w/upload/5/58/7inch_HDMI_LCD_%28H%29_User_Manual.pdf) : 

```sudo vi /boot/config.txt```

Add these lines to the bottom of the file:
```
# WaveShare monitor settings
max_usb_current=1
hdmi_force_hotplug=1
config_hdmi_boost=10
hdmi_group=2
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0
```

#### Auto-login as Pi user

This is only required if using an attached monitor.

Using `sudo raspi-config`, under System Options, enable "Desktop Autologin".

#### Reboot again

Reboot your pi, after which you can plug in the WaveShare monitor:

```sudo reboot```


## Testing the LEDs

If you haven't already connected your PCB HAT to the Pi and plugged in all your LED wires, now is the time. Once everything is connected, you can test that all your LEDs light up with the following steps.

Install this library from https://github.com/rpi-ws281x/rpi-ws281x-python :

```sudo pip3 install rpi_ws281x```

(On my Pi, after I hit return it seemed to sit for a minute before doing anything, so don't panic if you don't see immediate activity)

Grab a library of simple test cases.

```
cd /home/pi/
git clone --recursive https://github.com/rpi-ws281x/rpi-ws281x-python
cd /home/pi/rpi-ws281x-python/examples
vi strandtest.py
```

Modify these variables near the top of the file:

```
# LED strip configuration:
LED_COUNT = 211       # Number of LED pixels.
#LED_PIN = 18         # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN = 10          # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 64   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
```

And then personally I recommend commenting out the `theaterChase` commands on lines 110-113 and 117, especially if you have health concerns that make you susceptible to flashing lights.

This is the moment of truth. Test your LED strand with:

```sudo python3 /home/pi/rpi-ws281x-python/examples/strandtest.py -c```

At this point all the LEDs should light up in sequence. Note that my example above sets the LED_BRIGHTNESS variable to 64 out of 255, so don't worry if some of the LEDs appear "dim" (for instance the staircase and gate symbols that are behind a layer of 3D printed plastic).

Press Control-C to turn off all the lights and exit the `strandtest.py` program.

If the first X number of lights turn on but then nothing after a certain point, first double check that you have the correct LED_COUNT set in your `strandtest.py` configuration. More than once I started to panic about half my LEDs not lighting up, until I noticed I'd forgotten to update that variable. As a side-note, there is no harm in setting that number higher than the number of real LEDs you have; the only downside is that the program will take longer to move onto the next step (e.g. if you have 200 LEDs but set the count to 300, you'll twiddle your thumbs while waiting for the program to "turn on" those 100 extra non-existant LEDs before it moves on to the next color).

If that doesn't fix it, see the Troubleshooting document for more suggestions.

### Sidebar about how addressable LEDs work

If you're mildly curious about how addressable LEDs work, read on. Otherwise you can skip this section.

The "WS" in the WS2812 name stands for "World Semi", the company who makes the LEDs. If you see references to "5050", that is the size of the LEDs used in this Stargate Atlantis project: 5.0 by 5.0 mm. There's also a 3535 size, which is 3.5 mm square.

All the LEDs are connected in one long chain, with the Data Out from one LED going into the Data In of the next. Some high frequency of times per second, the microcontroller (in this case, our Pi Zero) sends out a long string of bits along the Data line. The first LED chops off the first 24 bits (8 for Green, 8 for Red, 8 for Blue), which it uses for itself. Then it passes all the rest of the bits along its Data Out pin. The next LED does the same. Once there are no more bits to pass along, any LEDs downstream of that will retain their previous color/brightness and not update this cycle. This process repeats, in our case, 800,000 times per second.

I offer that simple explanation because I found the name "addressable" to be a confusing misnomer when I first started researching. By this I mean that each LED doesn't have a universal unique identifier (UUID), but rather that you "address" them by generating a long string of 24-bit chunks, with each 24-bits corresponding to the next LED. Once I understood that I could appreciate the elegance of the simplicity, since it doesn't require somehow querying and saving ID numbers from all the LEDs in a chain. Anyway, perhaps this simplistic description will be of use to someone.

For more information, you can download the data sheet for the WS2812B from World Semi here: http://www.world-semi.com/solution/list-4-1.html

## Stargate Software

### Installing / Copying Files to the Pi

Create a folder for the Stargate in the Pi user's home directory:

```mkdir ~/stargateatlantis```

Copy all the files here. I used the following "rsync" command, so I could make edits on my local computer and then upload quickly to the Pi:

```my laptop$ rsync -vPrltgoD -e ssh "/path/to/StargateAtlantisRaspberryPi/" pi@atlantispi.local:/home/pi/stargateatlantis/```


If you're using the WaveShare 7" or another touch-sensitive monitor attached to your Pi, create a script on your Pi's Desktop that will launch the web interface:

```vi /home/pi/Desktop/StargateAtlantisCommand.sh```

Copy/paste these file contents:

```
#!/bin/bash
# https://pimylifeup.com/raspberry-pi-kiosk/
rm -r /home/pi/.cache/chromium/Default/Cache/*
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences
export DISPLAY=:0.0
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --disable-session-crashed-bubble --kiosk 127.0.0.1/index.htm &
```

Make the file executable:

```chmod u+x /home/pi/Desktop/StargateAtlantisCommand.sh```

Later, once the Stargate software is running, you can double tap on this script from your Pi's desktop to launch a full-screen web browser to control the Stargate.

### Download jquery javascript

I don't want to run afoul of jquery's licensing by including this file in my GitHub repo, so you'll need to download it separately:

```
cd /home/pi/stargateatlantis/web/
wget https://code.jquery.com/jquery-3.3.1.min.js
```

### Modify config.py

All code configuration is done in the `config.py` file. The only values you *must* customize are the "LED Ranges" section, based on how many LEDs you have and what order you've plugged them in (the Data In/Data Out connections). Optionally, there are also some LED brightness and color settings that you can customize.

```vi /home/pi/stargateatlantis/config.py```

After you've customized your `config.py` file, run the main program as follows: (note, it's important to change directories to the stargateatlantis directory, otherwise the web server won't find the /web/ folder and will return 404 errors in your browser)

```cd /home/pi/stargateatlantis/ ; sudo python3 main.py```


You can now open the `StargateAtlantisCommand.sh` script on your touch-monitor, or on another computer visit to http://atlantispi.local , to control your Stargate.


### Auto-Run

If you're happy with how the Stargate works, you can now set the program to auto-run:

You can use [Daemon tools](https://samliu.github.io/2017/01/10/daemontools-cheatsheet.html) to ensure the Python program runs at boot.

First ensure the Python program isn't running, then execute following commands:

```
sudo apt install daemontools daemontools-run
sudo mkdir /etc/service/stargateatlantis
sudo vi /etc/service/stargateatlantis/run
```

Enter the following text:

```
#!/bin/bash
cd /home/pi/stargateatlantis
exec /usr/bin/python3 main.py
```

Save and quit, then execute the following:

```sudo chmod u+x /etc/service/stargateatlantis/run```

The Python program should immediately start running. You can now control the Stargate via web browser as soon as the Raspberry Pi boots.

### Auto-launch dialing page on Pi's touch-screen

To automatically launch the dialing web page on your Pi's touch-screen monitor when the Pi boots, do the following:

Check to see if you already have an autostart file:

```ls /home/pi/.config/lxsession/LXDE-pi/autostart```

If you don't, copy the default one as a starting point:

```
mkdir -p /home/pi/.config/lxsession/LXDE-pi/
cp /etc/xdg/lxsession/LXDE-pi/autostart /home/pi/.config/lxsession/LXDE-pi/autostart
```

Now edit it:

```vi /home/pi/.config/lxsession/LXDE-pi/autostart```

and add this line to the bottom (this will execute the script we created in an earlier step)

```@/bin/bash 'sleep 5 ; /home/pi/Desktop/StargateAtlantisCommand.sh'```

Reboot your Pi, and the webpage should launch on its attached display automatically!


### Screensaver

If you'd like to enable a Stargate Atlantis screensaver (I downloaded [this video](https://www.youtube.com/watch?v=0H_0eXsFi20) as an mp4, though you might also like [this one](https://www.youtube.com/watch?v=ZtLJfxEZRN4)), do the following steps:

```sudo apt-get install xscreensaver```

Change permissions on this file (already included in your Git download):

```chmod +x /home/pi/stargateatlantis/web/VideoScreensaver.sh```

Edit your autostart file

```vi /home/pi/.config/lxsession/LXDE-pi/autostart```

and add these lines at the end:

```
@xscreensaver -no-splash
@/home/pi/stargateatlantis/web/VideoScreensaver.sh
```

Your complete autostart file should now look something like this:

```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@/bin/bash 'sleep 5 ; /home/pi/Desktop/StargateAtlantisCommand.sh'
@/home/pi/stargateatlantis/web/VideoScreensaver.sh
```

And, of course, download a video you'd like for the screensaver. You can name it "SGASpinningLogoAnimation.mp4" and drop it into the "web" folder, or if it's named something else, edit the `VideoScreensaver.sh` script to use your correct filename.


### Automatically turn screen off and on

If you want your attached screen to turn off and on automatically (for instance, turn off overnight), you can set up a cronjob that will do that. The following example turns the screen on at 7 a.m., off at 9 a.m., on again at 4 p.m., and off again at 10 p.m.:

```
sudo crontab -e

0 7 * * * vcgencmd display_power 1
0 9 * * * vcgencmd display_power 0
0 16 * * * vcgencmd display_power 1
0 22 * * * vcgencmd display_power 0
```

### That's it!

You're all done! Congratulations! I'm proud of you for sticking with it! Now, enjoy your Stargate!

## Other Helpful links

[Glitch's Stargate Atlantis on Thingiverse](https://www.thingiverse.com/thing:3153542)

[Glitch's Stargate Atlantis assembly video](https://www.youtube.com/watch?v=zSUKtZLlsoY)

[Glitch's Stargate Atlantis web page](http://www.glitch.uk/working-stargate-atlantis/)

[Mod parts for Stargate](https://www.thingiverse.com/thing:2795518)

[WaveShare monitor instructions](https://www.waveshare.com/w/upload/5/58/7inch_HDMI_LCD_%28H%29_User_Manual.pdf)

[Guide for NeoPixels](https://learn.adafruit.com/neopixels-on-raspberry-pi)


## Future improvements

I have some ideas for improving the gate, but I'm ready to move onto the next project. Perhaps another inspired soul will come along and want to tackle these!

1. If I were to build another one of these gates, I'd use two LEDs per gate symbol instead of just one, so that the entirety of each symbol could be lit instead of just the center. I'd also modify the `sga_gate_middle_x8` and `sga_gate_middle_bottom` STL files so there are holes in the walls between symbols, so wires can go directly from one symbol to the next without needing to loop up and over the little wall. I think that would really help with not breaking off soldered wires when assembling the gate.

2. Or, instead of number 1, what I'd really LOVE is for each of the 36 symbols to be its own tiny display or LED matrix, so that the symbols really could "move" around the gate, like the in-show dialing. I have wondered if this could be achieved using an [IS31FL3731 chip](http://www.issi.com/WW/pdf/IS31FL3731.pdf) and 0402 or smaller LEDs (the symbol area is only about 20x16mm). But, that is far beyond my electronics expertise. Alternatively, I did come across some small displays, this one from [Wish.com](https://www.wish.com/product/5d5ce7e6d0f70843c77bf175?hide_login_modal=true&share=web) and this one from [Adafruit](https://www.adafruit.com/product/3533), though I'm not sure if (or how well) they are daisy-chainable. It'd be expensive, too, but would really be the "bees knees" in getting a more screen-accurate dialing sequence.

3. In the web interface, I'd love a user-friendly way to set individual or groups of LEDs to a particular color, and then save that into a config file, then be able to recall and set that design at the press of a button (similar to how the Philips Hue lights and app work). Related to this, I'd love to add holiday-themed color profiles for the gate that could be enabled/disabled.

4. I'd love to network the SGA and SG1 gates so they can dial each other if they're on the same wifi. This could include some fun sound effects of Walter exclaiming "unscheduled offworld activation!"