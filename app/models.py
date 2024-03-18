from . import db
from werkzeug.utils import secure_filename

    
class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    num_rooms = db.Column(db.Integer)
    num_bathrooms = db.Column(db.Integer)
    price = db.Column(db.Numeric(10,2))  # Assuming a maximum price with two decimal places
    type = db.Column(db.String(80))
    location = db.Column(db.String(255))
    photo = db.Column(db.String(255))  # Path to the photo

    def __init__(self, title, description, num_rooms, num_bathrooms, price, type, location, photo):
        self.title = title
        self.description = description
        self.num_rooms = num_rooms
        self.num_bathrooms = num_bathrooms
        self.price = price
        self.type = type
        self.location = location
        self.photo = secure_filename(photo)  # Ensures the filename is safe to use as a filesystem path

    def __repr__(self):
        return '<Property %r>' % self.title

