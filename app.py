from flask import Flask
from flask import Flask
from models import db
from auth import auth
#from todo import todo
from flask_jwt_extended import JWTManager
from todos import todo

 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'


db.init_app(app)

jwt = JWTManager(app)


app.register_blueprint(auth)
app.register_blueprint(todo)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()