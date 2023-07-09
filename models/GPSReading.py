from peewee import *
from database import db
from forms import RoverDataForm
from datetime import datetime

class GPSReading(Model):
    id = AutoField() # An Integer, auto increment primary key
    rover_id = IntegerField()
    timestamp = DateTimeField()
    longitude = DoubleField()
    latitude = DoubleField()
    altitude = DoubleField()
    quality = IntegerField(null = True)
    hdop = FloatField(null = True)
    sats = IntegerField()
    temperature = FloatField(null = True)

    def from_rover_form(rover_form: RoverDataForm):
        return GPSReading(
            rover_id = rover_form.rover_id,
            timestamp = datetime.fromisoformat(rover_form.timestamp),
            longitude = float(rover_form.longitude),
            latitude = float(rover_form.latitude),
            altitude = rover_form.altitude,
            sats = rover_form.sats,
            temperature = rover_form.temp
            )

    class Meta:
        database = db
        table_name = "tracker_data"