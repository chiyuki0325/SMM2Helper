import codecs
import enum
from SMM2 import streams

class Save:
    def __init__(self, data=None):
        if not data:
            return None
        else:
            self.load(data)

    def load(self, data=None):
        if not data:
            return None
        else:
            self.data = data
            self.stream = streams.StreamIn(self.data)
            self.stream.byteorder = codecs.BOM_UTF16_LE
            self.NAME = self.stream.read(20, codecs.BOM_UTF16_BE).decode("utf-16-le", errors="ignore").rstrip('\x00')
            self.stream.seek(0x50)
            self.MII_DATA = self.stream.read(0x58, codecs.BOM_UTF16_BE)
            self.stream.seek(0xB920)
            self.own_courses = []
            self.unkown_courses = []
            self.downloaded_courses = []
            self.stream.seek(0xB920)
            for i in range(0x3C):
                self.own_courses.append([self.stream.read8(), SLOT_STATUS(self.stream.read8())])
                self.stream.skip(0x6)

            for i in range(0x3C):
                self.unkown_courses.append([self.stream.read8(), SLOT_STATUS(self.stream.read8())])
                self.stream.skip(0x6)

            for i in range(0x3C):
                self.downloaded_courses.append([self.stream.read8(), SLOT_STATUS(self.stream.read8())])
                self.stream.skip(0x6)

class SLOT_STATUS(enum.Enum):
    AVAILABLE = 0
    OCCUPIED = 1
