import socket
import threading
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from config import (
    AUTHOR,
    DISCIPLINE,
    PEER_PORT,
    SHARED_FOLDER,
    TRACKER_HOST,
    TRACKER_PORT,
)
from downloader import download_file_from_peer
from peer_server import start_peer_server
from tracker_client import send_request
from utils import get_file_hash

app = Flask(__name__)

peer_server_started = False
peer_server_lock = threading.Lock()


def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_socket.connect(("8.8.8.8", 80))
            return client_socket.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def ensure_shared_folder():
    if not SHARED_FOLDER.exists():
        SHARED_FOLDER.mkdir(parents=True, exist_ok=True)


def list_local_files():
    ensure_shared_folder()
    files = []
    for entry in SHARED_FOLDER.iterdir():
        if entry.is_file():
            file_hash = get_file_hash(entry)
            if file_hash:
                files.append(
                    {
                        "name": entry.name,
                        "discipline": DISCIPLINE,
                        "author": AUTHOR,
                        "type": entry.suffix.lstrip("."),
                        "hash": file_hash,
                    }
                )
    return files


def ensure_peer_server():
    global peer_server_started
    with peer_server_lock:
        if peer_server_started:
            return
        thread = threading.Thread(target=start_peer_server_safe, daemon=True)
        thread.start()
        peer_server_started = True


def start_peer_server_safe():
    try:
        start_peer_server()
    except OSError as error:
        # Evita quebrar quando a porta ja estiver ocupada por outra instancia.
        print(f"[PEER SERVER] Nao iniciado: {error}")


@app.route("/")
def index():
    ensure_peer_server()
    ensure_shared_folder()
    return render_template(
        "index.html",
        tracker_host=TRACKER_HOST,
        tracker_port=TRACKER_PORT,
        peer_port=PEER_PORT,
        author=AUTHOR,
        discipline=DISCIPLINE,
    )


@app.get("/api/status")
def status():
    return jsonify(
        {
            "tracker": f"{TRACKER_HOST}:{TRACKER_PORT}",
            "peer_port": PEER_PORT,
            "my_ip": get_local_ip(),
            "author": AUTHOR,
            "discipline": DISCIPLINE,
        }
    )


@app.post("/api/register")
def register_files():
    ensure_peer_server()
    files = list_local_files()
    if not files:
        return jsonify({"ok": False, "message": "Nenhum arquivo encontrado na pasta shared."}), 400

    payload = {"type": "REGISTER", "ip": get_local_ip(), "port": PEER_PORT, "files": files}
    response = send_request(payload, host=TRACKER_HOST, port=TRACKER_PORT)

    if response and response.get("status") == "OK":
        return jsonify({"ok": True, "message": f"{len(files)} arquivos registrados com sucesso.", "files": files})
    return jsonify({"ok": False, "message": "Falha ao registrar no tracker.", "tracker_response": response}), 502


@app.get("/api/files")
def network_files():
    response = send_request({"type": "LIST"}, host=TRACKER_HOST, port=TRACKER_PORT)
    if response and "files" in response:
        return jsonify({"ok": True, "files": response["files"]})
    return jsonify({"ok": False, "files": [], "message": "Nao foi possivel listar os arquivos."}), 502


@app.get("/api/lookup/<file_hash>")
def lookup(file_hash):
    response = send_request({"type": "LOOKUP", "hash": file_hash}, host=TRACKER_HOST, port=TRACKER_PORT)
    if response and "peers" in response:
        return jsonify({"ok": True, "peers": response["peers"]})
    return jsonify({"ok": False, "peers": [], "message": "Nenhum peer encontrado para esse hash."}), 404


@app.post("/api/download")
def download():
    data = request.get_json(silent=True) or {}
    peer_ip = data.get("peer_ip", "").strip()
    file_hash = data.get("file_hash", "").strip()
    filename = data.get("filename", "").strip()
    peer_port = int(data.get("peer_port", PEER_PORT))

    if not peer_ip or not file_hash or not filename:
        return jsonify({"ok": False, "message": "peer_ip, file_hash e filename sao obrigatorios."}), 400

    ok, message = download_file_from_peer(peer_ip, peer_port, file_hash, filename)
    status_code = 200 if ok else 502
    return jsonify({"ok": ok, "message": message, "saved_in": str(Path(SHARED_FOLDER))}), status_code


if __name__ == "__main__":
    ensure_shared_folder()
    ensure_peer_server()
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=False)
