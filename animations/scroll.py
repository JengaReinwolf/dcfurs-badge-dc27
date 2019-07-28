"""Scrolling Text"""
import dcfurs
import settings

## Font Data
font5var = {'A':bytearray([0x1E,0x05,0x05,0x1E,0x00]),
            'B':bytearray([0x1F,0x15,0x15,0x0E,0x00]),
            'C':bytearray([0x0E,0x11,0x11,0x11,0x00]),
            'D':bytearray([0x1F,0x11,0x11,0x0E,0x00]),
            'E':bytearray([0x1F,0x15,0x15,0x11,0x00]),
            'F':bytearray([0x1F,0x05,0x05,0x01,0x00]),
            'G':bytearray([0x1F,0x11,0x15,0x1D,0x00]),
            'H':bytearray([0x1F,0x04,0x04,0x1F,0x00]),
            'I':bytearray([0x11,0x1F,0x11,0x00]),
            'J':bytearray([0x18,0x11,0x11,0x1F,0x00]),
            'K':bytearray([0x1F,0x04,0x07,0x1C,0x00]),
            'L':bytearray([0x1F,0x10,0x10,0x00]),
            'M':bytearray([0x1F,0x01,0x1F,0x01,0x1F,0x00]),
            'N':bytearray([0x1F,0x01,0x02,0x1F,0x00]),
            'O':bytearray([0x0E,0x11,0x11,0x0E,0x00]),
            'P':bytearray([0x1F,0x05,0x05,0x07,0x00]),
            'Q':bytearray([0x1F,0x15,0x3D,0x11,0x1F,0x00]),
            'R':bytearray([0x1F,0x05,0x1D,0x07,0x00]),
            'S':bytearray([0x16,0x15,0x15,0x1D,0x00]),
            'T':bytearray([0x01,0x01,0x1F,0x01,0x01,0x00]),
            'U':bytearray([0x0F,0x10,0x10,0x0F,0x00]),
            'V':bytearray([0x1F,0x10,0x08,0x07,0x00]),
            'W':bytearray([0x0F,0x10,0x1C,0x10,0x0F,0x00]),
            'X':bytearray([0x1C,0x04,0x1F,0x04,0x07,0x00]),
            'Y':bytearray([0x03,0x04,0x1C,0x04,0x03,0x00]),
            'Z':bytearray([0x19,0x15,0x13,0x11,0x00]),
            'a':bytearray([0x18,0x14,0x1C,0x00]),
            'b':bytearray([0x1F,0x14,0x18,0x00]),
            'c':bytearray([0x08,0x14,0x14,0x00]),
            'd':bytearray([0x18,0x14,0x1F,0x00]),
            'e':bytearray([0x0C,0x1A,0x14,0x00]),
            'f':bytearray([0x1E,0x05,0x01,0x00]),
            'g':bytearray([0x16,0x1D,0x0F,0x00]),
            'h':bytearray([0x1F,0x04,0x18,0x00]),
            'i':bytearray([0x05,0x1D,0x00]),
            'j':bytearray([0x11,0x1D,0x00]),
            'k':bytearray([0x1F,0x0C,0x14,0x00]),
            'l':bytearray([0x1F,0x00]),
            'm':bytearray([0x1C,0x04,0x18,0x04,0x18,0x00]),
            'n':bytearray([0x1C,0x04,0x18,0x00]),
            'o':bytearray([0x08,0x14,0x08,0x00]),
            'p':bytearray([0x1E,0x0A,0x06,0x00]),
            'q':bytearray([0x0C,0x0A,0x3E,0x10,0x00]),
            'r':bytearray([0x1C,0x04,0x04,0x00]),
            's':bytearray([0x14,0x12,0x0A,0x00]),
            't':bytearray([0x02,0x1F,0x02,0x00]),
            'u':bytearray([0x0C,0x10,0x1c,0x00]),
            'v':bytearray([0x1C,0x10,0x0C,0x00]),
            'w':bytearray([0x1C,0x10,0x0C,0x10,0x0C,0x00]),
            'x':bytearray([0x10,0x0C,0x18,0x04,0x00]),
            'y':bytearray([0x12,0x14,0x0E,0x00]),
            'z':bytearray([0x1A,0x16,0x12,0x00]),
            ' ':bytearray([0x00,0x00,0x00]),
            ':':bytearray([0x0A,0x00]),
            ';':bytearray([0x10,0x0A,0x00]),
            '.':bytearray([0x10,0x10,0x00]),
            ',':bytearray([0x10,0x18,0x00]),
            '!':bytearray([0x17,0x17,0x00]),
            '?':bytearray([0x01,0x15,0x02,0x00])}

class scroll:
    color_map = [
        0xe0, # Red
        0xe8, # Orange
        0xfc, # Yellow
        0x1c, # Green
        0x03, # Blue
        0x43  # Purple
    ]

    def __init__(self, text=None):
        if text:
            self.text = text
        else:
            self.text = settings.banner
        
        self.interval = 250
        self.scrollbuf = bytearray([0x00, 0x00, 0x00, 0x00])
        self.colorbuf = bytearray([0x00, 0x00, 0x00, 0x00])
        self.shift = 0
        
        coloridx = 0
        for char in self.text:
            if char in font5var:
                self.scrollbuf += font5var[char]
                self.colorbuf += bytearray([self.color_map[coloridx]] * len(font5var[char]))
                coloridx = (coloridx + 1) % len(self.color_map)
    
    def draw(self):
        dcfurs.clear()
        for x in range(0, dcfurs.ncols):
            colbits = self.scrollbuf[(self.shift + x) % len(self.scrollbuf)]
            color = self.colorbuf[(self.shift + x) % len(self.colorbuf)]
            for y in range(0, dcfurs.nrows):
                if (colbits & (1 << y)) != 0:
                    dcfurs.set_pixel(x,y,color)
        self.shift = (self.shift + 1) % len(self.scrollbuf)

