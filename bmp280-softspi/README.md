# BMP280 Software SPI IO example   
Read temperature and pressure from bmp280 with software SPI interface.   

### Hardware requirements
BMP280 with spi interface.   
BMP280 breakout module has modules with 4 pin specifications (for i2c only) and 6 pin specifications (for i2c/SPI), but when using it with SPI, it is necessary to use a 6 pin specification module.   

### Wirering

|BMP280||GPIO||
|:-:|:-:|:-:|:-:|
|Vcc|--|3V3||
|Gnd|--|Gnd||
|SCL|--|SPI SCK|*1|
|SDA|--|SPI MOSI|*1|
|CSB|--|SPI SC|*1|
|SDO|--|SPI MISO|*1|

(*1)   
You can use any gpio.   
However, gpio that can be controlled with Python is required.   

```
$ sudo -E python3 bmp280-softspi.py --help
usage: bmp280-softspi.py [-h] [--sclk SCLK] [--mosi MOSI] [--cs CS] [--miso MISO]
                         [--print PRINT]

options:
  -h, --help     show this help message and exit
  --sclk SCLK    spi sclk gpio
  --mosi MOSI    spi mosi gpio
  --cs CS        spi cs gpio
  --miso MISO    spi miso gpio
  --print PRINT  print debug

$ sudo -E python3 bmp280-softspi.py --sclk 55 --mosi 54 --cs 68 --miso 69
sclk=55
mosi=54
cs=68
miso=69
print=0
chip_id = 0x58 BMP280
Read calibration data
-----------------------
Chip ID     : 0x58
Temperature : 23.16 C
Pressure    : 1005.37 hPa
-----------------------
Chip ID     : 0x58
Temperature : 23.16 C
Pressure    : 1005.33 hPa
-----------------------
Chip ID     : 0x58
Temperature : 23.16 C
Pressure    : 1005.3 hPa
-----------------------
Chip ID     : 0x58
Temperature : 23.16 C
Pressure    : 1005.27 hPa
```
