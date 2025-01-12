try:
    from app.connector.database import rf_authentication
    from mfrc522 import SimpleMFRC522
    import RPi.GPIO as GPIO
    
    
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

except ImportError: # Als RPi.GPIO niet is geïnstalleerd, of niet draait op een Raspberry Pi
    def tfa(): return False
