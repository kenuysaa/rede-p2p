# armazenar os metadados dos arquivos
files = {}

def add_peer(file_hash, file_name, peer):
    if file_hash not in files:
        files[file_hash] = {
            "name": file_name,
            "peers": []
        }

    if peer not in files[file_hash]["peers"]:
        files[file_hash]["peers"].append(peer)


def get_all_files():
    return [
        {"name": data["name"], "hash": file_hash}
        for file_hash, data in files.items()
    ]


def get_peers_by_name(file_name):
    for file_hash, data in files.items():
        if data["name"] == file_name:
            return file_hash, data["peers"]

    return None, None
