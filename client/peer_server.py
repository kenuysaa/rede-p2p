import socket
import threading
import json
from config import PEER_PORT, SHARED_FOLDER, BUFFER_SIZE

def handle_upload(client_socket):
    try:
        # Recebe o pedido (geralmente o Hash do arquivo)
        request_data = client_socket.recv(BUFFER_SIZE).decode()
        request = json.loads(request_data)
        file_hash = request.get("hash")

        # Procura o arquivo na pasta shared pelo nome ou hash
        # Aqui, para simplificar, vamos buscar pelo nome que o peer já conhece
        file_path = SHARED_FOLDER / request.get("filename")

        if file_path.exists():
            with open(file_path, "rb") as f:
                while (chunk := f.read(BUFFER_SIZE)):
                    client_socket.sendall(chunk)
            print(f"\n[UPLOAD] Arquivo {file_path.name} enviado com sucesso!")
    except Exception as e:
        print(f"[ERRO UPLOAD] {e}")
    finally:
        client_socket.close()

def start_peer_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PEER_PORT))
    server.listen(5)
    print(f"[PEER SERVER] Aguardando requisições de download na porta {PEER_PORT}...")

    while True:
        client_sock, addr = server.accept()
        thread = threading.Thread(target=handle_upload, args=(client_sock,))
        thread.start()