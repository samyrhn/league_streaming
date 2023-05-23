from kafka_producer.topic_producer import TopicProducer
from riot_api.riot_fetcher import RiotFetcher

import logging

logging.basicConfig(level = logging.INFO, force=True)   
logger = logging.getLogger(__name__)

def main():
    logger.debug('Instantiating classes...')
    rf = RiotFetcher()
    tp = TopicProducer()
    logger.debug('Classes instantiated successfully.')

    logger.debug('Acquiring player data...')
    data = rf.get_player_current_game(player_name='VC É NOSSO')
    if data:
        tp.send_data_to_kafka(data)

    tp.close()
    return

def lambda_handler(event, context=None):
    main()