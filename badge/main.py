# main.py
# WarBadge main program

import time
import machine
import neopixel
import network
import ubinascii
import urequests
import ujson
import config

# Scan for SSIDs
def scan(nic, ap_neighbors):
  # Scan for local APs
  scan_results = nic.scan()

  # Compare scan results against what we have already seen
  for result in scan_results:
    ssid = result[0]
    bssid = ubinascii.hexlify(result[1])
    rssi = result[3]
    # Check whether this is a new SSID or a new BSSID/RSSI
    if ssid not in ap_neighbors:
      # A new SSID
      ap_neighbors[ssid] = {
        bssid: rssi
      }
    else:
      # A new BSSID and/or RSSI
      ap_neighbors[ssid][bssid] = rssi


def main():
  # Our main program setup

  # Set up the two RGB LEDs
  np = neopixel.NeoPixel(machine.Pin(config.PIN_NEOPIXEL), config.LED_COUNT)

  # LEDs off
  np.fill(config.LED_COLOR_OFF)
  np.write()

  # Set the Wi-Fi radio to be a client only
  nic = network.WLAN(network.STA_IF)
  nic.active(True)
  need_first_connect = True
  unused_nic = network.WLAN(network.AP_IF)
  unused_nic.active(False)

  # Capture the MAC for the ID
  mac_id = str(ubinascii.hexlify(nic.config('mac')), 'utf-8')

  # Print the MAC ID on the console
  print('You are %s' % mac_id)

  # Keep track of all the APs we see
  ap_neighbors = {}

  # Keep track of how often we scan for SSIDs
  last_scan = time.ticks_ms()

  # Keep track of how often we upload scan results
  last_upload = time.ticks_ms()

  # Keep track of the last Wi-Fi connection
  # This fixes the walkaround double-blue LED issue
  last_connect = time.ticks_ms()

  # Our main program loop
  while True:
    # Check Wi-Fi connectivity
    if nic.status() == network.STAT_GOT_IP and not need_first_connect:
      # Connected
      np[config.LED_WIFI] = config.LED_COLOR_WIFI_UP
      np.write()

      # Check whether we should upload scan results yet
      if time.ticks_diff(time.ticks_ms(), last_upload) >= config.UPLOAD_INTERVAL:
        # It's time to upload
        np[config.LED_SCAN] = config.LED_COLOR_UPLOAD
        np.write()

        # Print the MAC ID on the console
        print('You are %s' % mac_id)

        try:
          encoded_ap_neighbors = ujson.dumps(ap_neighbors).encode('utf8')
          response = urequests.post(config.UPLOAD_URL + mac_id, data=encoded_ap_neighbors,  headers={'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'WarBadge Experimental ShmooCon 2018'})
        except:
          # The upload didn't work
          np[config.LED_SCAN] = config.LED_COLOR_ERROR
          np.write()
        else:
          # Check response status
          if response.status_code == config.UPLOAD_GOOD_STATUS:
            # It worked
            np[config.LED_SCAN] = config.LED_COLOR_SUCCESS
            np.write()
          else:
            # Bad response
            np[config.LED_SCAN] = config.LED_COLOR_ERROR
            np.write()

          response.close()

        last_upload = time.ticks_ms()

    elif nic.status() == network.STAT_CONNECTING and not need_first_connect:
      # Still connecting
      np[config.LED_WIFI] = config.LED_COLOR_WIFI_DOWN
      np.write()
    else:
      # Need to connect
      np[config.LED_WIFI] = config.LED_COLOR_WIFI_DOWN
      np.write()
      last_connect = time.ticks_ms()
      need_first_connect = False

      # Check whether we have a Wi-Fi PSK set or not
      if not config.CONNECT_PSK:
        nic.connect(config.CONNECT_SSID)
      else:
        nic.connect(config.CONNECT_SSID, config.CONNECT_PSK)
      
    # Check whether we should scan for SSIDs yet
    now = time.ticks_ms()
    if time.ticks_diff(now, last_scan) >= config.SCAN_INTERVAL and time.ticks_diff(now, last_connect) >= config.CONNECT_PAUSE:
      # It's time to scan
      np[config.LED_SCAN] = config.LED_COLOR_SCAN
      np.write()
      scan(nic, ap_neighbors)
      last_scan = time.ticks_ms()
      np[config.LED_SCAN] = config.LED_COLOR_OFF
      np.write()

    # Add a little delay to save battery
    time.sleep_ms(50)


# Run our program
main()

