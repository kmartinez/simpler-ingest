#These define what the data from the base and rovers that comes in should look like
class BaseDataForm:
    id: int
    temp: float
    timestamp: str
    batv: float

    def from_json(json):
        instance = BaseDataForm()
        try:
            instance.id = int(json["id"])
            instance.temp = float(json["temp"])
            instance.timestamp = str(json["timestamp"])
            instance.batv = float(json["batv"])
        except (KeyError, ValueError):
            raise ValueError("JSON is invalid")
        
        return instance

class RoverDataForm:
    rover_id: int
    sats: int
    temp: float
    altitude: float
    timestamp: str
    batv: float
    latitude: str
    longitude: str

    def from_json(json):
        instance = RoverDataForm()
        try:
            instance.rover_id = int(json["rover_id"])
            instance.sats = int(json["sats"])
            instance.temp = float(json["temp"])
            instance.altitude = float(json["altitude"])
            instance.timestamp = str(json["timestamp"])
            instance.batv = float(json["batv"])
            instance.latitude = str(json["latitude"])
            instance.longitude = str(json["longitude"])
        except (KeyError, ValueError):
            raise ValueError("JSON is invalid")
        
        return instance