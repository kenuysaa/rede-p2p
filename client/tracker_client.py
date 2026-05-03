import socket
import json
from config import TRACKER_HOST, TRACKER_PORT, BUFFER_SIZE


def send_request(request, host=TRACKER_HOST, port=TRACKER_PORT):
    try:  # comunicacao TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send(json.dumps(request).encode())
            response = s.recv(BUFFER_SIZE).decode()

        return json.loads(response)

    except Exception as e:
        print(f"[ERRO] {e}")
        return None
