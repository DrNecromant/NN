import unittest
import random
from math import sqrt
import requests

from main import app
from flask_api import status

from consts import *

# generate random data
coord = [(x, y) for x in xrange(1, 1000) for y in xrange(1, 1000)]
random.shuffle(coord)

class TestNN(unittest.TestCase):
	"""
	Integration test for NN
	"""
	def setUp(self):
		self.baseurl = "http://127.0.0.1:5000/v1/NN"
		self.user_count = 10000
		self.radius = 300
		self.user_id = 1
		self.page_size = 238

	def testCheckAlgorythm(self):
		"""
		Add 10k data with rest
		Get kNN with binary algorythm
		Calculate all distances manually
		Compare results
		"""
		# generate data
		print "Generage %s users..." % self.user_count
		url = "%s/users" % self.baseurl
		for i in range(self.user_count):
			res = requests.post(url, data = '{"x": "%s", "y": "%s"}' % coord.pop())
			self.assertEqual(res.status_code, status.HTTP_201_CREATED)
			
		Rarg = "R=%s" % self.radius
		Uarg = "U=%s" % self.user_id
		Darg = "dist=Y"

		print "Get kNN by binary algorythm..."
		url = "%s/users/knn" % self.baseurl
		url = "%s?%s&%s" % (url, Rarg, Uarg)
		res = requests.get(url)
		self.assertEquals(res.status_code, status.HTTP_200_OK)
		result1 = res.json()["result"]

		print "Get kNN by calculating all distances..."
		url = "%s/users/knn" % self.baseurl
		url = "%s?%s&%s&%s" % (url, Rarg, Uarg, Darg)
		res = requests.get(url)
		self.assertEquals(res.status_code, status.HTTP_200_OK)
		result2 = res.json()["result"]

		self.assertEquals(result1, result2)
		print "Results are equal", result1, result2
				
if __name__ == '__main__':
    unittest.main()
