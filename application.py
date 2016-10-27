import json
from flask import Flask, render_template, request

from config import ES_INDEX
from settings import es


application = Flask(__name__)


@application.route('/')
def index():
	coords = []
	return render_template("welcome.html",
                           coords=json.dumps(coords),
                        )


@application.route('/category', methods=['GET'])
def category():
	if request.method == 'GET':
		category = request.args.get('category')
		es_data = es.search(index=ES_INDEX, body={"query": {"match": {"text": category}}}, size=600)
		coords = []
		for data in es_data['hits']['hits']:
			if len(data['_source']['coordinates']) > 0:
				geo_data = data['_source']['coordinates'][0]['geometry']['location']
				lat = geo_data['lat']
				lng = geo_data['lng']
				coords.append([lat, lng])
		return render_template("twittmap.html",
	                           coords=json.dumps(coords),
	                        )


if __name__ == "__main__":
    application.run(debug=True)