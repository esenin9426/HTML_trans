from confluent_kafka import Consumer

# Конфигурация для подключения к Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',  # адрес и порт сервера Kafka
    'group.id': 'my-consumer-group_4',  # идентификатор группы потребителей
    'auto.offset.reset': 'earliest'  # начать чтение с самого начала топика
}

# Создание объекта потребителя Kafka
consumer = Consumer(conf)

# Подписка на топик Kafka
consumer.subscribe(['topic_name'])

# Чтение сообщений из топика Kafka
while True:
    msg = consumer.poll(1.0)  # ожидание нового сообщения в течение 1 секунды

    if msg is None:
        continue

    if msg.error():
        print(f"Ошибка при чтении сообщения: {msg.error()}")
        continue

    print(msg.value().decode('utf-8'))

# Закрытие соединения с Kafka
consumer.close()