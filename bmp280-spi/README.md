# BMP280 Hardware SPI IO example   
Read temperature and pressure from bmp280 with hardware SPI interface.   

### Hardware requirements
BMP280 with spi interface.   
BMP280 breakout module has modules with 4 pin specifications (for i2c only) and 6 pin specifications (for i2c/SPI), but when using it with SPI, it is necessary to use a 6 pin specification module.   

### Wirering

|BMP280||GPIO||
|:-:|:-:|:-:|:-:|
|Vcc|--|3V3||
|Gnd|--|Gnd||
|SCL|--|SPI SCK||
|SDA|--|SPI MOSI||
|CSB|--|SPI SC||
|SDO|--|SPI MISO||



```
$ sudo -E python3 bmp280-spi.py --help
usage: bmp280-spi.py [-h] [-d DEVICE] [-m MODE] [-s SPEED] [-p PRINT]

options:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        device file name
  -m MODE, --mode MODE  spi mode
  -s SPEED, --speed SPEED
                        spi clock speed
  -p PRINT, --print PRINT
                        print debug

$ sudo -E python3 bmp280-spi.py --device /dev/spidev0.0
device=/dev/spidev0.0
mode=0
speed=1000000
print=0
chip_id = 0x58 BMP280
Check Register
Read calibration data
-----------------------
Chip ID     : 0x58
Temperature : 23.39 C
Pressure    : 1004.89 hPa
-----------------------
Chip ID     : 0x58
Temperature : 23.38 C
Pressure    : 1004.92 hPa
-----------------------
Chip ID     : 0x58
Temperature : 23.38 C
Pressure    : 1004.88 hPa
```
