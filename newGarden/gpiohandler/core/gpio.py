try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    from gpiohandler import MOCK_GPIO as GPIO


GPIO_KEY = "gpio"
STATUS_KEY = "status"

SWITCH_MAP = {
    False: GPIO.HIGH,
    True: GPIO.LOW
}

_GPIO_RANGE = range(1, 27)


def init_core():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


def is_valid_gpio(gpio: int) -> bool:
    return gpio in _GPIO_RANGE


def setup_gpio(gpio: int, status: bool):
    GPIO.setup(gpio, GPIO.OUT, initial=SWITCH_MAP[status])


def set_gpio(gpio: int, status: bool):
    GPIO.output(gpio, SWITCH_MAP[status])


def get_gpio_status(gpio: int) -> bool:
    return SWITCH_MAP[GPIO.read(gpio)]


def cleanup_core():
    GPIO.cleanup()
