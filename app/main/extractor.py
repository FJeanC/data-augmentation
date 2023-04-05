import subprocess
from frame_operator import FrameOperator
import cv2
from senders.send_data_to_Register_API import send_data_to_Register_API
import os

class Extractor:
    """Extrai o frame especificado na mensagem e envia o frame para o operador de frames.
    """
    def __init__(self, messages, time):
        self.message = messages
        self.ope_start_time = time
    def extract_frame(self, video_path, frame_seconds_index):
        """Extrai o frame do vídeo

        Args:
            video_path (str): caminho do arquivo de vídeo.
            frame_seconds_index (int): índice do frame em segundos.

        Returns:
            numpy.ndarray: array numpy com o frame extraído.
        """
        video = cv2.VideoCapture(video_path)
        FPS = video.get(cv2.CAP_PROP_FPS)
        frame_index = int(FPS * (frame_seconds_index))
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        
        ret, frame = video.read()
        if not ret: # Tempo do frame_seconds_index é maior que o tempo total do vídeo
            last_key_frame = self.find_last_key_frame(video_path)
            video.set(cv2.CAP_PROP_POS_MSEC, last_key_frame)

            ret, frame = video.read()
            if not ret: # Erro caso o arquivo esteja corrompido ou arquivo não seja suportado
                send_data_to_Register_API(id, "Error", "None", self.ope_start_time)
                return
        video.release()
        return frame


    def extract_frame_and_process(self, id):
        """Extrai o frame do vídeo e envia para o operador.

        Args:
            id (int): Índice de operação do frame.
        """
        video_ref = self.message['video_ref']
        frame_seconds_index = self.message['frame_seconds_index']
        op_type = self.message['op_type']
        
        video_path =  f'../data/videos/{video_ref}'
        if not os.path.exists(video_path):
            send_data_to_Register_API(id, "Error", "None", self.ope_start_time)
            return
        
        frame = self.extract_frame(video_path, frame_seconds_index)
        self.send_data_to_operator(frame, op_type, id)
    
    def send_data_to_operator(self, frame, op_type, id):
        """Envia o frame para o operador de imagens.

        Args:
            frame (numpy.ndarray): A imagem a ser operada.
            op_type (string): Operações que deverão ser realizadas na imagem.
            id (int): Índice de operação do frame.
        """
        print("Processing!", id)
        operator = FrameOperator(frame, op_type, id, self.ope_start_time)
        operator.apply_operations_to_frame()

    def find_last_key_frame(self, video_path):
        """Encontra o último key frame do vídeo.

        Args:
            video_path (string): Path da localização do vídeo.

        Returns:
            int: Último key frame do vídeo.
        """
        ffprobe_command = f'ffprobe -loglevel error -select_streams v:0 -show_entries packet=pts_time,flags -of csv=print_section=0 {video_path}'
        awk_command = "awk -F',' '/K/ {print $1}'"
        key_frame_list = subprocess.check_output(f'{ffprobe_command} | {awk_command}', shell=True, text=True)
        return int(key_frame_list.split('\n')[-2][:-3].replace('.', ''))

