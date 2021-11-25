import time
import random
import json
import terminalio
from adafruit_magtag.magtag import MagTag

magtag = MagTag()

#provide a local configuration file that inits
config = json.loads(open("config.json").read())

#attempt to get an updated version of the config file online.
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests

# URLs to fetch from
TEXT_URL = "https://raw.githubusercontent.com/danlemire/danlemire.github.io/main/config.json"
JSON_QUOTES_URL = "https://www.adafruit.com/api/quotes.php"

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


def get_config():
    print(json.dumps(config))
    #magtag.set_text("config['openweather_token']",0,False) #index
    
get_config()

PLAINFONT = config['plainfont']     # Use built in font if True

magtag.peripherals.neopixel_disable = config['neopixels_disable'] # turn on lights
magtag.set_background(0xFFFFFF)    # set to white background
if config['backgroundfile'] is not "":
    magtag.set_background(config['backgroundfile'])
magtag.peripherals.neopixels.fill(0x000000) # red!
#magtag.refresh()

if config['mode'] is 'local': 
    verses = json.loads(open("verses.json").read())
    print("using local verses.")
else:
    verses = webverse.json()
    print("using web verses")
    print('.......................................................')
    print(json.dumps(verses))
    print('.......................................................')
# main text large font, used to display script index 0 during dev.
magtag.add_text(
    text_font = terminalio.FONT if PLAINFONT else "Arial-Bold-24.bdf",
    text_position=(
        magtag.graphics.display.width // 2,
        10,
    ),
    text_scale = 3 if PLAINFONT else 1,
    line_spacing=1,
    text_anchor_point=(0.5, 0),
)

# verse text, index 1
magtag.add_text(
    text_font= terminalio.FONT if PLAINFONT else "Arial-12.bdf",
    text_position=(3, 5),
    line_spacing=.9,
    text_wrap=39,
    text_maxlen=202,
    text_anchor_point=(0, 0),
)

#reference text, index 2
magtag.add_text(
        text_font = terminalio.FONT if PLAINFONT else "Arial-12.bdf",
        text_position=(183, 120),
        line_spacing=1.0,
        text_anchor_point=(0, 1),
)

def get_verse(index):
    magtag.set_text("",0,False) #index
    magtag.set_text((verses)[index]["Text"],1,False)
    reference = (verses)[index]["Book"] + " " + (verses)[index]["Chapter"] + ":" + (verses)[index]["Verse"]
    magtag.set_text(reference,2)
     
def get_ref(index):
    return (verses)[index]["Book"] + " " + (verses)[index]["Chapter"] + ":" + (verses)[index]["Verse"]

get_verse(0)

button_colors = ((255, 255, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0))
button_tones = (1047, 1318, 1568, 2093)
verse_count = -1
for a in verses:
    verse_count+=1

print(verse_count)

k = 0
j = 0
while True:
    for i, b in enumerate(magtag.peripherals.buttons):
        if not b.value:
            print("Button %c pressed" % chr((ord("A") + i)))
            print(i)
            magtag.peripherals.neopixel_disable = False
            magtag.peripherals.neopixels.fill(button_colors[i])
            #magtag.peripherals.play_tone(button_tones[i], 0.25) 
            
            #i takes the value of the button, so buttons are [0-3]
            if i == 0:
                j-=1 #go back 1 record
            if i == 1:
                j-=10 #go back 10 records
            if i == 2:
                j+=10 #go forward 1 record
            if i == 3:
                j+=1 #go forward 10 records
            if j < 0: 
                j=0 # if before first record just show the first record and try wifi update
                magtag.peripherals.neopixels[3] = 0x0000FF
                print("Connecting to %s"%secrets["ssid"])
        
                try: 
                    wifi.radio.connect(secrets["ssid"], secrets["password"])
                except : 
                    print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
                    print("Available WiFi networks:")
                    for network in wifi.radio.start_scanning_networks():
                        print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
                                network.rssi, network.channel))
                    wifi.radio.stop_scanning_networks()

                try: 
                    wifi.radio.connect(secrets["ssid"], secrets["password"])
                except ImportError: 
                    print('import error')

                print("Connected to %s!"%secrets["ssid"])
                print("My IP address is", wifi.radio.ipv4_address)

                magtag.peripherals.neopixels[2] = 0x00FF00
                    
                #ipv4 = ipaddress.ip_address("1.1.1.1")
                #print("Ping cloudflare: %f ms" % wifi.radio.ping(ipv4))

                pool = socketpool.SocketPool(wifi.radio)
                requests = adafruit_requests.Session(pool, ssl.create_default_context())

                print("Fetching text from", TEXT_URL)
                response = requests.get(TEXT_URL)
                print("-" * 40)
                print(response)
                print("-" * 40)

                magtag.peripherals.neopixels[1] = 0xFFFF00
                config = response.json()
                print(config)

                print("Fetching json from", config['datasource'])
                webverse = requests.get(config['datasource'])
                print("-" * 40)
                print(webverse.json())
                print("-" * 40)
                magtag.peripherals.neopixels[0] = 0xFF0000
                print("done")

                magtag.peripherals.neopixels[3] = 0xFFFFFF
                magtag.peripherals.neopixels[2] = 0xFFFFFF
                magtag.peripherals.neopixels[1] = 0xFFFFFF
                magtag.peripherals.neopixels[0] = 0xFFFFFF
                    
            if j > verse_count:
                j = verse_count # if after last, show last record
            get_verse(j)
            break
    else:
        magtag.peripherals.neopixel_disable = True
    k+=1
    #magtag.peripherals.neopixels[3] = 0xFF0000
    #magtag.peripherals.neopixels[2] = 0xFFFF00
    #magtag.peripherals.neopixels[1] = 0x00FF00
    #magtag.peripherals.neopixels[0] = 0x0000FF
    time.sleep(.1)
