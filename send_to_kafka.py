from confluent_kafka import Producer

# Create a Producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092'
}

# Create a Producer object
producer = Producer(conf)

# Send messages to Kafka
for i in range(100):
    message = f"Message {i}"
    producer.produce('topic_name', value=message)
    producer.flush()

# Close the Producer
producer.close()
