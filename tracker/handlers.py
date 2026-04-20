# trata os comandos recebidos

from database import add_peer, get_all_files, get_peers_by_name

def handle_register(request):
    peer_ip = request["ip"]
    peer_port = request["port"]

    for file in request["files"]:
        file_hash = file["hash"]
        file_name = file["name"]

        peer = {
            "ip": peer_ip,
            "port": peer_port
        }

        add_peer(file_hash, file_name, peer)

    return {"status": "OK"}


def handle_list():
    return {
        "files": get_all_files()
    }


def handle_lookup(request):
    file_name = request["name"]

    file_hash, peers = get_peers_by_name(file_name)

    if file_hash:
        return {
            "hash": file_hash,
            "peers": peers
        }

    return {"error": "Arquivo não encontrado"}
