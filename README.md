#  Tool for ret2win challenges.  

```
    ____                 ________  __________            __
   / __ \_      ______  / ____/ /_/ __/_  __/___  ____  / /
  / /_/ / | /| / / __ \/ /   / __/ /_  / / / __ \/ __ \/ / 
 / ____/| |/ |/ / / / / /___/ /_/ __/ / / / /_/ / /_/ / /  
/_/     |__/|__/_/ /_/\____/\__/_/   /_/  \____/\____/_/   
                                                           
                By: DiegoAltF4 and Dbd4

```


## Introduction

It can be used both locally and remotely (indicating IP and port). It automatically finds the offset to the Instruction Pointer stored in the stack. 

Furthermore, it can be configured to return a shell. By default, it prints the data received by the connection (possible flag). 

It also allows to display the offset to the instruction pointer in the stack and supports x86 architecture in both 32-bit and 64-bit and it can be used to debug the exploit with GDB. 


## Parameters

| Parameter    | Information |
|:-------------|:-------------|
| *-f*          | indicates the binary to be exploited (**mandatory parameter**). |
| *-t*     | indicates the target function we want to jump to (**mandatory parameter**). |
| *-v* | indicates verbose info mode. |
| *-vv*         | indicates maximum verbosity value, debug mode. |
| *-g* | allows attaching GDB for debugging purposes. |
| *--offset* | prints the offset to the Instruction Pointer. |
| *--shell* | allows an interactive session to be maintained after exploitation. |
| *--remote* | allows to exploit on a remote server. |
| *--before* | allows you to add content from a file before the payload. |
| *--after* | allows you to add content from a file after the payload. |

## Basic usage:

````bash
./PwnCtfTool.py -f vuln.bin -t flag_func
````


## Advanced use with examples


In this part, we will explain the different uses of the tool with examples. We have uploaded a list of vulnerable binaries and we will update this list as we include new options in the tool.
To make it easier to find the information we will indicate the parameters used in the final command that allows us to exploit the binary. In addition, we are going to classify the difficulty of the challenges using the 💣 emoji. A single bomb means that it is very easy, five bombs indicates that the difficulty is very high. 
For each challenge we have included a small writeup that explains in much more detail how we can get to the solution. 


### Vulnerable binary resolution 1


> Using the `-f` `-t` `--shell` `--offset` parameters 

For all the explanation you can read the writeup:

* [**Vuln1**](Example_binaries/Example1/) 💣

**Final command:**

```bash
python3 ../../PwnCtfTool.py -f ./vuln1 -t win --shell --offset
```


### Vulnerable binary resolution 2

> Using `-f` `-t` `--before` `--shell` parameters 

For all the explanation you can read the writeup:

* [**Vuln2**](Example_binaries/Example2/) 💣

**Final command:**

```bash
python3 ../../PwnCtfTool.py --before before2.txt -f vuln2 -t rce --shell
```

## Installation:

```bash
git clone https://github.com/Diego-AltF4/PwnCtfTool.git
cd ./PwnCtfTool
pip3 install -r requirements.txt
chmod +x PwnCtfTool.py
./PwnCtfTool.py
```


## Acknowledgements

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/dbd4">
      <img src="https://pbs.twimg.com/profile_images/1496195726078091268/IQeUbsxf_400x400.jpg" width="100px;" alt=""/><br/>
      <sub><b>David Billhardt</b></sub></a><br/>
    </td>
  </tr>
</table>

Created by [DiegoAltF4](https://twitter.com/Diego_AltF4) and [Dbd4](https://twitter.com/DavidBillhardt)

