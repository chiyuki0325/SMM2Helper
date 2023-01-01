# https://github.com/Kinnay/Nintendo-File-Formats/wiki/XLINK-File-Format
# Parser for Nintendo's XLNK format
# This format is used by *.bslnk and *.belnk files (sound links and effect links).
# This file is structured as follows:
# Header
# User data table
# Param define table
# Resource asset param table
# Trigger overwrite param table
# Local property name ref table
# Local property enum name ref table
# Direct value table
# Random table
# Curve table
# Curve point table
# Ex region
# Condition table
# Name table

import struct, codecs, numpy
from stream import * # https://github.com/Treeki/CylindricalEarth/blob/master/stream.py

class XLNK:
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
            self.stm = DataInputStream(self.data, LITTLE_ENDIAN)
            self.parse()

    def parse(self):
        # Header
        self.magic = self.stm.read_bytes(0x4)                           # magic
        self.dataSize = self.stm.read_u32()                             # dataSize
        self.version = self.stm.read_u32()                              # version
        self.numResParam = self.stm.read_u32()                          # numResParam
        self.numResAssetParam = self.stm.read_u32()                     # numResAssetParam
        self.numResTriggerOverwriteParam = self.stm.read_u32()          # numResTriggerOverwriteParam
        self.triggerOverwriteParamTablePos = self.stm.read_u32()        # triggerOverwriteParamTablePos
        self.localPropertyNameRefTablePos = self.stm.read_u32()         # localPropertyNameRefTablePos
        self.numLocalPropertyNameRefTable = self.stm.read_u32()         # numLocalPropertyNameRefTable
        self.numLocalPropertyEnumNameRefTable = self.stm.read_u32()     # numLocalPropertyEnumNameRefTable
        self.numDirectValueTable = self.stm.read_u32()                  # numDirectValueTable
        self.numRandomTable = self.stm.read_u32()                       # numRandomTable
        self.numCurveTable = self.stm.read_u32()                        # numCurveTable
        self.numCurvePointTable = self.stm.read_u32()                   # numCurvePointTable
        self.exRegionPos = self.stm.read_u32()                          # exRegionPos
        self.numUser = self.stm.read_u32()                              # numUser
        self.conditionTablePos = self.stm.read_u32()                    # conditionTablePos
        self.nameTablePos = self.stm.read_u32()                         # nameTablePos

        print("%s\tmagic" % (self.magic.decode("utf-8")))
        print("0x%08X\tdataSize" % (self.dataSize))
        print("0x%08X\tversion" % (self.version))
        print("0x%08X\tnumResParam" % (self.numResParam))
        print("0x%08X\tnumResAssetParam" % (self.numResAssetParam))
        print("0x%08X\tnumResTriggerOverwriteParam" % (self.numResTriggerOverwriteParam))
        print("0x%08X\ttriggerOverwriteParamTablePos" % (self.triggerOverwriteParamTablePos))
        print("0x%08X\tlocalPropertyNameRefTablePos" % (self.localPropertyNameRefTablePos))
        print("0x%08X\tnumLocalPropertyNameRefTable" % (self.numLocalPropertyNameRefTable))
        print("0x%08X\tnumLocalPropertyEnumNameRefTable" % (self.numLocalPropertyEnumNameRefTable))
        print("0x%08X\tnumDirectValueTable" % (self.numDirectValueTable))
        print("0x%08X\tnumRandomTable" % (self.numRandomTable))
        print("0x%08X\tnumCurveTable" % (self.numCurveTable))
        print("0x%08X\tnumCurvePointTable" % (self.numCurvePointTable))
        print("0x%08X\texRegionPos" % (self.exRegionPos))
        print("0x%08X\tnumUser" % (self.numUser))
        print("0x%08X\tconditionTablePos" % (self.conditionTablePos))
        print("0x%08X\tnameTablePos" % (self.nameTablePos))

        # Local Property Name Ref Table/Local Property Enum Name Ref Table
        self.stm.seek(self.localPropertyNameRefTablePos)

        self.localPropertyNameRefTable = []
        self.localPropertyEnumNameRefTable = []

        print("Local Property Name Ref Table")
        for i in range(self.numLocalPropertyNameRefTable):
            self.localPropertyNameRefTable.append(self.stm.read_u32())

        print("Local Property Enum Name Ref Table")
        for i in range(self.numLocalPropertyEnumNameRefTable):
            self.localPropertyEnumNameRefTable.append(self.stm.read_u32())

        # Name Table
        self.stm.seek(self.nameTablePos)
        self.nameTable = self.stm.read_bytes(self.dataSize-self.nameTablePos).split(b"\x00")

        print("Name Table")
        for i in self.nameTable:
            print(i.decode("utf-8", errors="ignore"))

        print("")
        for i in self.localPropertyNameRefTable:
            print("0x%08X\t0x%08X\t%s" % (i, i+self.nameTablePos, self.data[i+self.nameTablePos:i+self.nameTablePos+32].decode("utf-8", errors="ignore")))

        print("Done parsing!\n")

bslnkData = open("SLink2DB.bslnk", "rb").read() # Sound link
belnkData = open("ELink2DB.belnk", "rb").read() # Effect link

bslnk = XLNK(bslnkData)                         # Sound link
belnk = XLNK(belnkData)                         # Effect link
