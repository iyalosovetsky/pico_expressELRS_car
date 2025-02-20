# ELRS car platform



 This project has code to control the car platform by express ELRS receiver like betafpv nano receiver and TX12 RC . 
 The car is a four wheel drive platform powered by 4 PWM controlled motors. The code implements CRSF protocol on Raspberry Pico W to send command and retrieve telemetry data (battery state). 


| Platform                            | Start here                                                        | Further info              | 
|-------------------------------------|-------------------------------------------------------------------|---------------------------|
|Receiver BETAFPV NANO 2400                       | [![Receiver BETAFPV NANO 2400](https://www.expresslrs.org/assets/images/betaFPVrx2400.png)](https://prom.ua/ua/p2130654195-priemnik-elrs-24ghz.html) | [Doc][plat_arduino]       |
| Arduino using ESP-IDF toolchain     | [Template project][esp-idf-bluepad32-arduino]                     | [Doc][plat_arduino]       |
| Arduino + NINA coprocessor          | [Arduino Library][bp32-arduino]                                   | [Doc][plat_nina]          |
| CircuitPython + AirLift coprocessor | [CircuitPython Library][bp32-circuitpython]                       | [Doc][plat_airlift]       |
| Pico W                              | [Pico W example][pico-w-example]                                  | [Doc][plat_picow_picosdk] |
| ESP-IDF                             | [ESP32 example][esp32-example]                                    | [Doc][plat_esp32_espidf]  |
| Posix (Linux, macOS)                | [Posix example][posix-example]                                    | [Doc][plat_custom]        |                                                                                                           |
| Unijoysticle                        | [Unijoysticle2][unijoysticle2]                                    | [Doc][plat_unijoysticle]  |                                                                                                           |
| MightyMiggy                         | [Unijoysticle for Amiga][unijoysticle_sukko]                      | [Doc][plat_mightymiggy]   |                                                                                                           |



[![Watch the video](https://img.youtube.com/vi/cAvKrcaPvDQ/default.jpg)](https://youtu.be/cAvKrcaPvDQ)

parts 

[![Receiver BETAFPV NANO 2400](https://www.expresslrs.org/assets/images/betaFPVrx2400.png)](https://prom.ua/ua/p2130654195-priemnik-elrs-24ghz.html)

[![car platform](https://arduino.ua/products_pictures/large_ARC148.jpg)](https://arduino.ua/prod1908-robo-platforma-4-h-kolesnaya-dvyhpalybnaya-polnoprivodnaya)

[![Raspberry Pico W](https://www.raspberrypi.com/documentation/microcontrollers/images/pico-2-r4-pinout.svg)](
https://evo.net.ua/ru/mikrokontroller-raspberry-pi-pico-w/?srsltid=AfmBOopUA4QeR49kMoKL6BeQcgUpomg1QyBUS0xVd83PSJlIUxghn0VV)

[![optical sensor](https://arduino.ua/products_pictures/large_ADC233-1.jpg)](https://arduino.ua/prod2290-opticheskii-datchik-prepyatstviya-kompaktnii)



[![2S charger and bms ip2326](https://arduino.ua/products_pictures/large_aoc862_1.jpg)](https://arduino.ua/prod5916-modyl-bms-li-ion-2s-ip2326)

[![2x 18650 3000mAh](https://arduino.ua/products_pictures/large_tmp268_1.jpg)](https://arduino.ua/prod6971-akymylyator-lg-hg2-18650-3000mach-bez-zahisty-z-rozbirannya-bez-vivodiv)


[![PWM driver drv8833](https://arduino.ua/products_pictures/large_arc209_1.jpg)](https://arduino.ua/prod3697-draiver-dvigatelei-dvyhkanalnii-drv8833)

https://arduino.ua/prod6108-peremikach-kryglii-kcd1-201-2p-on-off-2-h-kontaktnii-6a-220v-bilii




see my project to control by bluetouth joystick  https://github.com/iyalosovetsky/robocar 
