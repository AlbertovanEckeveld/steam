import time
import machine
import neopixel
from machine import Pin, time_pulse_us

# Constants
SOUND_SPEED = 340  # in m/s
TRIG_PULSE_DURATION_US = 10  # microseconds
THRESHOLD_DISTANCE = 20  # in cm
HIGH_DISTANCE = 30  # in cm

# Pins
trig_pin = Pin(15, Pin.OUT)
echo_pin = Pin(14, Pin.IN)
np = neopixel.NeoPixel(machine.Pin(13), 8)

def measure_distance():
    """
    Meet de afstand met de ultrasone sensor en retourneert deze in cm.
    """
    trig_pin.value(0)

    trig_pin.value(1)
    time.sleep_us(TRIG_PULSE_DURATION_US)
    trig_pin.value(0)
    ultrason_duration = time_pulse_us(echo_pin, 1, 30000)
    if ultrason_duration < 0:
        return None  # Geen meetwaarde (timeout)
    
    # Berekening van afstand
    distance_cm = SOUND_SPEED * ultrason_duration / 20000
    return distance_cm


# Pulserende licht effecten
def light_pulse_effect_red(color, cycles=1):
    for _ in range(cycles):
        # Fade in
        for brightness in range(0, 256, 10):
            for i in range(8):
                np[i] = [brightness * color[0] // 255, 
                         brightness * color[1] // 255, 
                         brightness * color[2] // 255]
            np.write()
            time.sleep(0.025)
        # Fade out
        for brightness in range(255, -1, -10):
            for i in range(8):
                np[i] = [brightness * color[0] // 255, 
                         brightness * color[1] // 255, 
                         brightness * color[2] // 255]
            np.write()
            time.sleep(0.025)
            
def light_pulse_effect_green(color, cycles=1):
    """
    Laat een pulserend effect zien met de opgegeven kleur.
    """
    for _ in range(cycles):
        # Fade in
        for brightness in range(0, 256, 5):
            for i in range(8):
                np[i] = [brightness * color[0] // 255, 
                         brightness * color[1] // 255, 
                         brightness * color[2] // 255]
            np.write()
            time.sleep(0.05)
        # Fade out
        for brightness in range(255, -1, -5):
            for i in range(8):
                np[i] = [brightness * color[0] // 255, 
                         brightness * color[1] // 255, 
                         brightness * color[2] // 255]
            np.write()
            time.sleep(0.05)
            
            
def light_pulse_effect_blue(color, cycles=1):
    """
    Laat een pulserend effect zien met de opgegeven kleur.
    """
    for _ in range(cycles):
        # Fade in
        for brightness in range(0, 256, 10):
            for i in range(8):
                np[i] = [brightness * color[0] // 255, 
                         brightness * color[1] // 255, 
                         brightness * color[2] // 255]
            np.write()
            time.sleep(0.08)
        # Fade out
        for brightness in range(255, -1, -10):
            for i in range(8):
                np[i] = [brightness * color[0] // 255, 
                         brightness * color[1] // 255, 
                         brightness * color[2] // 255]
            np.write()
            time.sleep(0.08)


  
