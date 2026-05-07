from database import register_peer, add_file, get_all_files, get_ranked_peers

def handle_register(request):
    ip = request.get("ip")
    port = request.get("port")

    if not ip or not port:
        return {"error": "IP e Porta são obrigatórios"}

    peer_id = register_peer(ip, port)

    for file in request.get("files", []):
        metadata = {
            "name": file.get("name"),
            "discipline": file.get("discipline"),
            "author": file.get("author"),
            "type": file.get("type")
        }
        add_file(file.get("hash"), metadata, peer_id)

    return {"status": "OK"}

def handle_list(request=None):
    return {
        "files": get_all_files()
    }

def handle_lookup(request):
    file_hash = request.get("hash")
    if not file_hash:
        return {"error": "Hash do arquivo é obrigatório"}

    peers = get_ranked_peers(file_hash)

    if peers:
        return {
            "peers": peers
        }

    return {"error": "Arquivo não encontrado ou sem peers disponíveis"}
