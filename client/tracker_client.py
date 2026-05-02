import socket
import json

TRACKER_HOST = "127.0.0.1"
TRACKER_PORT = 5000

def send_request(request):
    try: # comunicacao TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TRACKER_HOST, TRACKER_PORT))

        s.send(json.dumps(request).encode())

        response = s.recv(4096).decode()
        s.close()

        return json.loads(response)

    except Exception as e:
        print(f"[ERRO] {e}")
        return None
