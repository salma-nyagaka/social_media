from confluent_kafka import Producer
import os

broker = os.environ.get('KAFKA_BROKER', 'localhost:9092')

producer = Producer({'bootstrap.servers': broker})

def send_message(topic, message):
    producer.produce(topic, message.encode('utf-8'))
    producer.flush()
