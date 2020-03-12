from gpiohandler import MOCK_FRUIT as fruit
from model import Sensor


def get_air_sensor_data(sensor: Sensor) -> tuple:
    return fruit.read_retry(fruit.DHT11, sensor.sensor_gpio)
