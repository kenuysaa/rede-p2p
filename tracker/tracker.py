import socket 
import json
from handlers import handle_register, handle_list, handle_lookup
from config import HOST, PORT, BACKLOG, BUFFER_SIZE


def start_tracker():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(BACKLOG)

    print(f"[TRACKER] Rodando em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[CONEXÃO] Cliente conectado: {addr}")

        try:
            data = conn.recv(BUFFER_SIZE).decode()

            if not data:
                conn.close()
                continue

            request = json.loads(data)

            print(f"[REQUEST] {request}")

            # roteamento
            if request["type"] == "REGISTER":
                response = handle_register(request)

            elif request["type"] == "LIST":
                response = handle_list()

            elif request["type"] == "LOOKUP":
                response = handle_lookup(request)

            else:
                response = {"error": "Comando inválido"}

            conn.send(json.dumps(response).encode())

        except Exception as e:
            print(f"[ERRO] {e}")
            conn.send(json.dumps({"error": "Erro interno"}).encode())

        finally:
            conn.close()


if __name__ == "__main__":
    start_tracker()
