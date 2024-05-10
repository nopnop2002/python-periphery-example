# mcp23019 example   

# Hardware requirements
mcp23017   

# Wirering
![MCP23017-LED](https://github.com/nopnop2002/python-periphery-example/assets/6020549/dca4f244-70a4-4a6a-ac4f-6f2c1de329f7)


```
$ sudo -E python3 main.py --help
usage: main.py [-h] [-d DEVICE] [-a ADDR] [--delay DELAY]

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        device file name
  -a ADDR, --addr ADDR  i2c address
  --delay DELAY         Delay time

$ sudo -E python3 main.py --device /dev/i2c-1
```
