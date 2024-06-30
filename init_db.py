from ext import app, db
from models import Reviewmodel, User, Comment
import datetime

time = datetime.datetime.now()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin_user = User(username='admin', password='adminpass', phonenum=500000000, date = time, role='Admin')
    admin_user.create()