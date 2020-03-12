from unittest.mock import Mock

_mock_map = {}


def setup(gpio, status):
    _mock_map[gpio] = status


def output(gpio, status):
    if gpio in _mock_map:
        _mock_map[gpio] = status


def read(gpio):
    print("read gpio {}".format(gpio))
    return _mock_map.get(gpio, 1)


def setmode(mode):
    print("set mode {}".format(mode))


def cleanup():
    print("cleanup")
    _mock_map = {}


def setwarnings(boolean):
    print("setwarning {}".format(boolean))


BCM = "bcm"
HIGH = "high"
LOW = "low"
OUT = "out"
