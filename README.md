# ELRS car platform



 This project has code to control the car platform by express ELRS receiver like betafpv nano receiver and TX12 RC . 
 The car is a four wheel drive platform powered by 4 PWM controlled motors. The code implements CRSF protocol on Raspberry Pico W to send command and retrieve telemetry data (battery state). 


The parts 

| Part name                            | Start here                                                        | Further info              | 
|-------------------------------------|-------------------------------------------------------------------|---------------------------|
|Raspberry Pico W                     | [![Raspberry Pico W](https://www.raspberrypi.com/documentation/microcontrollers/images/pico-2-r4-pinout.svg)](https://evo.net.ua/ru/mikrokontroller-raspberry-pi-pico-w/?srsltid=AfmBOopUA4QeR49kMoKL6BeQcgUpomg1QyBUS0xVd83PSJlIUxghn0VV) | [Link](https://evo.net.ua/ru/mikrokontroller-raspberry-pi-pico-w/?srsltid=AfmBOopUA4QeR49kMoKL6BeQcgUpomg1QyBUS0xVd83PSJlIUxghn0VV) |
|Receiver BETAFPV NANO 2400           | [![Receiver BETAFPV NANO 2400](https://www.expresslrs.org/assets/images/betaFPVrx2400.png)](https://prom.ua/ua/p2130654195-priemnik-elrs-24ghz.html) | [Link](https://prom.ua/ua/p2130654195-priemnik-elrs-24ghz.html)       |
|car platform                         | [![car platform](https://arduino.ua/products_pictures/large_ARC148.jpg)](https://arduino.ua/prod1908-robo-platforma-4-h-kolesnaya-dvyhpalybnaya-polnoprivodnaya) | [Link]([https://prom.ua/ua/p2130654195-priemnik-elrs-24ghz.html](https://arduino.ua/prod1908-robo-platforma-4-h-kolesnaya-dvyhpalybnaya-polnoprivodnaya)       |
(https://evo.net.ua/ru/mikrokontroller-raspberry-pi-pico-w/?srsltid=AfmBOopUA4QeR49kMoKL6BeQcgUpomg1QyBUS0xVd83PSJlIUxghn0VV)       |
|optical sensor                       | [![optical sensor](https://arduino.ua/products_pictures/large_ADC233-1.jpg)](https://arduino.ua/prod2290-opticheskii-datchik-prepyatstviya-kompaktnii) | [Link]([https://prom.ua/ua/p2130654195-priemnik-elrs-24ghz.html](https://arduino.ua/prod2290-opticheskii-datchik-prepyatstviya-kompaktnii)       |
|2S charger and bms ip2326           | [![2S charger and bms ip2326](https://arduino.ua/products_pictures/large_aoc862_1.jpg)](https://arduino.ua/prod5916-modyl-bms-li-ion-2s-ip2326) | [Link](https://arduino.ua/prod5916-modyl-bms-li-ion-2s-ip2326)       |
|2x 18650 3000mAh           | [![2x 18650 3000mAh](https://arduino.ua/products_pictures/large_tmp268_1.jpg)](https://arduino.ua/prod6971-akymylyator-lg-hg2-18650-3000mach-bez-zahisty-z-rozbirannya-bez-vivodiv) | [Link](https://prom.ua/ua/p2130654195-priemnik-elrs-24ghz.html](https://arduino.ua/prod6971-akymylyator-lg-hg2-18650-3000mach-bez-zahisty-z-rozbirannya-bez-vivodiv)       |
|PWM driver drv8833           | [![PWM driver drv8833](https://arduino.ua/products_pictures/large_arc209_1.jpg)](https://arduino.ua/prod3697-draiver-dvigatelei-dvyhkanalnii-drv8833) | [Link](https://arduino.ua/prod3697-draiver-dvigatelei-dvyhkanalnii-drv8833)        |







see my project to control by bluetouth joystick  https://github.com/iyalosovetsky/robocar 
