import os
import socket
import json

TRACKER_HOST = os.getenv("TRACKER_HOST", "127.0.0.1")
TRACKER_PORT = int(os.getenv("TRACKER_PORT", "5001"))


def send_request(request, host=TRACKER_HOST, port=TRACKER_PORT):
    try:  # comunicacao TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send(json.dumps(request).encode())
            response = s.recv(4096).decode()

        return json.loads(response)

    except Exception as e:
        print(f"[ERRO] {e}")
        return None
