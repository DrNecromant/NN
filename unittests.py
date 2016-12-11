import unittest

from main import app
from flask_api import status

from consts import *
from models import *

db.app = app
db.init_app(app)
db.create_all()

class TestDB(unittest.TestCase):
	"""
	Unittests for DB
	"""
	def testDBUser(self):
		"""
		Try to create record in a table DBUser
		"""
		user = DBUser(x = 1, y = 1)
		db.session.add(user)
		db.session.commit()

class TestUserList(unittest.TestCase):
	"""
	Unittests for endpoints
	"""
	def setUp(self):
		self.client = app.test_client()
		self.url = "%s/users" % BASEURL

	def testAddUser(self):
		"""
		Try to add new user
		Check return code is 201
		"""
		res = self.client.post(self.url, data = '{"x": 2, "y": 2}')
		self.assertEquals(res.status_code, status.HTTP_201_CREATED)

	def testAddUser(self):
		"""
		Try to add new user without x or y
		Check return code is 400
		"""
		res = self.client.post(self.url, data = '{"x": 2}')
		self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
		res = self.client.post(self.url, data = '{"y": 2}')
		self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

	def testEmptyUserList(self):
		"""
		Try to get empty UserList
		Check return code is 400
		"""
		#TODO: remove data first
		pass

	def testFullUserList(self):
		"""
		Try to get UserList
		Check return code is 200
		"""
		self.client.post(self.url, data = '{"x": 3, "y": 3}')
		res = self.client.get(self.url)
		self.assertEquals(res.status_code, status.HTTP_200_OK)

if __name__ == "__main__":
	suites = list()
	for test in (TestDB, TestUserList):
		suites.append(unittest.TestLoader().loadTestsFromTestCase(test))
	suite = unittest.TestSuite(suites)
	results = unittest.TextTestRunner(verbosity = 2).run(suite)
