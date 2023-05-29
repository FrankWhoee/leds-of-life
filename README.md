# leds-of-life
Script to run Game of Life on an led matrix as a decoration perpetually

## Demo
![](https://github.com/FrankWhoee/leds-of-life/blob/master/demo.gif?raw=true)

## Installation
1. `git clone https://github.com/hzeller/rpi-rgb-led-matrix.git`
2. `cd rpi-rg-led-matrix/bindings/python/`
3. `sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y`
4. `make build-python PYTHON=$(command -v python3)`
5. `sudo make install-python PYTHON=$(command -v python3)`
6. `cd ../../..`
7. `git clone git@github.com:FrankWhoee/leds-of-life.git`
8. `cd leds-of-life`
9. `sudo python3 main.py`
