import RPi.GPIO as GPIO
import time

# Constants
TRIG_PIN = 15  # GPIO 15
ECHO_PIN = 14  # GPIO 14
SOUND_SPEED = 343  # m/s

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

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

try:
    while True:
        distance = measure_distance()
        print(f"Distance: {distance:.2f} cm")
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped.")
finally:
    GPIO.cleanup()
