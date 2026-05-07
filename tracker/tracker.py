import socket
import json
import threading
from handlers import handle_register, handle_list, handle_lookup
from config import HOST, PORT, BACKLOG, BUFFER_SIZE

def handle_client(conn, addr):
    # Lida com a requisição de um cliente específico em uma Thread separada
    try:
        data = conn.recv(BUFFER_SIZE).decode('utf-8')
        if not data:
            return

        request = json.loads(data)
        print(f"[REQUEST] {addr} -> {request.get('type')}")

        command_type = request.get("type")

        if command_type == "REGISTER":
            response = handle_register(request)
        elif command_type == "LIST":
            response = handle_list(request)
        elif command_type == "LOOKUP":
            response = handle_lookup(request)
        else:
            response = {"error": "Comando inválido"}

        conn.send(json.dumps(response).encode('utf-8'))

    except json.JSONDecodeError:
        error_msg = json.dumps({"error": "Formato JSON inválido"}).encode('utf-8')
        conn.send(error_msg)
    except Exception as e:
        print(f"[ERRO] Falha ao processar cliente {addr}: {e}")
        error_msg = json.dumps({"error": "Erro interno no servidor"}).encode('utf-8')
        try:
            conn.send(error_msg)
        except:
            pass
    finally:
        conn.close()

def start_tracker():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(BACKLOG)

    print(f"[TRACKER] Rodando em {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server.accept()
            # Inicia uma nova thread para cada conexão, evitando que o Tracker trave
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[TRACKER] Encerrando servidor...")
    finally:
        server.close()

if __name__ == "__main__":
    start_tracker()
