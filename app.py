from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cherryteadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.session.autoflush = False
# import database api
import dbapi


# Homepage
@app.route('/')
def index():
	return render_template('index.html')

# Save email