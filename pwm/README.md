# pwm output example   
The hardware PWM provided by the Linux file system consists of a chip number and a channel number.   
The PWM chip number can be found with the command below.   
```
$ ls /sys/class/pwm/
pwmchip10  pwmchip11  pwmchip5  pwmchip6
```

In the above example, we can see that the PWM chip number is 10/11/5/6.

One PWM chip supports multiple PWM channels.   
You can check the number of PWM channels with the following command.   
```
$ cat /sys/class/pwm/pwmchip10/npwm
1

$ cat /sys/class/pwm/pwmchip11/npwm
1

$ cat /sys/class/pwm/pwmchip5/npwm
1

$ cat /sys/class/pwm/pwmchip6/npwm
1
```

In the above example, we can see that all PWM chips have only one channel.

```
$ sudo -E python3 pwm.py --help
usage: pwm.py [-h] [-c CHIP] [-f FREQ] [-d DUTY] [-p POLARITY]

options:
  -h, --help            show this help message and exit
  -c CHIP, --chip CHIP  PWM chip number
  -n CHANNELL, --channell CHANNELL
                        PWM channell number
  -f FREQ, --freq FREQ  PWM frequency
  -d DUTY, --duty DUTY  PWM duty
  -p POLARITY, --polarity POLARITY
                        PWM polarity

# Output pwmchip10
$ sudo -E python3 pwm --chip 10
```
