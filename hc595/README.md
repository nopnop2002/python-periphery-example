# hc595 (ShiftRegister) example   

# Hardware requirements
hc595   
Depending on the manufacturer, the model number may be SN54HC595/SL74HC595/SN74HC595.   

# Wirering
![74HC595-LED](https://github.com/nopnop2002/python-periphery-example/assets/6020549/24723718-569d-4574-a460-051f6f747afd)

```
$ sudo -E python3 main.py --help
usage: main.py [-h] [--data DATA] [--latch LATCH] [--clock CLOCK] [--delay DELAY]

optional arguments:
  -h, --help     show this help message and exit
  --data DATA    DATA GPIO
  --latch LATCH  LATCH GPIO
  --clock CLOCK  CLOCK GPIO
  --delay DELAY  Delay time


$ python3 main.py --data 23 --latch 24 --clock 25
```
