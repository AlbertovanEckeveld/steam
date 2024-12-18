import time
import machine
import neopixel
from machine import Pin, time_pulse_us

# Vaste waarden
GELUIDSSNELHEID = 340  # in m/s
TRIG_PULS_DUUR_US = 10  # microseconden
DREMPEL_AFSTAND = 40  # in cm
HOGE_AFSTAND = 60  # in cm

# Pins
trig_pin = Pin(15, Pin.OUT)
echo_pin = Pin(14, Pin.IN)
neopixel_strip = neopixel.NeoPixel(machine.Pin(13), 8)

def meet_afstand():
    """
    Meet de afstand met de ultrasone sensor en retourneert deze in cm.
    """
    trig_pin.value(0)
    time.sleep_us(5)

    trig_pin.value(1)
    time.sleep_us(TRIG_PULS_DUUR_US)
    trig_pin.value(0)
    ultrason_duur = time_pulse_us(echo_pin, 1, 30000)
    if ultrason_duur < 0:
        return None  # Geen meetwaarde (timeout)
    
    # Berekening van afstand
    afstand_cm = GELUIDSSNELHEID * ultrason_duur / 20000
    return afstand_cm

# Pulserende lichteffecten
def licht_pulserend_effect_rood(kleur, cycli=1):
    for _ in range(cycli):
        # Fade in
        for helderheid in range(0, 256, 10):
            for i in range(8):
                neopixel_strip[i] = [helderheid * kleur[0] // 255, 
                                     helderheid * kleur[1] // 255, 
                                     helderheid * kleur[2] // 255]
            neopixel_strip.write()
            time.sleep(0.025)
        # Fade out
        for helderheid in range(255, -1, -10):
            for i in range(8):
                neopixel_strip[i] = [helderheid * kleur[0] // 255, 
                                     helderheid * kleur[1] // 255, 
                                     helderheid * kleur[2] // 255]
            neopixel_strip.write()
            time.sleep(0.025)
            
def licht_pulserend_effect_groen(kleur, cycli=1):
    """
    Laat een pulserend effect zien met de opgegeven kleur.
    """
    for _ in range(cycli):
        # Fade in
        for helderheid in range(0, 256, 5):
            for i in range(8):
                neopixel_strip[i] = [helderheid * kleur[0] // 255, 
                                     helderheid * kleur[1] // 255, 
                                     helderheid * kleur[2] // 255]
            neopixel_strip.write()
            time.sleep(0.05)
        # Fade out
        for helderheid in range(255, -1, -5):
            for i in range(8):
                neopixel_strip[i] = [helderheid * kleur[0] // 255, 
                                     helderheid * kleur[1] // 255, 
                                     helderheid * kleur[2] // 255]
            neopixel_strip.write()
            time.sleep(0.05)
            
def licht_pulserend_effect_blauw(kleur, cycli=1):
    """
    Laat een pulserend effect zien met de opgegeven kleur.
    """
    for _ in range(cycli):
        # Fade in
        for helderheid in range(0, 256, 10):
            for i in range(8):
                neopixel_strip[i] = [helderheid * kleur[0] // 255, 
                                     helderheid * kleur[1] // 255, 
                                     helderheid * kleur[2] // 255]
            neopixel_strip.write()
            time.sleep(0.08)
        # Fade out
        for helderheid in range(255, -1, -10):
            for i in range(8):
                neopixel_strip[i] = [helderheid * kleur[0] // 255, 
                                     helderheid * kleur[1] // 255, 
                                     helderheid * kleur[2] // 255]
            neopixel_strip.write()
            time.sleep(0.08)

# Hoofdloop
while True:
    afstand_cm = meet_afstand()
    if afstand_cm is not None:
        print(f"Afstand: {afstand_cm:.2f} cm")

        if afstand_cm <= DREMPEL_AFSTAND:
            # Dichtbij: rood licht met pulserend effect
            licht_pulserend_effect_rood([128, 0, 0])
            
        elif DREMPEL_AFSTAND < afstand_cm <= HOGE_AFSTAND:
            # Tussenafstand: pulserend groen licht
            licht_pulserend_effect_groen([0, 128, 0])
            
        else:
            # Ver weg: blauw licht met pulserend effect
            licht_pulserend_effect_blauw([0, 0, 128])
    else:
        print("Geen afstand gemeten (timeout)")

    time.sleep(0.25)
