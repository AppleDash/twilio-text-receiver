import os
import flask
import flask_migrate

import flask_sqlalchemy as sqlalchemy

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
db = sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate(app, db)

# this is down here because message.py imports db from app.py (this file), so it needs to be initialized first.
from models.message import Message

# this function handles the webhook endpoint, which is called by Twilio when we receive a text on our number.
@app.route('/webhook')
def handle_webhook():
    pass


# this function handles the root endpoint, which is where texts that have been received will be displayed.
@app.route('/')
def handle_index():
    pass
