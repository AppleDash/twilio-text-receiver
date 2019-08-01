import os
import flask
import datetime
import twilio_util
import flask_migrate
import flask_sqlalchemy

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate(app, db)

# this is down here because message.py imports db from app.py (this file), so it needs to be initialized first.
from models.message import Message

# this function handles the webhook endpoint, which is called by Twilio when we receive a text on our number.
@app.route('/webhook')
@twilio_util.validate_twilio_request
def handle_webhook():
    request = flask.request

    message = Message(
        received_at=datetime.datetime.utcnow(),
        from_number=request.form['From'],
        to_number=request.form('To'),
        body=request.form('Body')
    )

    db.session.add(message)
    db.session.commit()


# this function handles the root endpoint, which is where texts that have been received will be displayed.
@app.route('/')
def handle_index():
    return flask.render_template('index.html.j2', messages=Message.query.order_by(Message.received_at))
