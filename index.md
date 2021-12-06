# Laser Harp Final Project

This is my write-up of the final project I completed for MUMT306 at McGill University in Fall 2021. 

## Overview

For my final project I designed a Laser Harp. A Laser Harp is a type of digital music interface that uses the placement and positioning of a performers hands relative to a series of laser beams to activate notes and adjust musical control parameters. In my specific implemtation, the harp uses an array of phototransistors to detect the breaking of a laser beam, and a parallel array of ultrasonic distance sensors to detect the precise location of the performers hand relative to the height of the beam. My harp then uses this information to send MIDI signals over a USB connection, which can then be attached to any digital MIDI synthesizer or DAW. 

### Physical Structure

The harp is approximately two metres wide by half a metre tall, constructed out of wood. On the top of the frame is an array of laser diodes hooked up to a seperate 5V source from the rest of the harp(to prevent the lasers inducing noise for the other sensors). For most of the testing a nine volt battery and converter circuit was used as this secondary power source. The rest of the system was powered through the USB connection to my computer. 

On the lower part of the frame, in parallel with the laser array is an array of phototransistors inserted into pre-drilled holes in the wooden frame. These light sensors are then routed through a multiplexer into the main microcontroller. On the top of the lower bar of the frame is also a distance sensor correspond to eight of the ten laser beams(those which play musical notes), as well as an array of breadboards. The breadboards handle connecting the wiring for both the main microcontroller as well as all of the distance sensors. 

### Musical Interface

The performer engages with the instrument through physical gesture and positioning of their hands relative to the beam array. In a continous cycle, the performer recieves musical feedback from the sounds induced by their actions. From this, they can then move their hands horizontally and vertically to play new notes or to control the parameters of existing ones. Once they have done so, the instrument will measure this new set of data points and convert it into MIDI notes, which are sent to the computer which then produces further musical feedback, continuing the loop of the performance. 

## Implementation

### Hardware

### Software

## Issues and Solutions

### Complexity

### Filtering

### Latency

## Conclusions 

