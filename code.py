#####################################################
#Laser Harp Control Software by Ian Grenville
#Created as part of a project for MUMT 306, Fall 2021
#Written in circuitpython for the Raspberry Pi Pico
#####################################################

#IO Libraries
import analogio
import digitalio
import board
import usb_midi
import adafruit_midi
import adafruit_hcsr04
#Processing Libraries
from ulab import numpy as np
import time


from adafruit_midi.note_on import NoteOn as note_on
from adafruit_midi.note_off import NoteOff as note_off
from adafruit_midi.control_change import ControlChange as control_change
from adafruit_midi.polyphonic_key_pressure import PolyphonicKeyPressure as polyphonic_key_pressure


#Pin mapping for access to the multiplexer and directly connected light sensors
mux_select_pins = [digitalio.DigitalInOut(board.GP22), digitalio.DigitalInOut(board.GP21), digitalio.DigitalInOut(board.GP20)]

for pin in mux_select_pins:
    pin.switch_to_output()

mux_in_pin = analogio.AnalogIn(board.A0)
left_select_light = analogio.AnalogIn(board.A1)
right_select_light = analogio.AnalogIn(board.A2)


#Pin mapping and constants for the distance sensors
trigger_pins = [board.GP7,board.GP9,board.GP10,board.GP1,board.GP17,board.GP19,board.GP12,board.GP15]
echo_pins = [board.GP6,board.GP8,board.GP11,board.GP0,board.GP16,board.GP18,board.GP13,board.GP14]

sonar = [None] * 8

sonar_data = np.zeros((10, 10), dtype=np.uint8)

for i in range(0, 8):
   sonar[i] = adafruit_hcsr04.HCSR04(trigger_pin=trigger_pins[i], echo_pin=echo_pins[i])
max_distance = 60 # The frame of the harp is about 58cm tall. This makes sure that we don't ever accidentally take readings from outside the harp frame.

#Data structures and pre-supplied thresholds/biases for handling light sensor data
light_thresholds = [250,100,150,100,100,100,120,200,400,300]

light_bias = [400,600,500,600,500,500,500,600,600,500]
light_trust = [(1,-10),(2,-30),(1,-10),(10,-100),(1,-10),(1,-10),(1,-10),(1,-10),(10,-10),(1,-10)]

light_data = np.ones((10,90), dtype=np.uint16)

flagged_sensors = [False]*10 #Indicates whether the data from a light sensor is too unreliable to be used. Uses distance sensors as a backup instead.



#Creates a very simply filter that gives a high weight to the 10 most recent samples and a low weight to the other 40 most recent
finite_impulse_filter = np.concatenate((np.ndarray([1/50]*10),np.ndarray([1/100] * 80)))

#Musical data structures and constants
major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
minor_scale = [0, 2, 3, 5, 7, 8, 10, 12]
scale = major_scale
root_note = 60 #Default note is middle c
note_state = [0] * 8
playing = [False] * 8

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

def read_light_sensors():   # Returns a 10 long list of sensor intensity
    global light_data
    light_data = np.roll(light_data, 1, axis=1) #Effectively turns our numpy array into a circular buffer
    for i in range(0,8):   # Read the mux light sensors
        #Set the selector pins using binary arithmetic
        mux_select_pins[0].value = i & 1
        mux_select_pins[1].value = i & 2
        mux_select_pins[2].value = i & 4
        #Read data
        value = mux_in_pin.value
        light_data[i,0] = value
    #The endmost light sensors are attached directly to the board
    light_data[8,0] = left_select_light.value
    light_data[9,0] = right_select_light.value
    values = [0]*10
    for i in range(0, 10):
        values[i] = np.dot((light_data[i]),finite_impulse_filter) #Apply the filter to the most recent vector of samples
    return values

#Check if the our light sensor detects the beam being blocked
def check_blocking():
    values = read_light_sensors()
    results = [False] * 10
    for i in range(0,10):
        #Compares each measurement to its threshold, adjusted by the bias
        power = abs(values[i]-light_bias[i])
        results[i] = (power > light_thresholds[i])
    return results

#Activate, read and store the data from all of our light sensors
def read_sonar():
    global sonar_data
    sonar_data = np.roll(sonar_data, 1, axis=1) #Effectivly turns our numpy array into a circular buffer
    for i in range(0,8):
        try:
            distance = sonar[i].distance
            if(distance < max_distance and distance > 0):
                sonar_data[i,0] = distance
        except Exception as error:
            print("Error reading sensor "+str(i))
            print(error)

#Returns the running average of the given sensor over the last 10 distance samples
def get_distance(sonar_index):
    return np.mean(sonar_data[sonar_index])

#Adjust our confidence that the note should be being played depending on whether the light sensors report it as blocked
def state_transition(state,blocking,trust):
    if(state>= 0 and blocking):
        return min(state+trust[0],100) #Maximum confidence of 100 to prevent notes lasting too long
    else:
        return max(state+trust[1],0)

def handle_setup():
    print("major or minor?")
    response = input()
    if(response == "major"):
        scale = major_scale
    elif(response == "minor"):
        scale = minor_scale
    print("What root note?(as a midi number)")
    if(int(response) > 0 and int(response) < 128):
        root_note = int(response)

    for i in range(0,100): #Just let the sensors run for a while to fill up the buffers properly
        read_light_sensors()
        read_sonar()
        time.sleep(0.01)

    for j in range(0,10): #Calibrating light sensors
        response = "more"
        while(not response=="done"):
            print("Calibrating sensor: " + str(j))
            max_sample = 0
            for k in range(0,150): #Read a set of 150 (post-filtering) sensor values to get an idea of its current ranges and response characteristics
                sample = abs(read_light_sensors()[j]-light_bias[j])
                max_sample = max(sample,max_sample)
                print((0,sample,light_thresholds[j])) #Print the data to the serial plotter for inspecting ranges
                time.sleep(0.02) #Sleep a bit so we don't data flood the computer
            print("Max sample:" + str(max_sample) + " Current Bias: " + str(light_bias[j]))
            response = input()
            if(response == "bias+"):
                light_bias[j]+=100
            elif(response == "bias-"):
                light_bias[j]-=100
            elif(response == "skip"):
                return
            elif(response == "flag"):
                flagged_sensors[j] = True
                response = "done"
            elif(not response == "done" and int(response) > 0 and int(response) < 1000):
                light_thresholds[j] = int(response)

#Backup tracking for if the light sensors for a given note are too unreliable.
#Attempts to detect hand presence from sonar information alone.
def hand_locate():
    hand = [0]*8
    for i in range(0,8):
        x = get_distance(i)
        y = max_distance
        z = max_distance
        if(i>0):
            y = get_distance(i-1)
        if(i<7):
            z = get_distance(i+1)
        #Specficially, since the sensors detect a cone larger than the beam, we check if there is a hand sufficiently closer to the sensor than to its neighbours.
        hand[i] = x if (y-x > 5 and z-x > 5) else 0
    return hand

handle_setup()
while True:
    blocking = check_blocking()
    for i in range(0,8):
        note_state[i] = state_transition(note_state[i],blocking[i],light_trust[i]) #Adjust our confidence that the note is being played by whether its being blocked
        if(flagged_sensors[i]): #If we've flagged the light sensor as unreliable, we just go off whether there is a hand above the sensor
            note_state[i] += light_trust[i][0] if (hand_locate()[7-i] > 0) else light_trust[i][1]

    read_sonar()
    distances = [max_distance]*8

    for j in range(0,8):
        note = root_note + scale[j]
        if(blocking[8]): #If the right beam is broken shift up a semitone
            note += 1
        elif(blocking[9]): #If the left beam is broken, shift down a semitone
            note -= 1
        if(note_state[j] > 3): #If we're pretty sure a note is being played,
            distances[j] = get_distance(7-j)
            if(not playing[j] and distances[j] <= 50): #We make sure there's a hand relatively nearby before triggering a note
                playing[j] = True
                midi.send(note_on(note, int(127*(distances[j])/max_distance))) #We send the note signal with the hand distance as a velocity param
            elif(playing[j] and distances[j] <= 55):
                midi.send(polyphonic_key_pressure(note,int(127*(distances[j])/max_distance))) #After playing we continue to send hand distance as aftertouch
                midi.send(control_change(20,int(min(distances)))) #We also send the lowest of all the the distance measurements as an overall control param
        else:
            if(playing[j]):
                playing[j] = False
                midi.send(note_off(note))

