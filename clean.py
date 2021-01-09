import json
import terminalio
from adafruit_magtag.magtag import MagTag


magtag = MagTag()
magtag.peripherals.neopixel_disable = True # turn off lights

magtag.set_background("bmps\magtag_bible.bmp")
verses = json.loads(open("verses.json").read())

# main text, index 0
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
    text_position=(10, 10),
    line_spacing=1.0,
    text_wrap=35,
    text_maxlen=130,
    text_anchor_point=(0, 0),
)

#reference text, index 2
# button labels, add all 4 in one loop
magtag.add_text(
        text_font = terminalio.FONT if PLAINFONT else "Arial-12.bdf",
        text_position=(150, 110),
        line_spacing=1.0,
        text_anchor_point=(0, 1),
)

#set verse txt
magtag.set_test("Hello World",0,False)
magtag.set_text((verses)["Text"], 1)

Ref = (verses)["Book"] + " " + (verses)["Chapter"] + ":" + (versus)["Verse"]

magtag.set_text((Ref, 2, False)