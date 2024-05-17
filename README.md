# python-periphery-example
python-periphery example code.   
python-periphery is a python library that can handle GPIO, onboard LED, SPI, i2c and UART.   
It is a very versatile library and highly portable.   
This library can also be used in the buildroot environment.   
The downside is that there is less example python code.   
This library is available for these Linux boards.   

- LuckFox Pico board using Rockchip RV1103/RV1106 chips.   
![luckfox-pico-1](https://github.com/nopnop2002/python-periphery-example/assets/6020549/c0ba3c08-8cd4-4488-ae6e-5d16fbf36b3d)
![luckfox-pico-2](https://github.com/nopnop2002/python-periphery-example/assets/6020549/536b585a-6695-4139-a97d-2c5aded58630)

- Milk-V Duo 64M board using CVITEK CV1800B chips.   
![Milk-V_Duo_64M](https://github.com/nopnop2002/python-periphery-example/assets/6020549/2e12bce9-e84e-4ad9-848a-9c64cc8eecf0)

- Milk-V Dio 256M board using Microsemi Corporation SG2002 chips.   
![Milk-V_Duo_256M](https://github.com/nopnop2002/python-periphery-example/assets/6020549/94e16c73-b2b5-4036-8965-d406aded7092)

I used it to check the operation of these Linux boards.

# Installation using pip

```Shell
sudo apt update
sudo apt install git python3-pip python3-setuptools
git clone https://github.com/vsergeev/python-periphery.git
cd python-periphery/
python3 -m pip install python-periphery
```

# Installing the buildroot environment   
Rebuild the kernel with python-periphery enabled.   
![python-periphery](https://github.com/nopnop2002/python-periphery-example/assets/6020549/7f26f096-6d5e-4618-a108-e5b174f9fc52)

