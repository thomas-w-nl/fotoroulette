class PhotoData:
    def __init__(self):
        self.photo = []
        self.photo_angle = []
        self._sensor_data = []
        self._sensor_data_angle = []

    def get_sensor_data(self, graden: int) -> int:
        """
        Geeft de confidence score voor de sensor data bij een meegegeven aantal graden
        :param graden: het aantal graden
        :return confidence_score: de zekerheid of er iemand voor staat
        """
        pass
