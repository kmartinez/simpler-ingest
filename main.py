from flask import Flask, request, abort
from forms import *
from models import *
from peewee import IntegrityError
import csv
import time

app = Flask(__name__)

db.create_tables([GPSReading, VoltageReading, TemperatureReading])


@app.route("/<id>", methods=["GET"])
def retrieve(id):
    id = int(id)

    # joins the tables based on rover_id and timestamp combined
    items = (TemperatureReading.select(
        TemperatureReading.rover_id.alias("rover_id"),
        TemperatureReading.timestamp.alias("timestamp"),
        GPSReading.latitude.alias("lat"),
        GPSReading.longitude.alias("long"),
        GPSReading.altitude.alias("alt"),
        VoltageReading.value.alias("voltage"),
        TemperatureReading.value.alias("temperature")
    ).join(
        VoltageReading,
        on=(TemperatureReading.rover_id == VoltageReading.rover_id and TemperatureReading.timestamp == VoltageReading.timestamp)
    ).join(
        GPSReading,
        JOIN.LEFT_OUTER,
        on=(TemperatureReading.rover_id == GPSReading.rover_id and TemperatureReading.timestamp == GPSReading.timestamp)
    ).where(TemperatureReading.rover_id == id)
    .order_by(TemperatureReading.timestamp))

    dicts = []
    for item in items.objects():
        # spent multiple real time hours to find out that you need to use .objects()
        # don't be like me
        new_dict = {
            "rover_id": item.rover_id,
            "timestamp": item.timestamp,
            "lat": item.lat,
            "long": item.long,
            "alt": item.alt,
            "voltage": item.voltage,
            "temperature": item.temperature
        }
        dicts.append(new_dict)
    
    return dicts


@app.route("/", methods=["POST"])
def ingest():
    data = request.json

    forms = []
    for item in data:
        try:
            if "id" in item.keys():
                forms.append(BaseDataForm.from_json(item))
            elif "rover_id" in item.keys():
                forms.append(RoverDataForm.from_json(item))
            else:
                raise ValueError("JSON does not contain required fields")
        except ValueError as e:
            abort(
                400,
                f"""JSON item is invalid:
                  {item}
                  {str(e)}""",
            )

    for form in forms:
        items_to_save = []

        if isinstance(form, RoverDataForm):
            items_to_save.append(GPSReading.from_rover_form(form))
            items_to_save.append(VoltageReading.from_rover_form(form))
            items_to_save.append(TemperatureReading.from_rover_form(form))
        elif isinstance(form, BaseDataForm):
            items_to_save.append(VoltageReading.from_base_form(form))
            items_to_save.append(TemperatureReading.from_base_form(form))
        else:
            raise NotImplementedError(
                f"Form type {type(item)} has no conversion to models"
            )

        for item in items_to_save:
            try:
                item.save()
            except IntegrityError as e:
                # skips individual items that can't be inserted for some reason
                # this is usually because it's a duplicate entry (and conflicts based on rover id and timestamp)
                # NOTE: this may be too inclusive but it's probably fine
                print(f"Item skipped!: {str(e)}")

    return "OK"
