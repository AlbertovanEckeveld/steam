import time
#import neopixel
from gpiozero import DigitalOutputDevice, DigitalInputDevice

# Constants
SOUND_SPEED = 343  # in m/s
TRIG_PULSE_DURATION_US = 10  # 10 microseconden
THRESHOLD_DISTANCE = 20  # in cm
HIGH_DISTANCE = 30  # in cm

# Pins
trig_pin = DigitalOutputDevice(15)  # GPIO 15 as output
echo_pin = DigitalInputDevice(14)   # GPIO 14 as input
#np = neopixel.NeoPixel(machine.Pin(13), 8)

def measure_distance():
    """
    Measures distance using the ultrasonic sensor and returns it in cm.
    """
    # Verzend trigger signaal
    trig_pin.off()
    time.sleep(0.000002)  # Wacht 2 microseconden
    trig_pin.on()
    time.sleep(0.00001) # Verzend 10 microseconden signaal
    trig_pin.off()

    # Wacht tot echo signaal wordt ontvangen
    while not echo_pin.value:
        pass  # Wacht op echo
    start_time = time.time()

    while echo_pin.value:
        pass  # Wacht tot echo signaal stopt
    end_time = time.time()

    # Bereken afstand in cm
    duration = end_time - start_time
    distance_cm = (SOUND_SPEED * duration * 100) / 2  # Deel door 2 omdat het geluid heen en terug gaat
    return distance_cm

"""
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
"""