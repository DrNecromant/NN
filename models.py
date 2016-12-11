from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DBUser(db.Model):
	"""
	Users with their coordinates
	"""
	id = db.Column(db.Integer, primary_key = True)
	x = db.Column(db.Integer)
	y = db.Column(db.Integer)

	def __init__(self, x, y):
		self.x = x
		self.y = y
