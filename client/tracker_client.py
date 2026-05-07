import socket
import json
from config import TRACKER_HOST, TRACKER_PORT, BUFFER_SIZE

def send_request(request, host=TRACKER_HOST, port=TRACKER_PORT):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0) # Previne congelamento se o Tracker não responder
            s.connect((host, port))
            s.send(json.dumps(request).encode('utf-8'))
            response = s.recv(BUFFER_SIZE).decode('utf-8')

        return json.loads(response)

    except socket.timeout:
        print("[ERRO] Tempo de conexão com o Tracker esgotado.")
        return None
    except ConnectionRefusedError:
        print("[ERRO] Conexão recusada. O Tracker está rodando?")
        return None
    except Exception as e:
        print(f"[ERRO] Falha na comunicação: {e}")
        return None
