from datetime import datetime
from LightingControl import LightingControl
import config

# Chevrons to show for specific number positions
hour_lookup = [
    [4],        # 0
    [4, 5],     # 1
    [5, 6],     # 2
    [6],        # 3
    [7],        # 4
    [7, 8],     # 5
    [8, 0],     # 6
    [0, 1],     # 7
    [1],        # 8
    [2],        # 9
    [2, 3],     # 10
    [3, 4],     # 11
    [4]         # 12
]


class AnimClock:
    def __init__(self, light_control):
        self.light_control = light_control
        self.hr = 0
        self.mins = 0
        self.secs = 0

    def animate(self, reset):
        if reset:
            self.hr = -1
            self.mins = -1
            self.secs = -1
            self.light_control.all_off()

        now = datetime.now().time()
        hour = now.hour
        mins = now.minute
        secs = now.second
        if hour > 12:
            hour -= 12
        # This next line has some fun math. The config.topmost_physical_symbol is at noon-o'clock,
        # so we start counting from there, and multiply the minutes by 36 symbols divided by 60 minutes.
        # Lastly, we perform a modulo 36, so the end result is between 0-35.
        mins = (config.topmost_physical_symbol + int(round(((float(mins) / 60.0) * 36.0)))) % 36 # 36 symbols on SGA gate
        
        # The wormhole strip LED 0 is at the bottom of the gate at the "30 seconds" position, so to workaround this,
        # add 30 seconds and then perform a modulo 60 to keep it in the range 0-59.
        secs = (secs + 30) % 60

        #print('Time: {}:{}:{}, Calc Time: {}:{}:{}'.format(now.hour, now.minute, now.second, hour, mins, secs))
        #self.light_control.all_off()
        if hour != self.hr:
            self.light_control.light_all_chevrons(color=config.color_off)
            self.show_hr(hour)
            self.hr = hour
        if mins != self.mins:
            self.light_control.light_all_symbols(color=config.color_off)
            self.show_min(mins)
            self.mins = mins
        if secs != self.secs:
            self.light_control.light_LED(config.leds['wormhole'][self.secs], color=config.color_off)
            self.show_sec(secs)
            self.secs = secs
        return 1

    def show_hr(self, hr):
        for chevron in hour_lookup[hr]:
            self.light_control.light_chevron(chevron)

    def show_min(self, mins):
        self.light_control.light_symbol(mins)

    def show_sec(self, secs):
        self.light_control.light_LED(config.leds['wormhole'][secs])

