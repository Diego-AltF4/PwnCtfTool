If we fuzzy the binary a bit we can see how function 3 is vulnerable to a buffer overflow:


![vuln2_1](https://user-images.githubusercontent.com/55554183/154162258-3602aad9-fa6b-4ace-b303-002e8b49be33.png)

Our target function is RCE since it launches a shell:

![Pasted image 20220215214916](https://user-images.githubusercontent.com/55554183/154162332-0953aee5-2e8b-4f5c-8811-b2252bd53637.png)

Having this information we can now use the tool, but first of all let's recapitulate:

1. We need to enter option 3, so we need to use the `--before` parameter. 
Let's create a file (with any name you want) containing only the desired option `3`:
`echo "3" > before2.txt`.

2. We need to indicate the function we want to jump to, in our case `rce`.
3. Add the `--shell` option to get a shell.

Final command:

```pyton3
python3 ../../PwnCtfTool.py --before before2.txt -f vuln2 -t rce --shell
```
![Pasted image 20220215215350](https://user-images.githubusercontent.com/55554183/154162373-968acd3a-d86b-4e20-9815-4303478f01db.png)
