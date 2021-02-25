
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import logging
from sdgFinder import SDGFinder


app = Flask(__name__)
CORS(app)
api = Api(app)

# Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("query")


sdg = SDGFinder()

file = open("index_html", "r")
hello_ht = file.read()
file.close()


# logging.basicConfig(filename="Usage.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

@app.route("/")
def hello():
    # app.logger.info('View Website')
    return hello_ht

class Search(Resource):
    def post(self):
        # app.logger.info('Use basic search')
        args = parser.parse_args()
        _result = sdg.getSDG(str(args["query"]), detailed=False)
        return _result

api.add_resource(Search, "/search")


class SearchDet(Resource):
    def post(self):
        # app.logger.info('use advanced search')
        args = parser.parse_args()
        _result = sdg.getSDG(str(args["query"]), detailed=True)
        return _result

api.add_resource(SearchDet, "/detailed_search")


if __name__ == "__main__":
    # logging.basicConfig(filename='usage.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True)
