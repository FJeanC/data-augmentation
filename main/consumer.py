import pika
import json
from datetime import datetime
from message_handler import Messagehandler


class Consumer:
    """Consome as mensagens da fila e manda as mensagens para o extrator.
    """
    def __init__(self, queue_name, rabbitmq_host="localhost"):
        self.rabbitmq_host = rabbitmq_host
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_host))
        self.channel = self.connection.channel()
        self.id = 1

    def consume(self):
        """Consome as mensagens da fila do RabbitMQ.
        """
        self.channel.queue_declare(queue=self.queue_name)
        def callback(ch, method, _, body):
            ope_start_time = datetime.utcnow().timestamp()
            message = json.loads(body)
            handler = Messagehandler(message, ope_start_time, self.id, ch, method)
            handler.handle_message()
            self.id += 1
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

# Inicializa o loop principal
consumer = Consumer('video_reference')
consumer.consume()
consumer.connection.close()
