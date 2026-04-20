import socket
import json

HOST = "127.0.0.1"
PORT = 5000

def send_request(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.send(json.dumps(request).encode())

    response = s.recv(4096).decode()
    print("Resposta:", response)

    s.close()

# TESTE 1: Registrar peer
send_request({
    "type": "REGISTER",
    "ip": "127.0.0.1",
    "port": 5001,
    "files": [
        {"name": "file1.txt", "hash": "abc123"},
        {"name": "file2.txt", "hash": "def456"}
    ]
})

# TESTE 2: Listar arquivos
send_request({
    "type": "LIST"
})

# TESTE 3: Buscar arquivo
send_request({
    "type": "LOOKUP",
    "name": "file1.txt"
})
