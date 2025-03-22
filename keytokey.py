import rtmidi
from pynput.keyboard import Controller, Key
import time

keyboard = Controller()

midi_in = rtmidi.MidiIn()
midi_out = rtmidi.MidiOut()
available_ports = midi_in.get_ports()
available_out_ports = midi_out.get_ports()

if available_ports:
    midi_in.open_port(0)
    print(f"Connected to: {available_ports[0]}")
else:
    print("No MIDI input ports available.")
    exit()

if available_out_ports:
    midi_out.open_port(0)
    print(f"Connected to output: {available_out_ports[0]}")
else:
    print("No MIDI output ports available.")
    exit()

MIDI_TO_KEY = {
    50: 'a',  
    52: 's',  
    53: 'd', 
    67: 'f',  
    69: 'g', 
    71: 'h',  
    48: Key.shift_l,  
    72: 'j', 
}

def midi_callback(event, data=None):
    message, _ = event
    status, note, velocity = message
    
    if status == 144 and velocity > 0:  # Note On
        if note in MIDI_TO_KEY:
            key = MIDI_TO_KEY[note]
            print(f"Pressed: {key}")
            keyboard.press(key)
    elif status == 128 or (status == 144 and velocity == 0):  # Note Off
        if note in MIDI_TO_KEY:
            key = MIDI_TO_KEY[note]
            print(f"Released: {key}")
            keyboard.release(key)

midi_in.set_callback(midi_callback)

print("Listening for MIDI input... Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
    midi_in.close_port()
    midi_out.close_port()
