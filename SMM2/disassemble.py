from capstone import *
from keystone import *

def DISASSEMBLE(ASSEMBLY_HEXSTRING=None, START_ADDRESS=None):
    if ASSEMBLY_HEXSTRING == None or START_ADDRESS == None:
        return None
    else:
        CS = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
        OUT = []
        for (ADDRESS, SIZE, MNEMONIC, OP_STR) in CS.disasm_lite(ASSEMBLY_HEXSTRING, START_ADDRESS):
            OUT.append(MNEMONIC)
        return OUT

def ASSEMBLE(ASSEMBLY_STRING=None, START_ADDRESS=None):
    if ASSEMBLY_STRING == None or START_ADDRESS == None:
        return None
    else:
        KS = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
        return bytes(KS.asm(ASSEMBLY_STRING, START_ADDRESS)[0])
