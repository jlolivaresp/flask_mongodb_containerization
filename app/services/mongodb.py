import os
from pymongo import MongoClient

db_username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
db_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
db_url_format = 'mongodb://{username}:{password}@mongodb-service:27017/'
db_url = db_url_format.format(username=db_username, password=db_password)


class MongoDB(object):
    """
    Service class to connect to MongoDB database.
    """

    # Singleton pattern: instantiates the database class to a single instance to avoid multiples instances in the code
    class __MongoDB:
        def __init__(self, arg):
            self.val = arg
            self.db = MongoClient(db_url).mia

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __init__(self, arg):
        """
        Constructor method.
        :param arg: [string] Name of the DB instance.
        """
        if not MongoDB.instance:
            MongoDB.instance = MongoDB.__MongoDB(arg)
        else:
            MongoDB.instance.val = arg

        self.db = MongoClient(db_url).mia
