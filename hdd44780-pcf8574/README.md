# hdd44780-pcf8574 example   
I took [this](https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/) code as a reference and ported it to the python-periphery.   

# Hardware requirements
- hdd44780 LCD.   
 Usually called 1602LCD/1604LCD.   

- pcf8574   
 Operating supply voltage is 2.5 V to 6V.   
 The i2c TTL level needs to match the host.   

# Wirering for 5V module
![GPIO_LCD+PCF8574-5V](https://github.com/nopnop2002/python-periphery-example/assets/6020549/e627ab31-9af1-4f42-87da-a0dfec66f8c4)

# Wirering for 3V3 module
![GPIO_LCD+PCF8574-3V3](https://github.com/nopnop2002/python-periphery-example/assets/6020549/6d7fcdfe-d48c-4208-a92b-1e23a864d136)


```
$ sudo -E python3 ./main.py --help
usage: main.py [-h] [--device DEVICE] [--addr ADDR] [--text1 TEXT1] [--text2 TEXT2] [--text3 TEXT3]
               [--text4 TEXT4] [--texts [TEXTS ...]]

options:
  -h, --help           show this help message and exit
  --device DEVICE      device file name
  --addr ADDR          i2c address
  --text1 TEXT1        text of line1
  --text2 TEXT2        text of line2
  --text3 TEXT3        text of line3
  --text4 TEXT4        text of line4
  --texts [TEXTS ...]  a list of text

## for 1602 LCD
$ sudo -E python3 main.py --device /dev/i2c-3 --addr 0x20 --text1 'Hello!!' --text2 'World!!'

$ sudo -E python3 main.py --device /dev/i2c-3 --addr 0x20 --texts 'Hello!!' 'World!!'

## for 1604 LCD
$ sudo -E python3 main.py --device /dev/i2c-3 --addr 0x20 --text1 'Hello!!' --text2 'World!!' --text3 'Good!!' --text4 'Bye!!'

$ sudo -E python3 main.py --device /dev/i2c-3 --addr 0x20 --texts 'Hello!!' 'World!!' 'Good!!' 'Bye!!'

## for clear all text
$ sudo -E python3 main.py --device /dev/i2c-3 --addr 0x20
```
