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

class UserList(Resource):
	"""
	Controller to show and modify userlist
	If user exists return 409 Conflict 
	Example:
		curl http://127.0.0.1:5000/v1/NN/users -X POST -d '{"x": 1, "y": 2}'
		curl http://127.0.0.1:5000/v1/NN/users -X GET
	"""

	def get(self):
		"""
		Get user list
		"""
		#TODO: show only first 100 records, add parametr to show next records
		return {}, status.HTTP_200_OK

	def post(self):
		"""
		Fetch json data from body ignoring Content-Type header by force flag
		If body is not json flask restfull api automatically handles that
		Store new user in DB and return user url
		"""
		json_data = request.get_json(force = True)
		if "x" not in json_data or "y" not in json_data:
			return {
				"message": "Bad request. JSON 'x' and 'y' keys are requied."
			}, status.HTTP_400_BAD_REQUEST
		# TODO: Check user with the same coord and return 409 if it exists
		# TODO: PUT params to DB and get ID
		user_id = 1
		return {
			"message": "Created",
			"user_url": "%s/users/%s" %(BASEURL, user_id)
		}, status.HTTP_201_CREATED

class User(Resource):
	"""
	Controller for other user CRUD actions
	Example:
		curl http://127.0.0.1:5000/v1/NN/users/id -X GET
		curl http://127.0.0.1:5000/v1/NN/users/id/update -X POST -d '{"x": 4}'
		curl http://127.0.0.1:5000/v1/NN/users/id/delete -X DELETE
	"""

	def get(self, user_id):
		return {}, status.HTTP_200_OK
		
	def post(self, user_id):
		return {}, status.HTTP_200_OK
		
	def delete(self, user_id):
		return {}, status.HTTP_200_OK

api.add_resource(UserList, "%s/users" % BASEURL)
api.add_resource(User, "%s/users/<int:user_id>" % BASEURL)

if __name__ == '__main__':
	app.run(debug = True)
