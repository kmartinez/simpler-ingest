from peewee import *
from database import db
from forms import RoverDataForm
from datetime import datetime

class RoverData(Model):
    id = AutoField() # An Integer, auto increment primary key
    rover_id = IntegerField(unique=True, null=True)
    timestamp = DateTimeField(unique=True, null=True)
    longitude = DoubleField(null=True)
    latitude = DoubleField(null=True)
    altitude = DoubleField(null=True)
    quality = IntegerField()
    hdop = FloatField()
    sats = IntegerField(null=True)
    temperature = FloatField()

    def from_rover_form(rover_form: RoverDataForm):
        return RoverData(
            rover_id = rover_form.rover_id,
            timestamp = datetime.fromisoformat(rover_form.timestamp),
            longitude = float(rover_form.longitude),
            latitude = float(rover_form.latitude),
            altitude = rover_form.altitude,
            sats = rover_form.sats,
            temperature = rover_form.temp,
            hdop = 0.01, #Placeholder
            quality = 4 #Placeholder
            )

    class Meta:
        database = db
        table_name = "tracker_data"