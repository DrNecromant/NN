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
			
		print "Get kNN by binary algorythm..."
		url = "%s/users/knn" % self.baseurl
		Rarg = "R=%s" % self.radius
		Uarg = "U=%s" % self.user_id
		url = "%s?%s&%s" % (url, Rarg, Uarg)
		res = requests.get(url)
		self.assertEquals(res.status_code, status.HTTP_200_OK)
		result1 = res.json()["result"]

		print "Get kNN by calculating all distances..."
		result2 = 0
		url = "%s/users/%s" % (self.baseurl, self.user_id)
		res = requests.get(url)
		self.assertEquals(res.status_code, status.HTTP_200_OK)
		json_result = res.json()
		x0 = json_result["x"]
		y0 = json_result["y"]
		url = "%s/users/info" % self.baseurl
		res = requests.get(url)
		self.assertEquals(res.status_code, status.HTTP_200_OK)
		user_count = res.json()["user_count"]
		print "Fetching %s users..." % user_count
		page_count = user_count / self.page_size
		if user_count % self.page_size:
			page_count += 1
		for page_id in range(page_count):
			url = "%s/users?pagesize=%s&page=%s" % (self.baseurl, self.page_size, page_id)
			res = requests.get(url)
			self.assertEquals(res.status_code, status.HTTP_200_OK)
			json_result = res.json()["users"]
			for user_id in json_result:
				x = json_result[user_id]["x"]
				y = json_result[user_id]["y"]
				if sqrt((x0 - x) ** 2 + (y0 - y) ** 2) <= self.radius:
					result2 += 1
		# exclude initial user
		result2 -= 1
		self.assertEquals(result1, result2)
		print "Results are equal"
				
if __name__ == '__main__':
    unittest.main()
