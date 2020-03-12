class RaspberryPIConnector:

    def setup_gpio(self, gpio: int, status: bool):
        #TODO call gpio handler REST
        print('setup', gpio, status)

    def set_gpio(self, gpio: int, status: bool):
        # TODO call gpio handler REST
        print('set', gpio, status)

    def cleanup_core(self):
        # TODO call gpio handler REST
        print('cleanup_core')