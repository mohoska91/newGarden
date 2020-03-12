from model import Sensor


class RawSensing:
    _MAP = {
        "Stemma": lambda sensor: 3,
        "DHT11": lambda sensor: 2
    }

    @classmethod
    def sense(cls, sensor: Sensor):
        return cls._MAP[sensor.name](sensor)
