from app.services.mongodb import MongoDB

# Initialize MongoDB instance
db = MongoDB('mongodb_instance').db


class Way:
    """
    DB Model for the Way collection.
    """

    def __init__(self):
        """
        Constructor method.
        """

        self.way = db.way

    def insert(self, nodes: list = None):
        """
        Inserts a list a nodes in the way collection with a unique identifier as its key.

        :param nodes: [array] Array of nodes to insert into the way collection.
        :return: [object] Inserted object.
        """

        inserted_id = self.way.insert_one(dict(nodes=nodes)).inserted_id
        return self.way.find_one(inserted_id)
