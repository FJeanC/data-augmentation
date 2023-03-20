import cv2
from random import randint
import numpy as np
import os
from send_data_to_Register_API import send_data_to_Register_API

class FrameOperator:
    """Realiza as operações descritas na mensagem e salva a imagem localmente.
    """
    def __init__(self, frame, op_type = "", id = 1, time = "00:00:00"):
        self.frame = frame
        self.op_type = op_type
        self.orginal_frame = frame
        self.id = id
        self.ope_start_time = time

    def grayscale(self):
        """Converte o frame para a escala de cinza.

        Returns:
            numpy.ndarray: O frame na escala de cinza.
        """
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return gray_frame

    def flip(self):
        """Espelha o frame.

        Returns:
            numpy.ndarray: O frame espelhado.
        """
        flipped_frame = cv2.flip(self.frame, 1)
        return flipped_frame

    def random_rotation(self):
        """Rotaciona o frame em um ângulo aleatório entre 0° e 180°.

        Returns:
            numpy.ndarray: O frame rotacionado.
        """
        (height, width) = self.frame.shape[:2]
        center = (width // 2, height // 2)
        angle = randint(0, 180)

        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_frame = cv2.warpAffine(self.frame, matrix, (width, height))

        return rotated_frame

    def noise(self):
        """Adiciona ruído no frame.

        Returns:
            numpy.ndarray: O frame com ruído.
        """
        noise = np.zeros(self.frame.shape, dtype=np.uint8)
        cv2.randn(noise, (0,), (60,))

        noisy_frame = cv2.add(self.frame, noise)
        return noisy_frame

    def apply_operations_to_frame(self):
        """Seleciona qual operação deve ser realizada no frame.
        """
        for operation in self.op_type.split('|'):
            if operation == 'flip':
                self.frame = self.flip()
            elif operation == 'grayscale':
                self.frame = self.grayscale()
            elif operation == 'noise':
                self.frame = self.noise()
            elif operation == 'random_rotation':
                self.frame = self.random_rotation()
        self.save_image()

    def save_image(self):
        """Salva o frame localmente como imagem .png.
        """
        self.folders_exists()
        frames_path = f'../data/frames/id_{self.id}.png'
        processed_path = f'../data/processed_frames/id_{self.id}.png'
        cv2.imwrite(processed_path, self.frame)
        cv2.imwrite(frames_path, self.orginal_frame)
        send_data_to_Register_API(self.id, "Success", self.op_type, self.ope_start_time)
        
    def folders_exists(self):
        """Valida as existências das pastas /frames e /processed_frames.
        """
        if not os.path.exists('../data/frames'):
            os.makedirs('../data/frames')
        if not os.path.exists('../data/processed_frames'):
            os.makedirs('../data/processed_frames')
