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

class DBUserStats(object):
	"""
	Get stats from DBUser such as:
	min, max, average, total with where clause
	"""

	def __init__(self, offsetX = None, offsetY = None, \
				limitX = None, limitY = None):
		query = db.session.query(
			db.func.min(DBUser.x).label("minX"), \
			db.func.min(DBUser.y).label("minY"), \
			db.func.max(DBUser.x).label("maxX"), \
			db.func.max(DBUser.y).label("maxY"), \
			db.func.avg(DBUser.x).label("avgX"), \
			db.func.avg(DBUser.y).label("avgY"), \
			db.func.count(DBUser.id).label("count"), \
		)

		if offsetX is not None:
			query = query.filter(DBUser.x >= offsetX)
		if offsetY is not None:
			query = query.filter(DBUser.y >= offsetY)
		if limitX is not None:
			query = query.filter(DBUser.x <= limitX)
		if limitY is not None:
			query = query.filter(DBUser.y <= limitY)

		self.result = query.one()

	@property
	def rect(self):
		"""
		return rect corner coordinates
		"""
		return (
			(self.result.minX, self.result.minY), \
			(self.result.minX, self.result.maxY), \
			(self.result.maxX, self.result.minY), \
			(self.result.maxX, self.result.maxY), \
		)

	@property
	def minX(self):
		return self.result.minX

	@property
	def minY(self):
		return self.result.minY

	@property
	def maxX(self):
		return self.result.maxX

	@property
	def maxY(self):
		return self.result.maxY

	@property
	def avgX(self):
		return int(self.result.avgX)

	@property
	def avgY(self):
		return int(self.result.avgY)

	@property
	def count(self):
		return self.result.count
