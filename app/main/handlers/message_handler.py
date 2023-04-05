from pydantic import BaseModel, validator
from senders.send_data_to_Register_API import send_data_to_Register_API
from extractor import Extractor

class Operation:
    valid_operations = ['noise', 'random_rotation', 'flip', 'grayscale']


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
        message_operations = value.split('|')
        for operation in message_operations:
            if operation not in Operation.valid_operations:
                raise ValueError(f'{operation} is invalid.')
        return value



class Messagehandler:
    def __init__(self, message, ope_start_time, id, ch, method) -> None:
        self.message = message
        self.ope_time = ope_start_time
        self.id = id
        self.ch = ch
        self.method = method

    def handle_message(self):
        try:
            self.validate_message()
            self.process_message()
        except ValueError:
            self.handle_error()
        except ConnectionError as err:
            print(err)
            self.ch.basic_nack(delivery_tag=self.method.delivery_tag, requeue=True)
        else:
            self.ch.basic_ack(delivery_tag=self.method.delivery_tag)

    def validate_message(self):
        BaseMessage.parse_obj(self.message)

    def process_message(self):
        extrator = Extractor(self.message, self.ope_time)
        extrator.extract_frame_and_process(id=self.id)

    def handle_error(self):
        send_data_to_Register_API(self.id, "Error", "None", self.ope_time)
