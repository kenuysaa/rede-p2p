import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SHARED_FOLDER = BASE_DIR.parent / "shared"

TRACKER_HOST = "10.80.9.224"
TRACKER_PORT = int(os.getenv("TRACKER_PORT", "5001"))

PEER_PORT = int(os.getenv("PEER_PORT", "5002"))
BUFFER_SIZE = int(os.getenv("CLIENT_BUFFER_SIZE", "4096"))

AUTHOR = os.getenv("AUTHOR", "Aluno")
DISCIPLINE = os.getenv("DISCIPLINE", "SISTEMAS_DISTRIBUIDOS")
