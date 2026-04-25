from flask_sqlalchemy import SQLAlchemy
import json

db: SQLAlchemy = SQLAlchemy()

class Router(db.Model):

    __tablename__ = 'routers'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String)
    motd = db.Column(db.String)
    interfaces = db.Column(db.String)

    def __repr__(self) -> str:
        return f'Router(id={self.id!r}, hostname={self.hostname!r})'

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'hostname': self.hostname,
            'motd': self.motd,
            'interfaces':  json.loads(self.interfaces) if self.interfaces is not None else {}
        }

class Switch(db.Model):

    __tablename__ = 'switches'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String)

    ip = db.Column(db.String)
    netmask = db.Column(db.String)
    motd = db.Column(db.String)
    ports = db.Column(db.String)
    interfaces = db.Column(db.String)


    def __repr__(self):
        return f'Switch(id={self.id!r}, hostname={self.hostname!r}) ip={self.ip!r} netmask={self.netmask!r}'

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'hostname': self.hostname,
            'motd': self.motd,
            'ports': json.loads(self.ports) if self.ports is not None else {},
            'interfaces': json.loads(self.interfaces) if self.interfaces is not None else {},
        }