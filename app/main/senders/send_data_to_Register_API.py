import requests
import json

def send_data_to_Register_API(id, status, ope_type, ope_start_time):
    """Faz a chamada da API de Registros para salvar as operações e erros no banco de dados.

    Args:
        id (int): Índice de operação do frame.
        status (string): Indica se operação foi erro ou sucesso.
        ope_type (string): Operações que foram realizadas na imagem.
        ope_start_time (float):  Tempo inicial da operação.
    """
    url = "http://127.0.0.1:8000/register"
    data = {
            "id" : id,
            "status" : status,
            "ope_start_time" : ope_start_time,
            "operation_type": ope_type
        }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise ConnectionError("Http Error.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Connection Error")
    except requests.exceptions.Timeout:
        raise ConnectionError("Timeout Error")
    except requests.exceptions.RequestException:
        raise ConnectionError("Connection Error")
    
    if response.status_code == 200:
        print("Data sent to API")
        print(response.json())
    else:
        print("API fail")
        print(response.text)
