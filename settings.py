import googlemaps

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from config import GMAP_KEY, AWS_ES_HOST, AWS_ES_PORT, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, 'es')

es = Elasticsearch(
    hosts=[{'host': AWS_ES_HOST, 'port': AWS_ES_PORT}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
# print(es.info())

gmaps = googlemaps.Client(key=GMAP_KEY)
