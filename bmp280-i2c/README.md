# BMP280 i2c IO example   
Read temperature and pressure from bmp280 with i2c interface.   

### Hardware requirements
BMP280 with i2c interface.

### Wirering

|BMP280||GPIO||
|:-:|:-:|:-:|:-:|
|Vcc|--|3V3||
|Gnd|--|Gnd||
|SCL|--|i2c SCL||
|SDA|--|i2c SDA||
|CSB|--|3V3||
|SDO|--|GND/3V3|*1|

(*1)   
i2c address selection.   
Gnd:0x76/3V3:0x77   


```
$ sudo -E python3 bmp280-i2c.py --help
usage: bmp280-i2c.py [-h] [-d DEVICE] [-a ADDR] [-p PRINT]

options:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        device file name
  -a ADDR, --addr ADDR  i2c address
  -p PRINT, --print PRINT
                        print debug

$ sudo -E python3 bmp280-i2c.py --device /dev/i2c-3
device=/dev/i2c-3
addr=0x76
chip_id = 0x58 BMP280
-----------------------
Chip ID     : 0x58
Temperature : 22.29 C
Pressure    : 1004.73 hPa
-----------------------
Chip ID     : 0x58
Temperature : 22.29 C
Pressure    : 1004.67 hPa
-----------------------
Chip ID     : 0x58
Temperature : 22.29 C
Pressure    : 1004.71 hPa
-----------------------
Chip ID     : 0x58
Temperature : 22.28 C
Pressure    : 1004.69 hPa
```
