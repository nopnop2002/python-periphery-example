# pcf8574 example   

# Hardware requirements
pcf8574x   
Total package sink capability of 80 mA.   

# Wirering
![PCF8574-LED](https://github.com/nopnop2002/python-periphery-example/assets/6020549/6df6f102-461b-442a-9055-7ed9baec833c)

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
