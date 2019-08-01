import os
import flask
import datetime
import flask_migrate
import flask_sqlalchemy

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

TOKEN = os.environ['TOKEN']

# this is down here because message.py imports db from app.py (this file), so it needs to be initialized first.
from models.message import Message

# this function handles the webhook endpoint, which is called by Twilio when we receive a text on our number.
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    request = flask.request

    if request.args['token'] != TOKEN:
        return 'bad token', 403

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


if __name__ == '__main__':
    app.run()
