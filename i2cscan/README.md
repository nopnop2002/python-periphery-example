# i2c device scan example   
Scan for i2c devices.   
```
$ sudo -E python3 i2cscan.py --help
usage: i2cscan.py [-h] [-d DEVICE]

options:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE

$ sudo -E python3 i2cscan.py --device /dev/i2c-3
device=/dev/i2c-3
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- 76 --
```
