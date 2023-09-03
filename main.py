from flask import Flask, request, abort, jsonify
from forms import *
from models import *
from peewee import IntegrityError
import csv
import time

app = Flask(__name__)

#db.create_tables([GPSReading, VoltageReading, TemperatureReading])


@app.route("/<id>", methods=["GET"])
def retrieve(id):
    id = int(id)

    # joins the tables based on rover_id and timestamp combined
    db.connect()
    items = (TemperatureReading.select(
        TemperatureReading.rover_id.alias("rover_id"),
        TemperatureReading.timestamp.alias("timestamp"),
        GPSReading.latitude.alias("lat"),
        GPSReading.longitude.alias("long"),
        GPSReading.altitude.alias("alt"),
        VoltageReading.value.alias("voltage"),
        TemperatureReading.value.alias("temperature")
    ).join_from(
        TemperatureReading, VoltageReading,
        on=((TemperatureReading.rover_id == VoltageReading.rover_id) & (TemperatureReading.timestamp == VoltageReading.timestamp))
    ).join_from(
        TemperatureReading, GPSReading,
        JOIN.LEFT_OUTER,
        on=((TemperatureReading.rover_id == GPSReading.rover_id) & (TemperatureReading.timestamp == GPSReading.timestamp))
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
    db.close() # I'm not sure if peewee does lazy loading or not so just in case the close is here
    
    return jsonify(dicts)


@app.route("/", methods=["POST"], strict_slashes=False)
def ingest():
    data = request.json

    with open("/var/www/html/incoming/posts.txt", "a") as file:
        ts = datetime.now().strftime("%Y/%m/%d,%H:%M:%S, ")
        file.write(ts + str(request.data, 'utf-8') + '\n')

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
            # abort(
            #     400,
            #     f"""JSON item is invalid:
            #       {item}
            #       {str(e)}""",
            # )
            # I am aware what I'm doing is a cardinal sin but it's easier
            # the embedded devices only need to know that the packet was received/processed
            pass #Skips the invalid entry individually

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

        db.connect()
        for item in items_to_save:
            try:
                item.save()
            except IntegrityError as e:
                # skips individual items that can't be inserted for some reason
                # this is usually because it's a duplicate entry (and conflicts based on rover id and timestamp)
                # NOTE: this may be too inclusive but it's probably fine
                print(f"Item skipped!: {str(e)}")
        db.close()

    return "OK"
