try:
    import Jetson.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    gpio_pins = {
        "grid": 7,
        "sand": 11,
        "load": 13,
        "heater": 15
    }
    for pin in gpio_pins.values():
        GPIO.setup(pin, GPIO.OUT)
except ImportError:
    print("GPIO not available on this system. Using mock.")
    GPIO = None
    gpio_pins = {}

def control_gpio(name, state):
    if GPIO and name in gpio_pins:
        GPIO.output(gpio_pins[name], GPIO.HIGH if state else GPIO.LOW)
    else:
        print(f"Simulated: Setting {name} to {'HIGH' if state else 'LOW'}")