import codecs
from SMM2 import streams


class Course:
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
            self.HEADER = CourseHeader(self.stream.read(0x200, codecs.BOM_UTF16_BE))
            # self.OVERWORLD = CourseArea(self.stream.read(0x2DEE0, codecs.BOM_UTF16_BE))
            # self.SUBWORLD = CourseArea(self.stream.read(0x2DEE0, codecs.BOM_UTF16_BE))

    def save(self):
        self.stream = streams.StreamOut()
        self.stream.byteorder = codecs.BOM_UTF16_LE


class CourseHeader:
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
            self.START_POSITION = {
                "Y": self.stream.read8()
            }
            self.GOAL_POSITION = {
                "Y": self.stream.read8(),
                "X": self.stream.read16()
            }
            self.TIME_LIMIT = self.stream.read16()
            self.CC_COUNT = self.stream.read16()
            self.SAVE_DATE = {
                "YEAR": self.stream.read16(),
                "MONTH": self.stream.read8(),
                "DAY": self.stream.read8()
            }
            self.SAVE_TIME = {
                "HOUR": self.stream.read8(),
                "MINUTE": self.stream.read8()
            }
            self.AUTOSCROLL_SPEED = self.stream.read8()
            self.CC_CATEGORY = self.stream.read8()
            self.CC_HASH = self.stream.read32()
            self.GAME_VERSION = self.stream.read32()
            self.MANAGEMENT_FLAGS = self.stream.read32()
            self.CC_TRY_COUNT = self.stream.read32()
            self.CC_TIME = self.stream.read32()
            self.CREATION_ID = self.stream.read32()
            self.UPLOAD_ID = self.stream.read64()
            self.COMPLETION_FLAGS = self.stream.read32()
            self.stream.skip(0xBC)
            self.stream.skip(0x1)
            self.GAME_STYLE = self.stream.read(0x2)
            self.stream.skip(0x1)
            self.NAME = self.stream.read(0x42, codecs.BOM_UTF16_BE).decode("utf-16-le", errors="ignore").rstrip('\x00')
            self.DESCRIPTION = self.stream.read(0xCA, codecs.BOM_UTF16_BE).decode("utf-16-le", errors="ignore").rstrip(
                '\x00')

    def save(self):
        self.stream = streams.StreamOut()
        self.stream.byteorder = codecs.BOM_UTF16_LE
