from app.services.overpass import Overpass
from app.model.way import Way
from flask import Flask, jsonify

# Create Flask object
app = Flask(__name__)

# Initialize Overpass service class
overpass = Overpass()

# Initialize Way model class
way = Way()


# Route HTTP requests from http://0.0.0.0:<PORT_NUMBER>/
@app.route("/")
def add_ways_to_db():
    """
    Queries a list of ways from the Overpass API and stores their associated nodes to the Way collection of the DB.

    :return: [json] Json with the information of the data inserted in the DB in the form:
    {
        <way_id>: <inserted object>
    }.
    """

    # List of ways to query from the Open Street Map API
    way_ids = ['4848900793', '2388248', '253408665']

    try:
        db_insertions = dict()

        for way_id in way_ids:
            node_list = overpass.way(way_id).get_way_node_list()
            insert_response = way.insert(node_list)
            db_insertions = dict(**db_insertions, **{way_id: str(insert_response)})

        return jsonify(db_insertions)

    except Exception as e:
        return jsonify(str(e))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
