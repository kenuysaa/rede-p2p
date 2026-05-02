# armazenar os metadados dos arquivos
import time
import math

files = {}
peers = {}

DECAY_LAMBDA = 0.0001  # controla velocidade do decaimento

def register_peer(ip, port):
    peer_id = f"{ip}:{port}"

    if peer_id not in peers:
        peers[peer_id] = {
            "score": 0,
            "last_update": time.time()
        }
    return peer_id

def update_reputation(peer_id, value):
    now = time.time()
    last = peers[peer_id]["last_update"]
    old_score = peers[peer_id]["score"]
    decayed_score = old_score * math.exp(-DECAY_LAMBDA * (now - last))

    new_score = decayed_score + value

    peers[peer_id]["score"] = new_score
    peers[peer_id]["last_update"] = now

def add_file(file_hash, metadata, peer_id):
    if file_hash not in files:
        files[file_hash] = {
            "metadata": metadata,
            "peers": []
        }

    if peer_id not in files[file_hash]["peers"]:
        files[file_hash]["peers"].append(peer_id)
        update_reputation(peer_id, 1)

def get_all_files():
    result = []

    for file_hash, data, in files.items():
        entry = data["metadata"].copy()
        entry["hash"] = file_hash
        result.append(entry)

    return result

def get_ranked_peers(file_hash):
    if file_hash not in files:
        return []

    ranked = []

    for peer_id in files[file_hash]["peers"]:
        peer = peers[peer_id]

        now = time.time()
        score = peer["score"] * math.exp(-DECAY_LAMBDA * (now - peer["last_update"]))

        ip, port = peer_id.split(":")
        ranked.append({
            "ip": ip,
            "port": int(port),
            "score": score
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked
