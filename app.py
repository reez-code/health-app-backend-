from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
migrate=Migrate(app,db)

from models import Doctor, Appointment, Admin
#import routes

if __name__ == "__main__":
    app.run(debug=True)
    