import boto3
import googlemaps

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from kafka import KafkaProducer
from kafka import KafkaConsumer
from watson_developer_cloud import AlchemyLanguageV1


from config import GMAP_KEY, AWS_ES_HOST, AWS_ES_PORT, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, ARN, WATSON_API_KEY

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, 'es')

es = Elasticsearch(
    hosts=[{'host': AWS_ES_HOST, 'port': AWS_ES_PORT}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())
# es = Elasticsearch()
gmaps = googlemaps.Client(key=GMAP_KEY)

kafka_producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
kafka_consumer = KafkaConsumer('tweets')

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='tweets')

SNS = boto3.resource('sns')
topic = SNS.Topic('tweets')
arn = ARN

ALCHEMY_LANGUAGE = AlchemyLanguageV1(api_key=WATSON_API_KEY)
