from confluent_kafka import Consumer, KafkaException
import os

broker = os.environ.get('KAFKA_BROKER', 'localhost:9092')

consumer = Consumer({
    'bootstrap.servers': broker,
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

def consume_messages(topic):
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
            print(f'Received message: {msg.value().decode("utf-8")}')
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
