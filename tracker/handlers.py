# trata os comandos recebidos
from database import register_peer, add_file, get_all_files, get_ranked_peers

def handle_register(request):
    ip = request["ip"]
    port = request["port"]

    peer_id = register_peer(ip, port)

    # metadatas
    for file in request["files"]:
        metadata = {
            "name": file["name"],
            "discipline": file["discipline"],
            "author": file["author"],
            "type": file["type"]
        }

        add_file(file["hash"], metadata, peer_id)

    return {"status": "OK"}

def handle_list():
    return {
        "files": get_all_files()
    }

def handle_lookup(request):
    file_hash = request["hash"]

    peers = get_ranked_peers(file_hash)

    if peers:
        return {
            "peers": peers
        }

    return {"error": "Arquivo não encontrado"}
