# Data Augmentation  

Sistema desenvolvido em Python que faz operações de Data Augmentation.  


O sistema recebe e gerencia mensagens utilizando o RabbitMQ, extrai a imagem do vídeo no tempo especificado na mensagem,faz as operações necessárias na imagem e registra localmente as operações feitas.
## Arquitetura do Sistema
![image](https://user-images.githubusercontent.com/84576267/226353370-037f4a3b-b611-41ed-8871-80fb9fd7961e.png)

## Requisitos

- Python - Versão Utilizada: 3.10.64
- [pip](https://pip.pypa.io/en/stable/)
- [SQLite3](https://www.sqlite.org/index.html)
- [FastAPI](https://fastapi.tiangolo.com/)
- [pika](https://pika.readthedocs.io/en/stable/index.html#)
- [Docker](https://www.docker.com/)
- [OpenCV](https://opencv.org/)

## Instalação
Baixar [Docker](https://www.docker.com/).  

FastAPI:
```bash
pip install "fastapi[all]"
```
pika:
```bash
pip install pika
```
OpenCV
```bash
pip install opencv-python
```
Para baixar o projeto, digite no terminal:
```bash
git clone https://github.com/FJeanC/data-augmentation
```
## Rodando o código
1. No terminal, rode o seguinte comando para executar o RabbitMQ:
```bash
docker run -p 15672:15672 -p 5672:5672 rabbitmq:3.9.9-management-alpine
```

2. Em outro terminal, navegue a para a pasta `/api` e rode o seguinte comando:
```bash
uvicorn registers:app --reload
```
3. Em outro terminal, navegue para a pasta `/main` e rode o seguinte comando:
```bash
python3 enqueue.py
```
4. Em seguida, na mesma pasta, rode o seguinte comando:
```bash
python3 consumer.py
```
5. Para rodar os testes, navegue para a pasta `/api` e rode o seguinte comando:
```bash
pytest
```
