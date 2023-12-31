from peewee import *
from database import db
from forms import RoverDataForm,BaseDataForm
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
    #NOTE: temperature is obsoleted by TemperatureReading but is left filled in
    #for backward compatibility purposes (with glactracker plotter)
    #i would very much advise the field be removed when someone can be bothered
    #to update the plotter

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
        constraints = [SQL('UNIQUE (rover_id, timestamp)')]

class VoltageReading(Model):
    id = AutoField() # An Integer, auto increment primary key
    rover_id = IntegerField()
    timestamp = DateTimeField()
    value = FloatField()

    def from_rover_form(rover_form: RoverDataForm):
        return VoltageReading(
            rover_id = rover_form.rover_id,
            timestamp = datetime.fromisoformat(rover_form.timestamp),
            value = rover_form.batv
            )

    def from_base_form(base_form: BaseDataForm):
        return VoltageReading(
            rover_id = base_form.id,
            timestamp = datetime.fromisoformat(base_form.timestamp),
            value = base_form.batv
        )

    class Meta:
        database = db
        table_name = "voltage_readings_2023"
        constraints = [SQL('UNIQUE (rover_id, timestamp)')]

class TemperatureReading(Model):
    id = AutoField() # An Integer, auto increment primary key
    rover_id = IntegerField()
    timestamp = DateTimeField()
    value = FloatField()

    def from_rover_form(rover_form: RoverDataForm):
        return TemperatureReading(
            rover_id = rover_form.rover_id,
            timestamp = datetime.fromisoformat(rover_form.timestamp),
            value = rover_form.temp
            )

    def from_base_form(base_form: BaseDataForm):
        return TemperatureReading(
            rover_id = base_form.id,
            timestamp = datetime.fromisoformat(base_form.timestamp),
            value = base_form.temp
        )

    class Meta:
        database = db
        table_name = "temperature_readings_2023"
        constraints = [SQL('UNIQUE (rover_id, timestamp)')]