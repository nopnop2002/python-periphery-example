# python-periphery-example
python-periphery example code.   
python-periphery is a python library that can handle GPIO, onboard LED, SPI, and i2c.   
It is a very versatile library and highly portable.   
The downside is that there is less example python code.   
I used this to check the operation of the LuckFox Pico board, which uses the Rockchip RV1103/RV1106 chip.   
![luckfox-pico-1](https://github.com/nopnop2002/python-periphery-example/assets/6020549/c0ba3c08-8cd4-4488-ae6e-5d16fbf36b3d)
![luckfox-pico-2](https://github.com/nopnop2002/python-periphery-example/assets/6020549/536b585a-6695-4139-a97d-2c5aded58630)


# Installation

```Shell
sudo apt update
sudo apt install git python3-pip python3-setuptools
git clone https://github.com/vsergeev/python-periphery.git
cd python-periphery/
python3 -m pip install python-periphery
```


# gpio blink example   
Blinking gpio.
```
$ sudo -E python3 gpio.py --help
usage: gpio.py [-h] [-g GPIO]

options:
  -h, --help            show this help message and exit
  -g GPIO, --gpio GPIO  GPIO to blink

$ sudo -E python3 leds.py -g 1
```


# led blink example   
Blinking on-board led.   
The number of onboard LEDs depends on the device.   
You can find the onboard LED with the command below.   
```
$ ls /sys/class/leds/
default-on  led0  led1  mmc0
```

```
$ sudo -E python3 leds.py --help

usage: leds.py [-h] [-d DEVICE]

options:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        Onboard LED device


$ sudo -E python3 leds.py -d led0
```

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

$ sudo -E python3 bmp280-spi.py -d /dev/spidev0.0
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




# i2c device scan example   
Scan for i2c devices.   
```
$ sudo -E python3 i2cscan.py --help
usage: i2cscan.py [-h] [-d DEVICE]

options:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE

$ sudo -E python3 i2cscan.py -d /dev/i2c-3
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


$ sudo -E python3 bmp180-i2c.py -d /dev/i2c-3
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

$ sudo -E python3 bmp280-i2c.py -d /dev/i2c-3
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


# UART IO example   

### Hardware requirements
USB-TTL converter like CH340.

### Wirering

|CH340||GPIO||
|:-:|:-:|:-:|:-:|
|Gnd|--|Gnd||
|TX|--|RX GPIO||
|RX|--|TX GPIO||


```
$ sudo -E python3 uart.py --help
usage: uart.py [-h] [-d DEVICE] [-b BAUDRATE] [-p PRINT]

options:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        device file name
  -b BAUDRATE, --baudrate BAUDRATE
                        baudrate
  -p PRINT, --print PRINT
                        print debug

$ sudo -E python3 uart.py -d /dev/ttyS3 -b 115200
device=/dev/ttyS3
baudrate=115200
read 5 bytes: [hello]
```
