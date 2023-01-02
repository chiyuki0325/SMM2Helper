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


class CourseArea:
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
            self.AREA_THEME = self.stream.read8()
            self.AUTOSCROLL_TYPE = self.stream.read8()
            self.SCREEN_BOUNDARY_FLAGS = self.stream.read8()
            self.AREA_ORIENTATION = self.stream.read8()
            self.END_LIQUID_HEIGHT = self.stream.read8()
            self.LIQUID_MODE = self.stream.read8()
            self.LIQUID_SPEED = self.stream.read8()
            self.END_LIQUID_HEIGHT = self.stream.read8()
            self.BOUNDARIES = {
                "RIGHT": self.stream.read32(),
                "TOP": self.stream.read32(),
                "LEFT": self.stream.read32(),
                "BOTTOM": self.stream.read32()
            }
            self.AREA_FLAGS = self.stream.read32()
            self.ACTOR_COUNT = self.stream.read32()
            self.OTOASOBI_COUNT = self.stream.read32()
            self.SNAKE_BLOCK_COUNT = self.stream.read32()
            self.CLEAR_DOKAN_COUNT = self.stream.read32()
            self.NOBINOBI_PAKKUN_COUNT = self.stream.read32()
            self.BLOCK_BIKKURI_COUNT = self.stream.read32()
            self.ORBIT_BLOCK_COUNT = self.stream.read32()
            self.stream.skip(0x4)
            self.TILE_COUNT = self.stream.read32()
            self.RAIL_COUNT = self.stream.read32()
            self.ICICLE_COUNT = self.stream.read32()
            self.ACTOR_DATA = self.stream.substream(0x20 * 2600, codecs.BOM_UTF16_BE)
            self.OTOASOBI_DATA = self.stream.substream(0x4 * 300, codecs.BOM_UTF16_BE)
            self.SNAKE_BLOCK_DATA = self.stream.substream(0x3C4 * 5, codecs.BOM_UTF16_BE)
            self.CLEAR_DOKAN_DATA = self.stream.substream(0x124 * 200, codecs.BOM_UTF16_BE)
            self.NOBINOBI_PAKKUN_DATA = self.stream.substream(0x54 * 10, codecs.BOM_UTF16_BE)
            self.BLOCK_BIKKURI_DATA = self.stream.substream(0x2C * 10, codecs.BOM_UTF16_BE)
            self.ORBIT_BLOCK_DATA = self.stream.substream(0x2C * 10, codecs.BOM_UTF16_BE)
            self.TILE_DATA = self.stream.substream(0x4 * 4000, codecs.BOM_UTF16_BE)
            self.RAIL_DATA = self.stream.substream(0xC * 1500, codecs.BOM_UTF16_BE)
            self.ICICLE_DATA = self.stream.substream(0x4 * 300, codecs.BOM_UTF16_BE)
            self.ACTORS = []
            for i in range(self.ACTOR_COUNT):
                self.ACTORS.append(Actor(self.ACTOR_DATA.read(0x20, codecs.BOM_UTF16_BE)))

    def save(self):
        self.stream = streams.StreamOut()
        self.stream.byteorder = codecs.BOM_UTF16_LE


class Actor:
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
            self.POSITION = {
                "X": self.stream.read32() / 10,
                "Y": self.stream.read32() / 10
            }
            self.stream.skip(0x2)
            self.SIZE = {
                "X": self.stream.read8(),
                "Y": self.stream.read8()
            }
            self.FLAGS = [
                self.stream.read32(),
                self.stream.read32()
            ]
            self.EXTENDED_DATA = self.stream.read32()
            self.TYPES = {
                "PARENT": [
                    self.stream.read8(),
                    self.stream.read8()
                ],
                "CHILD": [
                    self.stream.read8(),
                    self.stream.read8()
                ]
            }
            self.LINK_ID = self.stream.read16()
            self.OTOASOBI_ID = self.stream.read16()

    def save(self):
        self.stream = streams.StreamOut()
        self.stream.byteorder = codecs.BOM_UTF16_LE
