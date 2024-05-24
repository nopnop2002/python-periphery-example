# hdd44780-hc595 example   
I took [this](https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/) code as a reference and ported it to the python-periphery.   

# Hardware requirements
- hdd44780 LCD.   
 Usually called 1602LCD/1604LCD.   

- hc595   
 Depending on the manufacturer, the model number may be SN54HC595/SL74HC595/SN74HC595.   

# Wirering for 5V module
![GPIO_LCD-HC595_5V](https://github.com/nopnop2002/python-periphery-example/assets/6020549/a0396c7b-614c-488e-b310-c122cc5c4c5a)

# Wirering for 3V3 module
![GPIO_LCD-HC595_3V3](https://github.com/nopnop2002/python-periphery-example/assets/6020549/c269fcb1-e602-49fd-8bbc-a013a28a1418)

```
sudo -E python3 main.py --help
usage: main.py [-h] [--data DATA] [--latch LATCH] [--shift SHIFT] [--text1 TEXT1] [--text2 TEXT2] [--text3 TEXT3]
               [--text4 TEXT4] [--texts [TEXTS ...]]

options:
  -h, --help           show this help message and exit
  --data DATA          DATA GPIO
  --latch LATCH        LATCH GPIO
  --shift SHIFT        SHIFT GPIO
  --text1 TEXT1        text of line1
  --text2 TEXT2        text of line2
  --text3 TEXT3        text of line3
  --text4 TEXT4        text of line4
  --texts [TEXTS ...]  a list of text

## for 1602 LCD
$ sudo -E python3 main.py --data 70 --latch 71 --shift 72 --text1 'Hello!!' --text2 'World!!'

$ sudo -E python3 main.py --data 70 --latch 71 --shift 72 --texts 'Hello!!' 'World!!'

## for 1604 LCD
$ sudo -E python3 main.py --data 70 --latch 71 --shift 72 --text1 'Hello!!' --text2 'World!!' --text3 'Good!!' --text4 'Bye!!'

$ sudo -E python3 main.py --data 70 --latch 71 --shift 72 --texts 'Hello!!' 'World!!' 'Good!!' 'Bye!!'

## for clear all text
$ sudo -E python3 main.py --data 70 --latch 71 --shift 72
```
