# ShmooCon 2018 WarBadge Games
## [![Build Status](https://travis-ci.org/robotlandman/warbadge.svg?branch=master)](https://travis-ci.org/robotlandman/warbadge)
See more at [warbadge.ninja](https://warbadge.ninja)

## How to flash a badge
The 2018 ShmooCon [badges](https://www.instagram.com/warbadge/) have an ESP 8266 chip inside. If you open the case you will se an "S2" pad, which is where the reset button would normally go. You have to short this pad (a flathead screwdriver blade works well) while turning the badge on. This will put the badge in serial bootload mode.

Once the badge is in this mode you can load anything that runs on the ESP 8266 via USB serial cable. In this case, the [MicroPython](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html) image via [esptool.py](https://github.com/espressif/esptool). You will need the [serial driver](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers) if you are running Mac or Windows.

Your load command on a Mac will look something like this:
```
esptool.py --port /dev/cu.SLAB_USBtoUART --baud 115200 write_flash --flash_size=detect -fm dio 0 esp8266-20171101-v1.9.3.bin
```

Power the badge off and back on, and connect via serial terminal (e.g. minicom, PuTTY, etc.) You will be at the MicroPython REPL and ready to the load the warbadge python program. The easiest way to do this is to wrap the files in the [badge](https://github.com/robotlandman/warbadge/tree/master/badge) folder inside python that saves them to the badge flash. That looks something like this:
```
# Hit Ctrl-E to enter bulk paste mode

output = open('config.py', 'w')
output.write("""
# Paste config.py here
""")
output.close()

output = open('main.py', 'w')
output.write("""
# Paste main.py here
""")
output.close()

# Hit Ctrl-D to end bulk paste mode and to run the pasted code
```

If it was successful, the console will display the number of bytes written for each file. The program saved to main.py will run automatically when the badge powers up.

Power the badge off and on again, and make note of the MAC address that is printed to the console. The ShmooCon Labs team is recording MACs and handles for the [leaderboard](https://warbadge.ninja/scoreboard). Post-con, well, who knows how that is going to work - stay tuned.

## What are all these LED colors?
You can see/set this in config.py, but here's an easy reference:

**Bottom LED**

Color | Meaning
----- | -------
Blue | Not connected to Wi-Fi
Green | Connected to Wi-Fi

**Top LED**

Color | Meaning
----- | -------
Blue | Scanning for SSIDs and APs
Yellow | Uploading results to [warbadge.ninja](https://warbadge.ninja/scoreboard)
Green | Successful upload
Red | Error uploading

## The con(test) is over, what now?

If you want to modify your badge and continue playing the game, update config.py with a new SSID and optional PSK to connect to. Set the SSID to your phone's hotspot and you'll have a roaming Wi-Fi scanning rig.

If you just want to use the MicroPython environment and your badge is flashed, hit Ctrl-C to break out of the main.py running program. The badge has two [NeoPixel](http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/neopixel.html) RGB LEDs off pin 14 in addition to the Wi-Fi capabilities of the ESP 8266 chip. Index 0 is the LED in the nose of the rocket and index 1 is the tail LED.

Have fun!