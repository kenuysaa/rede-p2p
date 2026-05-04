import socket
from pathlib import Path
from tracker_client import send_request
from utils import get_file_hash
from config import SHARED_FOLDER, TRACKER_HOST, TRACKER_PORT, PEER_PORT, AUTHOR, DISCIPLINE

def get_local_ip():
    """Tenta descobrir o IP real da máquina na rede local."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def ensure_shared_folder():
    """Garante que a pasta 'shared' existe para evitar erros."""
    if not SHARED_FOLDER.exists():
        SHARED_FOLDER.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Pasta '{SHARED_FOLDER}' criada.")

def register():
    ensure_shared_folder()
    files = []

    for entry in SHARED_FOLDER.iterdir():
        if entry.is_file():
            file_hash = get_file_hash(entry)
            if file_hash:
                files.append({
                    "name": entry.name,
                    "discipline": DISCIPLINE,
                    "author": AUTHOR,
                    "type": entry.suffix.lstrip("."),
                    "hash": file_hash
                })

    if not files:
        print("Nenhum arquivo encontrado. Adicione arquivos à pasta 'shared' e tente novamente.")
        return

    request = {
        "type": "REGISTER",
        "ip": get_local_ip(),
        "port": PEER_PORT,
        "files": files
    }

    response = send_request(request, host=TRACKER_HOST, port=TRACKER_PORT)
    if response and response.get("status") == "OK":
        print(f"[REGISTER] {len(files)} arquivos registrados com sucesso!")
    else:
        print(f"[REGISTER] Erro no registro: {response}")

def list_files():
    request = {"type": "LIST"}
    response = send_request(request, host=TRACKER_HOST, port=TRACKER_PORT)

    print("\n[ARQUIVOS DISPONÍVEIS]")

    if response and "files" in response and response["files"]:
        for f in response["files"]:
            print(f"- {f['name']} ({f['discipline']}) | Autor: {f['author']} | Hash: {f['hash']}")
    else:
        print("Nenhum arquivo encontrado no Tracker.")

def lookup():
    file_hash = input("Digite o hash do arquivo: ").strip()

    if not file_hash:
        print("Hash inválido. Tente novamente.")
        return

    request = {
        "type": "LOOKUP",
        "hash": file_hash
    }

    response = send_request(request, host=TRACKER_HOST, port=TRACKER_PORT)

    print("\n[PEERS DISPONÍVEIS]")

    if response and "peers" in response:
        for p in response["peers"]:
            print(f"-> {p['ip']}:{p['port']} | Score de Reputação: {p['score']:.4f}")
    else:
        error_msg = response.get("error", "Erro desconhecido") if response else "Sem resposta do Tracker"
        print(f"Nenhum peer encontrado. Detalhe: {error_msg}")

def print_menu():
    print("\nREDE P2P ACADÊMICA")
    print(f"Tracker Alvo: {TRACKER_HOST}:{TRACKER_PORT}")
    print("1 - Registrar/Atualizar meus arquivos no Tracker")
    print("2 - Listar todos os arquivos da rede")
    print("3 - Buscar peers que possuem um arquivo (por Hash)")
    print("0 - Sair")

def main():
    print("Iniciando Cliente P2P...")
    ensure_shared_folder()

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
            print("Encerrando...")
            break
        else:
            print("Opção inválida. Escolha uma opção do menu.")

if __name__ == "__main__":
    main()
