import json
import requests
from flask import Flask, render_template, request, redirect, url_for

from config import ES_INDEX
from settings import es


application = Flask(__name__)


@application.route('/', methods=['GET', 'POST'])
def index():
	es_data = es.search(index=ES_INDEX, size=10000)
	coords = []
	for data in es_data['hits']['hits']:
		if len(data['_source']['coordinates']) > 0:
			geo_data = data['_source']['coordinates']['location'].split(',')
			lat = float(geo_data[0])
			lng = float(geo_data[1])
			sentiment = data['_source']['sentiment']
			coords.append([lat, lng, sentiment])
	return render_template("welcome.html",
                           coords=coords,
                           msg=None)


@application.route('/category', methods=['GET'])
def category():
	if request.method == 'GET':
		category = request.args.get('category')
		es_data = es.search(index=ES_INDEX, body={"query": {"match": {"text": 
			{"query": category, 'zero_terms_query': "all"}}}}, size=10000)
		coords = []
		for data in es_data['hits']['hits']:
			if len(data['_source']['coordinates']) > 0:
				geo_data = data['_source']['coordinates']['location'].split(',')
				lat = float(geo_data[0])
				lng = float(geo_data[1])
				sentiment = data['_source']['sentiment']
				coords.append([lat, lng, sentiment])
		return render_template("twittmap.html",
	                           coords=coords,
	                           category=category
	                        )


@application.route('/sns', methods = ['POST'])
def sns():
    try:
        js = json.loads(request.data)
    except:
        return render_template("welcome.html",
	                           coords=[],
	                           category='Invalid JSON'
	                        )

    hdr = request.headers.get('X-Amz-Sns-Message-Type')
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
        r = requests.get(js['SubscribeURL'])

    if hdr == 'Notification':
        print(js["Message"], js['Timestamp'])

    es.index(index="tweets", doc_type="tweets", 
					body=js['Message'])
    


if __name__ == "__main__":
    application.run(debug=True)