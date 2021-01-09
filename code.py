import time
import random
import json
import terminalio
from adafruit_magtag.magtag import MagTag

PLAINFONT = False     # Use built in font if True

magtag = MagTag()
magtag.peripherals.neopixel_disable = True # turn on lights
magtag.set_background(0xFFFFFF)    # set to white background
#magtag.set_background("magtag_bible.bmp")
magtag.peripherals.neopixels.fill(0x000000) # red!
#magtag.refresh()
  
verses = json.loads(open("verses.json").read())

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
                j=0 # if before first record just show the first record 
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
