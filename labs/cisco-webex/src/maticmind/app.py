import os
from flask import Flask, request, Response

from dotenv import load_dotenv

# load environment variables from '.env' file
load_dotenv()

# create flask instance
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")

# db connection ana start application
from models import db, User
import json

db.init_app(app)

# create all models
with app.app_context():
    db.create_all()

# this is a test endpoint. Add your logic to handle the incident correctly
# As a reference check routers.py file in this repo to learn how to interact with the database:
#  https://github.com/alarmfox/dtlab-api/tree/solution
# Official documentation: https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html
@app.route('/incident', methods=['POST'])
def test() -> str:
    # get incident data from request as json
    # data = request.get_json()

   
    users = User.query.all()

    # create room
    # add users
    # send first message
    return Response(json.dumps([user.to_dict() for user in users]), mimetype="application/json"), 200

