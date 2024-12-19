import time
import neopixel
import RPi.GPIO as GPIO

# Constants
SOUND_SPEED = 340  # in m/s
TRIG_PULSE_DURATION_US = 10  # microseconds
THRESHOLD_DISTANCE = 20  # in cm
HIGH_DISTANCE = 30  # in cm

# Pins
trig_pin = Pin(15, Pin.OUT)
echo_pin = Pin(14, Pin.IN)
np = neopixel.NeoPixel(Pin(13), Pin.OUT)

#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(np, GPIO.OUT)


def measure_distance():
    """
    Measures distance using the ultrasonic sensor and returns it in cm.
    """ 
    # Send trigger pulse
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(0.000002)  # Wait 2 microseconds
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # Send 10 microsecond pulse
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Wait for echo start
    while GPIO.input(ECHO_PIN) == 0:
        pass
    start_time = time.time()

    # Wait for echo end
    while GPIO.input(ECHO_PIN) == 1:
        pass
    end_time = time.time()

    # Calculate distance
    duration = end_time - start_time
    distance_cm = (SOUND_SPEED * duration * 100) / 2  # Divide by 2 for round trip
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
  
