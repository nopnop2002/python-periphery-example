# BMP180 i2c IO example   
Read temperature and pressure from bmp180 with i2c interface.   

### Hardware requirements
BMP180 with i2c interface.

### Wirering

|BMP180||GPIO||
|:-:|:-:|:-:|:-:|
|3V3|--|3V3||
|ECC|--|N/C||
|CLR|--|N/C||
|SCL|--|i2c SCL||
|SDA|--|i2c SDA||
|5V|--|N/C||
|GND|--|Gnd||


```
$ sudo -E python3 bmp180-i2c.py --help
usage: bmp180-i2c.py [-h] [-d DEVICE] [-a ADDR]

options:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        device file name
  -a ADDR, --addr ADDR  i2c address


$ sudo -E python3 bmp180-i2c.py --device /dev/i2c-3
device=/dev/i2c-3
addr=0x77
Chip ID          : 85
Version          : 2
-----------------------
Chip ID     : 0x55
Temperature : 24.6 C
Pressure    : 1012.32 hPa
-----------------------
Chip ID     : 0x55
Temperature : 24.6 C
Pressure    : 1012.31 hPa
-----------------------
Chip ID     : 0x55
Temperature : 24.6 C
Pressure    : 1012.31 hPa
-----------------------
Chip ID     : 0x55
Temperature : 24.6 C
Pressure    : 1012.32 hPa
-----------------------
```
