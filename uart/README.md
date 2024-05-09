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

$ sudo -E python3 uart.py --device /dev/ttyS3 --baudrate 115200
device=/dev/ttyS3
baudrate=115200
read 5 bytes: [hello]
```
