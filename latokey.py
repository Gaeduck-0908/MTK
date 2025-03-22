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

MIDI_KEY_MAP = {
    31: Key.shift, 32: 'a', 33: 's', 34: 'd',
    38: "j", 35: 'f', 36: 'g', 37: 'h',
}

def set_led(note, color):
    midi_out.send_message([144, note, color])

def clear_led(note):
    midi_out.send_message([144, note, 0])

def midi_callback(event, data=None):
    message, _ = event
    status, note, velocity = message
    
    if status == 144 and velocity > 0:  # Note On
        if note in MIDI_KEY_MAP:
            print(f"Pressed: {MIDI_KEY_MAP[note]}")
            keyboard.press(MIDI_KEY_MAP[note])
    elif status == 128 or (status == 144 and velocity == 0):  # Note Off
        if note in MIDI_KEY_MAP:
            print(f"Released: {MIDI_KEY_MAP[note]}")
            keyboard.release(MIDI_KEY_MAP[note])

midi_in.set_callback(midi_callback)

print("Listening for MIDI input... Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
    midi_in.close_port()
    midi_out.close_port()