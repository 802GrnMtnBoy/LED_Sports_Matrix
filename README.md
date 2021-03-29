# Disclaimer
I am in no way a professional at coding in Python (still learning) and am well aware that my code may not be considered "standard" or follows best practicies. But I do welcome anyone who would like to contribute to this project, make it better or more streamlined with more efficient code.

# LED Sports Matrix
A python project using a Raspberry Pi Zero with an Adafruit Hat to power a 32x64 LED Matrix with various sport data and weather information!

**I will be updating the ReadMe file as time allows**

This project was born from the efforts of the following separate projects.
  1.  [nhl-led-scoreboard](https://github.com/riffnshred/nhl-led-scoreboard)
  2.  [mlb-led-scoreboard](https://github.com/MLB-LED-Scoreboard/mlb-led-scoreboard)
  3.  [led-matrix-weatherstation](https://github.com/JosephSamela/led-matrix-weatherstation)

I am a fan of multiple sport teams and wanted to make a solution that would cycle through various sport teams instead of focus on one specific sport. Each sport screen shows basic information about active live games. This project makes various API calls and displays the response information to the LED matrix in addition to displaying weather and team logos. 


# Tools / Hardware
  1. Raspberry Pi - I used a [Raspberry Pi Zero WH](https://www.adafruit.com/product/3708) for this project
  2. [Adafruit RGB Martix Bonnet/Hat](https://www.adafruit.com/product/3211)
  3. [LED Matrix Module](https://www.amazon.com/gp/product/B07SDMWX9R/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1) (32x64 pixels)
  4. [5V 4A (4000mA) switching power supply](https://www.adafruit.com/product/1466)
  5. [GPIO Ribbon Cable 2x8 IDC Cable](https://www.adafruit.com/product/4170)

# Prerequisites
  1.  [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library (Allows code to access the LED Matrix)
  2.  weatherapi.com API key


# Example Outputs
![GitHub Logo](/images/PXL_20210329_114302690.jpg)

![GitHub Logo](/images/PXL_20210329_114318769.jpg)

![GitHub Logo](/images/PXL_20210329_114344873.jpg)
