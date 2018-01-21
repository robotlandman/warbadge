# config.py
# WarBadge Common Configuration

# The Wi-Fi SSID to connect to
CONNECT_SSID = 'shmoocon-romp'

# The base URL to post scan results to
UPLOAD_URL = 'https://warbadge.ninja/checkin/'

# Don't upload more often than this in ms
UPLOAD_INTERVAL = 20000

# Status code for good upload
UPLOAD_GOOD_STATUS = 201

# Don't scan more often than this in ms
SCAN_INTERVAL = 15000

# Wait before scanning while connecting in ms
CONNECT_PAUSE = 1000

# NeoPixel LED configuration
PIN_NEOPIXEL = 14

# Number of LEDs in the chain
LED_COUNT = 2

# LED indices
#   0 is top of rocket
#   1 is bottom of rocket
LED_SCAN = 0
LED_WIFI = 1

# LED color constants
LED_COLOR_WIFI_DOWN = (0, 0, 255)
LED_COLOR_WIFI_UP = (0, 255, 0)
LED_COLOR_SCAN = (0, 0, 255)
LED_COLOR_UPLOAD = (255, 100, 0)
LED_COLOR_SUCCESS = (0, 255, 0)
LED_COLOR_ERROR = (255, 0, 0)
LED_COLOR_OFF = (0, 0, 0)
