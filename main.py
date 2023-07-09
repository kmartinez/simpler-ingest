from flask import Flask, request, abort
from forms import *
from models import *

app = Flask(__name__)

db.create_tables([GPSReading, VoltageReading, TemperatureReading])

@app.route('/', methods=['POST'])
def main():
    data = request.json

    forms = []
    for item in data:
        try:
            if "id" in item.keys():
                forms.append(BaseDataForm.from_json(item))
            elif "rover_id" in item.keys():
                forms.append(RoverDataForm.from_json(item))
            else: raise ValueError("JSON does not contain required fields")
        except ValueError as e:
            abort(400, f"""JSON item is invalid:
                  {item}
                  {str(e)}""")
    
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
            raise NotImplementedError(f"Form type {type(item)} has no conversion to models")
        
        for item in items_to_save:
            item.save()
    
    return "OK"