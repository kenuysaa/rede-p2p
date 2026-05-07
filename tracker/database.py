import time
import math
import threading
from config import DECAY_LAMBDA

files = {}
peers = {}
db_lock = threading.Lock() # Trava para garantir Thread-Safety

def register_peer(ip, port):
    peer_id = f"{ip}:{port}"
    with db_lock:
        if peer_id not in peers:
            peers[peer_id] = {
                "score": 0.0,
                "last_update": time.time()
            }
    return peer_id

def update_reputation_unsafe(peer_id, value):
    """Função interna sem lock, deve ser chamada dentro de um bloco 'with db_lock'"""
    now = time.time()
    last = peers[peer_id]["last_update"]
    old_score = peers[peer_id]["score"]

    decayed_score = old_score * math.exp(-DECAY_LAMBDA * (now - last))
    new_score = decayed_score + value

    peers[peer_id]["score"] = new_score
    peers[peer_id]["last_update"] = now

def add_file(file_hash, metadata, peer_id):
    with db_lock:
        if file_hash not in files:
            files[file_hash] = {
                "metadata": metadata,
                "peers": []
            }

        if peer_id not in files[file_hash]["peers"]:
            files[file_hash]["peers"].append(peer_id)
            update_reputation_unsafe(peer_id, 1) # Adiciona crédito por compartilhar

def get_all_files():
    result = []
    with db_lock:
        for file_hash, data in files.items():
            entry = data["metadata"].copy()
            entry["hash"] = file_hash
            result.append(entry)
    return result

def get_ranked_peers(file_hash):
    ranked = []
    with db_lock:
        if file_hash not in files:
            return []

        now = time.time()
        for peer_id in files[file_hash]["peers"]:
            peer = peers.get(peer_id)
            if not peer:
                continue

            # Calcula score simulado em tempo real para ordenação
            score = peer["score"] * math.exp(-DECAY_LAMBDA * (now - peer["last_update"]))

            ip, port = peer_id.split(":")
            ranked.append({
                "ip": ip,
                "port": int(port),
                "score": score
            })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked
