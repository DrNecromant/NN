import unittest
import random
from math import sqrt
import time
from pprint import pprint

from main import app
from flask_api import status

from consts import *
from models import *

db.app = app
db.init_app(app)
client = app.test_client()

# define initial variables
initial_user_id_list = [1, 2, 3]
radius_list = [10, 50, 100 , 500, 1000]
baseurl = "v1/NN"

def testAllDistanceSearch(radius, initial_user_id):
	url = "%s/users/knn?R=%s&U=%s&dist=Y" % (baseurl, radius, initial_user_id)
	res = client.get(url)
	return eval(res.get_data())["result"]

def testBinarySearch(radius, initial_user_id):
	url = "%s/users/knn?R=%s&U=%s" % (baseurl, radius, initial_user_id)
	res = client.get(url)
	return eval(res.get_data())["result"]

if __name__ == '__main__':
	results = dict()
	print "\ntest | attempt_id | radius | knn | exec_time"
	for test in (testBinarySearch, testAllDistanceSearch):
		timelist = list()
		for radius in radius_list:
			for initial_user_id in initial_user_id_list:
				init_time = time.time()
				knn = test(radius, initial_user_id)
				exec_time = time.time() - init_time
				timelist.append(exec_time)
				print "\n", test.__name__, initial_user_id, radius, knn, exec_time, 
		results[test.__name__] = sum(timelist) / len(timelist)
	print "\n\nRESULTS:\n"
	for testname in results:
		print "\t%s: %s" %(testname, results[testname])
