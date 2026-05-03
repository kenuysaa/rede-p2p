import socket
from tracker_client import send_request
from utils import get_file_hash
from config import SHARED_FOLDER, TRACKER_HOST, TRACKER_PORT, PEER_PORT, AUTHOR, DISCIPLINE


def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def register():
    if not SHARED_FOLDER.exists():
        print(f"[ERRO] Pasta compartilhada não encontrada: {SHARED_FOLDER}")
        return

    files = []

    for entry in SHARED_FOLDER.iterdir():
        if entry.is_file():
            file_hash = get_file_hash(entry)
            files.append({
                "name": entry.name,
                "discipline": DISCIPLINE,
                "author": AUTHOR,
                "type": entry.suffix.lstrip("."),
                "hash": file_hash
            })

    if not files:
        print("Nenhum arquivo encontrado em shared/. Adicione arquivos à pasta shared e tente novamente.")
        return

    request = {
        "type": "REGISTER",
        "ip": get_local_ip(),
        "port": PEER_PORT,
        "files": files
    }

    response = send_request(request, host=TRACKER_HOST, port=TRACKER_PORT)
    print("[REGISTER]", response)


def list_files():
    request = {"type": "LIST"}
    response = send_request(request, host=TRACKER_HOST, port=TRACKER_PORT)

    print("\n[ARQUIVOS DISPONÍVEIS]")

    if response and "files" in response:
        for f in response["files"]:
            print(f"- {f['name']} ({f['discipline']}) | hash={f['hash']}")
    else:
        print("Nenhum arquivo encontrado")


def lookup():
    file_hash = input("Digite o hash do arquivo: ")

    if not file_hash.strip():
        print("Hash inválido. Tente novamente.")
        return

    request = {
        "type": "LOOKUP",
        "hash": file_hash.strip()
    }

    response = send_request(request, host=TRACKER_HOST, port=TRACKER_PORT)

    print("\n[PEERS DISPONÍVEIS]")

    if response and "peers" in response:
        for p in response["peers"]:
            print(f"{p['ip']}:{p['port']} | score={p['score']:.2f}")
    else:
        print("Nenhum peer encontrado")


def print_menu():
    print("\n--- REDE P2P SIMPLES ---")
    print(f"Tracker: {TRACKER_HOST}:{TRACKER_PORT}")
    print("1 - Registrar arquivos no tracker")
    print("2 - Listar arquivos disponíveis")
    print("3 - Buscar peers por hash")
    print("0 - Sair")


def main():
    print("Rede P2P simples para trabalho acadêmico de Sistemas Distribuídos")
    print(f"Pasta compartilhada: {SHARED_FOLDER}")

    while True:
        print_menu()
        op = input(">> ").strip()

        if op == "1":
            register()
        elif op == "2":
            list_files()
        elif op == "3":
            lookup()
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Digite 0, 1, 2 ou 3.")


if __name__ == "__main__":
    main()
