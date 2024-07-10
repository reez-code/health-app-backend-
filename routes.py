from flask import Flask ,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config["SQLALCHEMY DATABASE URI"]="sqlite:///test.db"

db=SQLAlchemy(app)
migrate=Migrate(app,db)

from models import Doctor,Appointment,Admin

@app.route("/doctors", methods=["GET", 'POST'])
def get_doctors():
    if request.method == "GET":
        doctors= Doctor.query.all()