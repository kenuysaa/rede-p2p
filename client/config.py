import os
from pathlib import Path

# Caminho da pasta que deve conter os arquivos compartilhados pelo peer.
BASE_DIR = Path(__file__).resolve().parent
SHARED_FOLDER = BASE_DIR.parent / "shared"

# Configurações do tracker que o cliente deve contatar.
TRACKER_HOST = os.getenv("TRACKER_HOST", "127.0.0.1")
TRACKER_PORT = int(os.getenv("TRACKER_PORT", "5001"))

# Porta local do peer. Se for implementado o servidor de arquivos peer-to-peer,
# esta é a porta em que este peer estará disponível.
PEER_PORT = int(os.getenv("PEER_PORT", "5002"))

# Buffer de rede usado para receber dados TCP.
BUFFER_SIZE = int(os.getenv("CLIENT_BUFFER_SIZE", "4096"))

# Metadados fixos do projeto acadêmico.
AUTHOR = os.getenv("AUTHOR", "Guilherme")
DISCIPLINE = os.getenv("DISCIPLINE", "REDES")
