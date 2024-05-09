# hdd44780 example   

```
$ sudo -E python3 hdd44780.py --help
usage: hdd44780.py [-h] [--rs RS] [--enable ENABLE] [--d4 D4] [--d5 D5] [--d6 D6] [--d7 D7] [--text1 TEXT1] [--text2 TEXT2]
                   [--text3 TEXT3] [--text4 TEXT4] [--clear CLEAR]

optional arguments:
  -h, --help       show this help message and exit
  --rs RS          RS GPIO
  --enable ENABLE  ENABLE GPIO
  --d4 D4          D4 GPIO
  --d5 D5          D4 GPIO
  --d6 D6          D4 GPIO
  --d7 D7          D4 GPIO
  --text1 TEXT1    text of line1
  --text2 TEXT2    text of line2
  --text3 TEXT3    text of line3
  --text4 TEXT4    text of line4
  --clear CLEAR    clear all text

## for 1602 LCD
$ sudo -E python3 hdd44780.py --rs 23 --enable 24 --d4 14 --d5 15 --d6 17 --d7 18 --text1 "Hello!" --text2 "World!"

## for 1604 LCD
$ sudo -E python3 hdd44780.py --rs 23 --enable 24 --d4 14 --d5 15 --d6 17 --d7 18 --text1 "Hello!" --text2 "World!" --text3 "Good!" --text4 "Bye!"

## for clear all text
$ sudo -E python3 hdd44780.py --rs 23 --enable 24 --d4 14 --d5 15 --d6 17 --d7 18 --clear
