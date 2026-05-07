import socket
import threading
from pathlib import Path
from tracker_client import send_request
from utils import get_file_hash
from peer_server import start_peer_server
from downloader import download_file_from_peer
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

    print("\n[ARQUIVOS DISPONÍVEIS NA REDE]")
    if response and "files" in response and response["files"]:
        for f in response["files"]:
            print(f"- {f['name']} ({f['discipline']}) | Autor: {f['author']} | Hash: {f['hash']}")
    else:
        print("Nenhum arquivo encontrado no Tracker.")

def lookup():
    file_hash = input("Digite o hash do arquivo: ").strip()

    if not file_hash:
        print("Hash inválido.")
        return

    request = {"type": "LOOKUP", "hash": file_hash}
    response = send_request(request, host=TRACKER_HOST, port=TRACKER_PORT)

    print("\n[PEERS QUE POSSUEM O ARQUIVO]")
    if response and "peers" in response:
        for p in response["peers"]:
            print(f"-> {p['ip']}:{p['port']} | Reputação: {p['score']:.4f}")
    else:
        print("Nenhum peer encontrado para este hash.")

def print_menu():
    print("\n" + "="*30)
    print("      REDE P2P ACADÊMICA")
    print("="*30)
    print(f"Tracker: {TRACKER_HOST}:{TRACKER_PORT}")
    print(f"Meu IP: {get_local_ip()} | Porta de Upload: {PEER_PORT}")
    print("-" * 30)
    print("1 - Registrar meus arquivos")
    print("2 - Listar todos os arquivos")
    print("3 - Buscar por Hash (Ver reputação)")
    print("4 - Baixar arquivo de um Peer (Download)")
    print("0 - Sair")
    print("-" * 30)

def main():
    ensure_shared_folder()
    
    # Inicia o servidor de upload (Peer Server) em uma thread separada
    print("[INFO] Iniciando servidor de upload em background...")
    threading.Thread(target=start_peer_server, daemon=True).start()

    while True:
        print_menu()
        op = input("Escolha uma opção >> ").strip()

        if op == "1":
            register()
        elif op == "2":
            list_files()
        elif op == "3":
            lookup()
        elif op == "4":
            print("\n[DOWNLOAD]")
            target_ip = input("IP do Peer: ").strip()
            target_hash = input("Hash do arquivo: ").strip()
            fname = input("Nome exato do arquivo (ex: aula.pdf): ").strip()
            
            # Usa PEER_PORT para garantir consistência com o servidor do outro peer
            sucesso, msg = download_file_from_peer(target_ip, PEER_PORT, target_hash, fname)
            print(f"\n[DOWNLOAD STATUS] {msg}")
        elif op == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
