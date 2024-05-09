# pwm output example   
The number of pwm GPIOs depends on the device.   
You can find the pwm GPIO with the command below.   
```
$ ls /sys/class/pwm/
pwmchip10  pwmchip11  pwmchip5  pwmchip6
```

```
$ sudo -E python3 pwm.py --help
usage: pwm.py [-h] [-c CHIP] [-f FREQ] [-d DUTY] [-p POLARITY]

options:
  -h, --help            show this help message and exit
  -c CHIP, --chip CHIP  PWM chip number
  -f FREQ, --freq FREQ  PWM frequency
  -d DUTY, --duty DUTY  PWM duty
  -p POLARITY, --polarity POLARITY
                        PWM polarity

# Output pwmchip10
$ sudo -E python3 pwm --chip 10
```
