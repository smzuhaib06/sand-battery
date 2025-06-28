# control_logic.py
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

    gpio_pins = {
        "grid": 5,
        "sand": 6,
        "load": 13,
        "heater": 19,
        "mosfet1": 17,
        "mosfet2": 27,
        "mosfet3": 22
    }

    for pin in gpio_pins.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

except ImportError:
    print("GPIO not available. Running mock mode.")
    GPIO = None
    gpio_pins = {}

def control_gpio(name, state):
    if GPIO and name in gpio_pins:
        # Enforce: mosfet2 and mosfet3 cannot be ON at same time
        if name == "mosfet2" and state:
            GPIO.output(gpio_pins["mosfet3"], GPIO.LOW)
        if name == "mosfet3" and state:
            GPIO.output(gpio_pins["mosfet2"], GPIO.LOW)

        # Finally set requested pin
        GPIO.output(gpio_pins[name], GPIO.HIGH if state else GPIO.LOW)
    else:
        print(f"[Mock] Set {name} to {'ON' if state else 'OFF'}")
