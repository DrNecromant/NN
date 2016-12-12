from flask import Flask, request
from flask_api import status
from flask_restful import Resource, Api

from consts import *
from models import *

app = Flask("NN")
# Load config for app
if __name__ == '__main__':
	app.config.from_object('consts.ProductionConfig')
else:
	app.config.from_object('consts.TestingConfig')
# Catch all unexpected 404s in json format
api = Api(app, catch_all_404s = True)

# Init DB
db.app = app
db.init_app(app)
db.create_all()

class Info(Resource):
	"""
	Provide information about Users
	"""

	def get(self):
		user_count = DBUser.query.count()
		return {
			"message": "OK",
			"user_count": user_count
		}, status.HTTP_200_OK

class UserList(Resource):
	"""
	Controller to show and extend userlist
	If user exists return 409 Conflict 
	Example:
		curl http://127.0.0.1:5000/v1/NN/users -X POST -d '{"x": 1, "y": 2}'
		curl http://127.0.0.1:5000/v1/NN/users?page=2&pagesize=5 -X GET
	"""

	def get(self):
		"""
		Get user list
		By default show only first 100 records
		page and pagesize are configurable by request args
		"""
		page = int(request.args.get('page', 0))
		pagesize = int(request.args.get('pagesize', 100))
		query = DBUser.query
		query = query.offset(page * pagesize)
		query = query.limit(pagesize)
		users = query.all()
		if not users:
			return {
				"message": "Users not found"
			}, status.HTTP_404_NOT_FOUND

		# Create json for each user in list
		json_users = dict()
		for user in users:
			json_users[user.id] = {
				"x": user.x,
				"y": user.y,
				"user_url": "%s/%s" %(request.url, user.id)
			}

		return {
			"message": "OK",
			"users": json_users
		}, status.HTTP_200_OK

	def post(self):
		"""
		Fetch json data from body ignoring Content-Type header by force flag
		If body is not json flask restfull api automatically handles that
		Store new user in DB and return user url
		"""
		json_data = request.get_json(force = True)
		if "x" not in json_data or "y" not in json_data:
			return {
				"message": "Bad request. x and y keys are requied."
			}, status.HTTP_400_BAD_REQUEST

		x = json_data["x"]
		y = json_data["y"]

		# Check user exists. If so, return conflict
		user = DBUser.query.filter_by(x = x, y = y).first()
		if user:
			return {
				"message": "Conflict. User (%s, %s) exists" % (x, y),
			}, status.HTTP_409_CONFLICT
		# Add user into DB
		user = DBUser(x, y)
		db.session.add(user)
		db.session.flush()

		db.session.commit()
		# Get user ID and return url
		return {
			"message": "Created",
			"user_url": "%s/%s" %(request.url, user.id)
		}, status.HTTP_201_CREATED

class User(Resource):
	"""
	Controller for other user CRUD actions
	Example:
		curl http://127.0.0.1:5000/v1/NN/users/id -X GET
		curl http://127.0.0.1:5000/v1/NN/users/id/update -X POST -d '{"x": 4}'
		curl http://127.0.0.1:5000/v1/NN/users/id/delete -X DELETE
	"""

	def _not_found_error(self, user_id):
		return {
			"message": "User %s not found" % user_id
		}, status.HTTP_404_NOT_FOUND

	def get(self, user_id):
		"""
		Return User object
		"""
		user = DBUser.query.filter_by(id = user_id).first()
		if not user:
			return self._not_found_error(user_id)
		return {
			"message": "OK",
			"x": user.x,
			"y": user.y
		}, status.HTTP_200_OK
		
	def post(self, user_id):
		"""
		Update User object
		"""
		user = DBUser.query.filter_by(id = user_id).first()
		if not user:
			return self._not_found_error(user_id)
		json_data = request.get_json(force = True)
		if "x" not in json_data and "y" not in json_data:
			return {
				"message": "Bad request. x or y keys are requied."
			}, status.HTTP_400_BAD_REQUEST

		x = json_data.get("x")
		y = json_data.get("y")
		if x:
			user.x = x
		if y:
			user.y = y
		db.session.flush()
		db.session.commit()
		return {
			"message": "OK",
			"user_url": "%s/%s" %(request.url, user.id)
		}, status.HTTP_200_OK
		
	def delete(self, user_id):
		"""
		Delete User object
		"""
		user = DBUser.query.filter_by(id = user_id).first()
		if not user:
			return self._not_found_error(user_id)
		user.query.delete()
		db.session.commit()
		return {
			"message": "OK"
		}, status.HTTP_200_OK

class Knn(Resource):
	"""
	Controller to find K nearest neighbors
	R (raduis) and U (user_id) arguments are mandatory
	Example:
		curl http://127.0.0.1:5000/v1/NN/users/knn?U=10&R=10 -X GET
	"""

	def get(self):
		radius = int(request.args.get('R', 0))
		user_id = int(request.args.get('U', 0))
		if not radius:
			return {
				"message": "Bad request. R argument is required."
			}, status.HTTP_400_BAD_REQUEST
		if not user_id:
			return {
				"message": "Bad request. U argument is required."
			}, status.HTTP_400_BAD_REQUEST

		#TODO: main algorithm

		return {
			"message": "OK",
			"result": 0,
		}, status.HTTP_200_OK

api.add_resource(UserList, "%s/users" % BASEURL)
api.add_resource(Info, "%s/users/info" % BASEURL)
api.add_resource(User, "%s/users/<int:user_id>" % BASEURL)
api.add_resource(Knn, "%s/users/knn" % BASEURL)

if __name__ == '__main__':
	app.run(debug = True)
