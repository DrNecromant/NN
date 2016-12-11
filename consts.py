BASEURL = "/v1/NN"

class ProductionConfig(object):
	TESTING = False
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = "sqlite:///production.db"
	SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(object):
	TESTING = True
	DEBUG = True
	DATABASE_URI = 'sqlite:///:memory:'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
