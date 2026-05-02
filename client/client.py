import os
from tracker_client import send_request
from utils import get_file_hash

PORT = 5001
SHARED_FOLDER = "../shared"

AUTHOR = "Guilherme"
DISCIPLINE = "REDES"

def register():
    files = []

    for filename in os.listdir(SHARED_FOLDER):
        filepath = os.path.join(SHARED_FOLDER, filename)

        if os.path.isfile(filepath):
            file_hash = get_file_hash(filepath)

            file_data = {
                "name": filename,
                "discipline": DISCIPLINE,
                "author": AUTHOR,
                "type": filename.split(".")[-1],
                "hash": file_hash
            }

            files.append(file_data)

    request = {
        "type": "REGISTER",
        "ip": "127.0.0.1",
        "port": PORT,
        "files": files
    }

    response = send_request(request)
    print("[REGISTER]", response)

def list_files():
    request = {"type": "LIST"}
    response = send_request(request)

    print("\n[ARQUIVOS DISPONÍVEIS]")

    if response and "files" in response:
        for f in response["files"]:
            print(f"- {f['name']} ({f['discipline']}) [{f['hash']}]")
    else:
        print("Nenhum arquivo encontrado")

def lookup():
    file_hash = input("Digite o hash do arquivo: ")

    request = {
        "type": "LOOKUP",
        "hash": file_hash
    }

    response = send_request(request)

    print("\n[PEERS DISPONÍVEIS]")

    if response and "peers" in response:
        for p in response["peers"]:
            print(f"{p['ip']}:{p['port']} | score={p['score']:.2f}")
    else:
        print("Nenhum peer encontrado")

def main():
    while True:
        print("\n1 - REGISTER")
        print("2 - LIST")
        print("3 - LOOKUP")
        print("0 - SAIR")

        op = input(">> ")

        if op == "1":
            register()
        elif op == "2":
            list_files()
        elif op == "3":
            lookup()
        elif op == "0":
            break


if __name__ == "__main__":
    main()
