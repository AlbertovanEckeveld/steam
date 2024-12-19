from app.connector.database import rf_authentication
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def tfa():
    """
        Two-factor authentication voor RFID-kaarten.

        Returns:
            bool: True als de authenticatie is geslaagd, anders False.
    """
    try:
        reader = SimpleMFRC522()

        if rf_authentication(reader.read()[0]) == True:
            return True
        
        return False

    finally:
        GPIO.cleanup()

