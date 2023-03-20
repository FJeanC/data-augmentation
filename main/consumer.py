import pika
import json
from extractor import Extractor
from datetime import datetime
from send_data_to_Register_API import send_data_to_Register_API
from pydantic import BaseModel, validator


class BaseMessage(BaseModel):
    video_ref: str
    frame_seconds_index: int
    op_type: str

    @validator('frame_seconds_index')
    def validate_frame_seconds_index(cls, value):
        """Valida se frame_seconds_index é um número positivo.
        """
        if value < 0:
            raise ValueError('frame_seconds_index cannot be negative')
        return value
    
    @validator('op_type')
    def validate_op_type(cls, value):
        """Valida se op_type é uma operação valida.
        """
        valid_operations = ['noise', 'random_rotation', 'flip', 'grayscale']
        message_operations = value.split('|')
        for operation in message_operations:
            if operation not in valid_operations:
                raise ValueError(f'{operation} is invalid.')
        return value

class Consumer:
    """Consome as mensagens da fila e manda as mensagens para o extrator.
    """
    def __init__(self, queue_name, rabbitmq_host="localhost"):
        self.rabbitmq_host = rabbitmq_host
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_host))
        self.channel = self.connection.channel()
        self.id = 1

    def send_data_to_extractor(self, message_data, ope_start_time):
        """Envia a mensagem para o extrator.

        Args:
            message_data (dict): A mensagem da fila.
            ope_start_time (float): Tempo inicial da operação.
        """
        extrator = Extractor(message_data, ope_start_time)
        extrator.extract_frame_and_process(id=self.id)
        self.id += 1 

    def consume(self):
        """Consome as mensagens da fila do RabbitMQ.
        """
        self.channel.queue_declare(queue=self.queue_name)
        def callback(ch, method, _, body):
            ope_start_time = datetime.utcnow().timestamp()
            message = json.loads(body)
            try:
                BaseMessage.parse_obj(message)
                self.send_data_to_extractor(message, ope_start_time)
            except ValueError:
                send_data_to_Register_API(self.id, "Error", "None", ope_start_time)
                self.id += 1 
            except ConnectionError as err:
                print(err)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)

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
