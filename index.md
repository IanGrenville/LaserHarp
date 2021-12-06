# Laser Harp Final Project

This is my write-up of the final project I completed for MUMT306 at McGill University in Fall 2021. 

![Picture](PXL_20211130_035925657_exported_2073.jpg)

## Demo

## Overview

For my final project I designed a Laser Harp. A Laser Harp is a type of digital music interface that uses the placement and positioning of a performers hands relative to a series of laser beams to activate notes and adjust musical control parameters. In my specific implemtation, the harp uses an array of phototransistors to detect the breaking of a laser beam, and a parallel array of ultrasonic distance sensors to detect the precise location of the performers hand relative to the height of the beam. My harp then uses this information to send MIDI signals over a USB connection, which can then be attached to any digital MIDI synthesizer or DAW. 

### Physical Structure

The harp is approximately two metres wide by half a metre tall, constructed out of wood. On the top of the frame is an array of laser diodes hooked up to a seperate 5V source from the rest of the harp(to prevent the lasers inducing noise for the other sensors). For most of the testing a nine volt battery and converter circuit was used as this secondary power source. The rest of the system was powered through the USB connection to my computer. 

On the lower part of the frame, in parallel with the laser array is an array of phototransistors inserted into pre-drilled holes in the wooden frame. These light sensors are then routed through a multiplexer into the main microcontroller. On the top of the lower bar of the frame is also a distance sensor correspond to eight of the ten laser beams(those which play musical notes), as well as an array of breadboards. The breadboards handle connecting the wiring for both the main microcontroller as well as all of the distance sensors. 

![Physical structure](labelled_hardware.PNG)


|Colour | Component|
|-------|----------|
|Red | Laser Array|
|Green | Sonar Sensor|
|Blue | Pi Pico/Mux |
|Purple | Phototransistor|

### Musical Interface

Before a performance can begin, the light sensors must be manually tuned corresponding to the ambient light conditions in the space, as well as to adjust for overall variances and unreliabilities with the electronic components. After setup is complete, the performer engages with the instrument through physical gesture and positioning of their hands relative to the beam array. In a continous cycle, the performer recieves musical feedback from the sounds induced by their actions. From this, they can then move their hands horizontally and vertically to play new notes or to control the parameters of existing ones. Once they have done so, the instrument will measure this new set of data points and convert it into MIDI notes, which are sent to the computer which then produces further musical feedback, continuing the loop of the performance. 

![Musical Interface Diagram](performance_diagram.PNG)

## Implementation

![Implementation Diagram](operation_diagram.PNG)

### Hardware

- [HRCS04 Distance Sensors](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
- [650nm 5mw Laser Diodes](https://www.adafruit.com/product/1054#technical-details)
- [HW5P-1 Phototransistors](https://cdn-shop.adafruit.com/product-files/2831/HW5P-1_2015__1_.pdf)
- [4051 Analog Multiplixer](https://www.ti.com/lit/ds/symlink/cd4051b.pdf?ts=1638812768510&ref_url=https%253A%252F%252Fwww.ti.com%252Fproduct%252FCD4051B)
- [Raspberry Pi Pico](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)

### Software

- [Circuitpython](https://circuitpython.org/)
- [adafruit_hcsr04](https://circuitpython.readthedocs.io/projects/hcsr04/en/0.4.4/)
- [digitalIO](https://circuitpython.readthedocs.io/en/latest/shared-bindings/digitalio/index.html)/[analogIO](https://circuitpython.readthedocs.io/en/latest/shared-bindings/analogio/index.html)
- [uLab](https://circuitpython.readthedocs.io/en/latest/shared-bindings/ulab/)
- [adafruit_midi](https://circuitpython.readthedocs.io/projects/midi/en/latest/api.html)
- [usb_midi](https://circuitpython.readthedocs.io/en/latest/shared-bindings/usb_midi/index.html)

## Issues and Solutions

### Complexity

### Filtering

![Sensor Data Example](sensor_comp.PNG)
### Latency

## Conclusions 

