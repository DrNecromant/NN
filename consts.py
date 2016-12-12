BASEURL = "/v1/NN"
SQL_TESTDATA_COUNT = 100

class ProductionConfig(object):
	TESTING = False
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = "sqlite:///production.db"
	SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(object):
	TESTING = True
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
