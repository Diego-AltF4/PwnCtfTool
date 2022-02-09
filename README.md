##  Tool for ret2win challenges.  
It can be used both locally and remotely (indicating IP and port). It automatically finds the offset to the Instruction Pointer stored in the stack. 

It can be configured to return a shell. By default, it prints the data received by the connection (possible flag). 
It also allows to display the offset to the instruction pointer in the stack and supports x86 architecture in both 32-bit and 64-bit. 
It can be used to debug the exploit with GDB. 

Basic usage:

````./PwnCtfTool.py -f vuln.bin -t flag_func````

```
Auto PWN tool for CTF
optional arguments:
  -h, --help show this help message and exit
  -vv Max Verbose (debug)
  -v Verbose (info)
  -g Attach GDB
  -f FILE File to PWN
  -t TARGET Target Function
  --offset Print offset Instruction Pointer
  --shell Stay interactive
  --remote Exploit remote server
```

Installation:
```
git clone https://github.com/Diego-AltF4/PwnCtfTool.git
cd ./PwnCtfTool
pip3 install -r requirements.txt
./PwnCtfTool.py
```
If the tool isn't working due to corefile errors you may solve them by using this command:
```
sudo bash -c 'echo core > /proc/sys/kernel/core_pattern'
```
It changes the content of the core_pattern file so that corefiles get always generated with the name "core". This is necessary since the tool accesses the corefile using that name.

**Note:** It is recommended to save a backup of the /proc/sys/kernel/core_pattern file before using the command abovementioned, specially if you have other programs working with corefiles.


## Acknowledgements

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/dbd4">
      <img src="https://pbs.twimg.com/profile_images/1380667733449306113/7rJEid1j_400x400.jpg" width="100px;" alt=""/><br/>
      <sub><b>David Billhardt</b></sub></a><br/>
    </td>
  </tr>
</table>

Created by [DiegoAltF4](https://twitter.com/Diego_AltF4) and [Dbd4](https://twitter.com/DavidBillhardt)

