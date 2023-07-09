from peewee import *
from database import db
from forms import RoverDataForm, BaseDataForm
from datetime import datetime

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