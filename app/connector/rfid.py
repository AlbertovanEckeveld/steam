from app.connector.database import execute_query
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()


def rfid_authentication(userRFID):
    isAuthenticated = False


    rfidQuery = execute_query(f"SELECT COUNT(*) FROM authentication WHERE rfid = '{userRFID}'")


    print("Resultaat query =", rfidQuery)


    if rfidQuery[0][0] == 1:
        print("Je RFID komt voor in het systeem.")
        isAuthenticated = True
    else:
        print("Helaas, je RFID komt niet voor in het systeem")

    return isAuthenticated



try:
    print("Houd je RFID-kaart voor de lezer")


    id, text = reader.read()
    print(f"Gelezen RFID: {id}")


    if rfid_authentication(id) == True:
        print("Toegang verleend!")
    else:
        print("Toegang geweigerd!")

finally:
    GPIO.cleanup()

