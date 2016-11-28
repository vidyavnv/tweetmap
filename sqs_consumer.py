import json

from elasticsearch import Elasticsearch
from threading import Thread

from settings import topic, arn, ALCHEMY_LANGUAGE, queue


def consumer():
	while True:
		# try:
		messages = queue.receive_messages(MaxNumberOfMessages=1,WaitTimeSeconds=20)
		for message in messages:
			orig_msg = json.loads(message.body)
			if 'text' in orig_msg:
				print(orig_msg['text'])
				response = ALCHEMY_LANGUAGE.sentiment(text=orig_msg['text'])
				print(response)
				sentiment = response["docSentiment"]["type"]
				orig_msg['sentiment'] = sentiment
				sns_response = topic.publish(TopicArn=arn,
	                                         Message=json.dumps(orig_msg),
	                                         Subject='tweet')

		# except Exception as e:
		# 	print e
		# 	continue


def main():
	for i in xrange(2):
		thread = Thread(target=consumer)
		thread.start()


if __name__ == '__main__':
	main()

