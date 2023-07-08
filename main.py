from flask import Flask, request, abort
from peewee import SqliteDatabase
from forms import *
from enum import Enum
from models.RoverData import *
from datetime import datetime

app = Flask(__name__)

db.create_tables([RoverData])

@app.route('/', methods=['POST'])
def main():
    data = request.json
    forms = []

    for item in data:
        try:
            forms.append(RoverDataForm.from_json(item))
            continue
        except ValueError:
            pass

        try:
            forms.append(BaseDataForm.from_json(item))
            continue
        except ValueError:
            pass

        return abort(400, f"JSON is invalid: {item}")
    
    for form in forms:
        if isinstance(form, RoverDataForm):
            roverData = RoverData.from_rover_form(form)
            roverData.save()
        if isinstance(form, (RoverDataForm, BaseDataForm)):
            pass #TODO: Voltage info
    
    return "OK"