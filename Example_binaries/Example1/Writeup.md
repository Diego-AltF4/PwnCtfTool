If we list the functions of the binary, we can see a very interesting "win":

![vuln1_1](https://user-images.githubusercontent.com/55554183/154161588-593a6e61-64c0-4707-8549-a0e4570749d8.png)

If we inspect the function, we can see that it makes a system call by passing `/bin/sh`.

![vuln1_2](https://user-images.githubusercontent.com/55554183/154161773-c9a51641-c100-4ec0-8c9b-e3428a5271c4.png)

So, we know that we want to jump to the win function and we want to get a shell. That's all we need to use the tool:

```python3
python3 ../../PwnCtfTool.py -f ./vuln1 -t win --shell
```
![vuln1_3](https://user-images.githubusercontent.com/55554183/154161848-3884f16d-7252-4ab1-bc08-53417e5a1a6f.png)

We can also see the offset to the IP with the `--offset` parameter:


![vuln1_4](https://user-images.githubusercontent.com/55554183/154161942-cd65be15-4b84-4cbe-85d9-b98b3c266cf0.png)

```python3
python3 ../../PwnCtfTool.py -f ./vuln1 -t win --shell --offset
```

The offset is 120.
