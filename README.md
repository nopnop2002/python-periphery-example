# python-periphery-example
python-periphery example code.   
python-periphery is a python library that can handle GPIO, onboard LED, SPI, and i2c.   
It is a very versatile library and highly portable.   
The downside is that there is less example python code.   

# Installation

```Shell
sudo apt update
sudo apt install git python3-pip python3-setuptools
git clone https://github.com/vsergeev/python-periphery.git
cd python-periphery/
python3 -m pip install python-periphery
```


# gpio example   
Toggle gpio.
```
$ sudo -E python3 gpio.py --help
usage: gpio.py [-h] [-g GPIO]

options:
  -h, --help            show this help message and exit
  -g GPIO, --gpio GPIO  GPIO to blink

$ sudo -E python3 leds.py -g 1
```


# leds example   
Toggle on-board led.   
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

# spi IO example   
Read temperature and humidity from bmp280 with spi interface.   

### Hardware requirements
BMP280 with spi interface.

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
```



# i2c IO example   
Read temperature and humidity from bmp280 with i2c interface.   

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
```



