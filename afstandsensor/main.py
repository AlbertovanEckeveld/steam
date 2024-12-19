import time
import neopixel
import rpi.gpio as GPIO
import board

# Constants
TRIG_PIN = 15  # GPIO 15
ECHO_PIN = 14  # GPIO 14
SOUND_SPEED = 343  # m/s
TRIG_PULSE_DURATION_US = 10  # microseconds
THRESHOLD_DISTANCE = 20  # in cm
HIGH_DISTANCE = 30  # in cm

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
NEOPIXEL_PIN = board.D18

# NeoPixel setup
NUM_PIXELS = 8
ORDER = neopixel.GRB
np = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=0.5, auto_write=False, pixel_order=ORDER)

def measure_distance():
    """
    Meet de afstand met de ultrasone sensor en retourneert deze in cm.
    """
    TRIG_PIN.value(0)
    time.sleep_us(5)

    TRIG_PIN.value(1)
    time.sleep_us(TRIG_PULSE_DURATION_US)
    TRIG_PIN.value(0)
    ultrason_duration = time_pulse_us(ECHO_PIN, 1, 30000)
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

# Main loop
while True:
    distance_cm = measure_distance()
    if distance_cm is not None:
        print(f"Distance: {distance_cm:.2f} cm")

        if distance_cm <= THRESHOLD_DISTANCE:
            # Dichtbij: rood licht met lopend effect
            light_pulse_effect_red([128, 0, 0])
            
        elif THRESHOLD_DISTANCE < distance_cm <= HIGH_DISTANCE:
            # Tussenafstand: pulserend groen licht
            light_pulse_effect_green([0, 128, 0])
            
        else:
            # Ver weg: blauw licht met lopend effect
            light_pulse_effect_blue([0, 0, 128])
    else:
        print("No distance measured (timeout)")

    time.sleep(0.25)
  
