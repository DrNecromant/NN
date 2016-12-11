import unittest
import random

from main import app
from flask_api import status

from consts import *
from models import *

db.app = app
db.init_app(app)
db.create_all()

# generate random data
xs = range(1, 100)
random.shuffle(xs)
ys = range(1, 100)
random.shuffle(ys)

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
	Unittests for UserList
	"""
	def setUp(self):
		self.client = app.test_client()
		self.url = "%s/users" % BASEURL
		# lambda to generate random unique coordinates
		self.getCoords = lambda: (xs.pop(), ys.pop())

	def testAddUser(self):
		"""
		Try to add new user
		Check return code is 201
		"""
		res = self.client.post(self.url, data = '{"x": %s, "y": %s}' % self.getCoords())
		self.assertEquals(res.status_code, status.HTTP_201_CREATED)

	def testAddInvalidUser(self):
		"""
		Try to add new user without x or y
		Check return code is 400
		"""
		res = self.client.post(self.url, data = '{"x": %s}' % xs.pop())
		self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
		res = self.client.post(self.url, data = '{"y": %s}' % ys.pop())
		self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

	def testAddiExistedUser(self):
		"""
		Try to add new existed user
		Check return code is 409
		"""
		coords = self.getCoords()
		self.client.post(self.url, data = '{"x": %s, "y": %s}' % coords)
		res = self.client.post(self.url, data = '{"x": %s, "y": %s}' % coords)
		self.assertEquals(res.status_code, status.HTTP_409_CONFLICT)

	def testEmptyUserList(self):
		"""
		Try to get empty UserList
		Check return code is 400
		"""
		# Clean Users table firstt
		DBUser.query.delete()
		res = self.client.get(self.url)
		self.assertEquals(res.status_code, status.HTTP_404_NOT_FOUND)

	def testFullUserList(self):
		"""
		Try to get UserList
		Check return code is 200
		"""
		self.client.post(self.url, data = '{"x": %s, "y": %s}' % self.getCoords())
		res = self.client.get(self.url)
		self.assertEquals(res.status_code, status.HTTP_200_OK)

class TestInfo(unittest.TestCase):
	"""
	Unittests for Info
	"""
	def setUp(self):
		self.client = app.test_client()
		self.url = "%s/users/info" % BASEURL

	def testGetInfo(self):
		"""
		Try to get info
		Check return code is 200
		"""
		res = self.client.post(self.url)
		self.assertEquals(res.status_code, status.HTTP_200_OK)

if __name__ == "__main__":
	suites = list()
	for test in (TestDB, TestUserList):
		suites.append(unittest.TestLoader().loadTestsFromTestCase(test))
	suite = unittest.TestSuite(suites)
	results = unittest.TextTestRunner(verbosity = 2).run(suite)
