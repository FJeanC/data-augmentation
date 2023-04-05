import json
import pika

# Adiciona as mensagens do payload na fila

with open('../data/messages/payload.json') as f:
    messages = json.load(f)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='video_reference')

for message in messages:
    message_string = json.dumps(message)
    channel.basic_publish(exchange='', routing_key='video_reference', body=message_string)
    print(f'Message: {message_string}')

connection.close()
