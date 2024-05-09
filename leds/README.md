# on-board led blink example   
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

# Blink /sys/class/leds/led0
$ sudo -E python3 leds.py --device led0
```
