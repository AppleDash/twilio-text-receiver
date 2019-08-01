from app import db
from sqlalchemy.dialects.postgresql import UUID


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(UUID, primary_key=True, server_default='gen_random_uuid()')
    received_at = db.Column(db.DateTime, nullable=False)
    from_number = db.Column(db.Text, nullable=False)
    to_number = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __init__(self, received_at, from_number, to_number, body):
        self.received_at = received_at
        self.from_number = from_number
        self.to_number = to_number
        self.body = body
