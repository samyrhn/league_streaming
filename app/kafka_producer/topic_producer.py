from kafka import KafkaProducer
import json
import logging
import os

class TopicProducer:
    def __init__(self, bootstrap_servers=[os.environ['BOOTSTRAP_SERVERS']]):
        self.logger = logging.getLogger(__name__)
        self.producer = self.connect_to_broker(bootstrap_servers)
    
    def on_send_success(self, record_metadata):
        self.logger.info('Message sent successfully!')
        self.logger.debug(record_metadata)
        return

    def on_send_error(self, excp):
        self.logger.error('Message not sent.', exc_info=excp)
        return

    def connect_to_broker(self, bootstrap_servers):
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        if producer.bootstrap_connected():
            self.logger.info('Connection to broker established.')
            return producer
        
        raise RuntimeError('Unable to connect to broker')

    def send_data_to_kafka(self,json_data, topic = 'league-streaming-topic'):
        self.producer.send(topic, json_data).add_callback(self.on_send_success).add_errback(self.on_send_error)
        self.producer.flush()
        return

    def close(self):
        self.producer.close()

