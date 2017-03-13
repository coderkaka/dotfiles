import subprocess

from i3pystatus import Status
from i3pystatus import *

status = Status(standalone=True)

# Displays clock like this:
# Tue 30 Jul 11:59:46 PM KW31
status.register("clock",
    format="%a %-d %b %Y %X",)

# Displays the weather like this:
#
#status.register("weather",
#    location_code="ASXX0043:1",
#    format="GEELONG {current_temp}",
#    interval=60)
#status.register("weather",
#    location_code="ASXX0075:1",
#    format="MELBOURNE {current_temp}",
#    interval=60)

# Shows the average load of the last minute and the last 5 minutes
# (the default value for format is used)
#status.register("load")

#Shows the remaining of power
status.register("battery",
    format="Pow {status}{percentage:.2f}",
    alert=True,
    alert_percentage=5,
    status={
        "DIS": "↓",
        "CHR": "↑",
        "FULL": "=", },)
# Shows the usage of memory
#status.register("mem",
#	format="Mem Usage:{percent_used_mem}",)

# Shows your CPU temperature, if you have a Intel CPU
status.register("temp",
    color="f0fff0",
    format="CPU T {temp:.0f}°C",)

# Displays whether a DHCP client is running
#status.register("runwatch",
#    name="DHCP",
#    path="/var/run/dhclient*.pid",)
#
# Shows the address and up/down state of eth0. If it is up the address is shown in
# green (the default value of color_up) and the CIDR-address is shown
# (i.e. 10.10.10.42/24).
# If it's down just the interface name (eth0) will be displayed in red
# (defaults of format_down and color_down)
#
# Note: the network module requires PyPI package netifaces
#status.register("network",
#    interface="wlp2s0",
#    format_up="{essid}:{quality} Speed:{kbs}KB/s",)

# Has all the options of the normal network and adds some wireless specific things
# like quality and network names.
#status.register("network",
#    interface="eno1",
#    format_up="Speed:{kbs}KB/s",)
#
# Note: requires both netifaces and basiciw
# Shows disk usage of /
# Format:
# 42/128G [86G]
status.register("disk",
    path="/",
    format="Disk {avail}G/{total}G",)

# Shows pulseaudio default sink volume
#
# Note: requires libpulseaudio from PyPI
status.register("pulseaudio",
#    color="9aff9a",
    format="♪ {volume}",)

#Shows backlight
#status.register("backlight",
#    color ="f0fff0",
#    format="卍 {percentage}",)

# all my custom buttons
#status.register("text",
#    text="New Comic",
#    on_leftclick="~/.config/i3/update_background",
#    color="#44bbff",)

#status.register("text",
#    text="Sleep Screen",
#    on_leftclick="sleep 1; xset dpms force off",
#    color="#44bbff",)
#
#i3lock = "i3lock -i ~/Pictures/head.jpg -p win";
#
#status.register("text",
#    text="Suspend System",
#    on_leftclick=i3lock + "; systemctl suspend",
#    color="#44bbff",)
#
#status.register("text",
#    text="Screensaver",
#    on_leftclick="xscreensaver-command -activate",
#    color="#44bbff",)

#status.register("text",
#    text="lock",
#    on_leftclick=i3lock,
#    color="#44bbff,")

status.run()
