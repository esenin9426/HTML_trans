from confluent_kafka import Producer

# Create a Producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092,localhost:9093,localhost:9094'
}

# Create a Producer object
producer = Producer(conf)

# Send messages to Kafka
for i in range(10):
    message = f"Message {i}"
    producer.produce('topic_name', value=message)
    producer.flush()

# Close the Producer
producer.close()
