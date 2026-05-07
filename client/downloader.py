import socket
import json
from config import BUFFER_SIZE, SHARED_FOLDER

def download_file_from_peer(peer_ip, peer_port, file_hash, filename):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect((peer_ip, peer_port))

        # Envia o pedido do arquivo
        request = {"hash": file_hash, "filename": filename}
        client.sendall(json.dumps(request).encode())

        # Prepara o caminho de salvamento
        save_path = SHARED_FOLDER / f"downloaded_{filename}"

        with open(save_path, "wb") as f:
            while True:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
        
        return True, f"Sucesso! Salvo em: {save_path.name}"
    except Exception as e:
        return False, f"Erro no download: {e}"
    