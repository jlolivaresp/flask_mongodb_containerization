import requests

# Overpass API URL
overpass_url = "http://overpass-api.de/api/interpreter"

# Format for querying "ways" from the Overpass API
QUERY_WAY_STRING_FORMAT = """
            [out:json];
            (way({id});
            );
            out center;
            """


class Overpass:
    """
    Service class of the Open Street Map Overpass API.
    """

    def __init__(self):
        """
        Constructor method.
        """
        self.response = None

    @staticmethod
    def query(query_string: str):
        """
        Queries directly to the API with a given query string.

        :param query_string: [string] String to query data.
        :return: [json] Json response from the query.
        """
        response = requests.get(overpass_url, params={'data': query_string})
        data = response.json()
        return data

    def way(self, way_id: str):
        """
        Gets the information of a way by providing a <way_id> and sets the response to self.response.

        :param way_id: [string] Way ID
        :return: [self]
        """

        way_query_string_format = QUERY_WAY_STRING_FORMAT.format(id=way_id)
        self.response = self.query(way_query_string_format)
        return self

    def get_way_node_list(self):
        """
        Gets the node list from the self.response. You can do way(way_id=<way_id>).get_way_node_list()

        :return: [array] Array containing the list of nodes of the queried way.
        """

        # If self.response exists and contains "elements", return "nodes"
        if self.response and self.response.get('elements'):
            elements = self.response.get('elements')[0]
            nodes = elements.get('nodes')
            return nodes
        else:
            return list()
