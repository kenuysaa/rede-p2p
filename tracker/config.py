import os

HOST = os.getenv("TRACKER_HOST", "0.0.0.0")
PORT = int(os.getenv("TRACKER_PORT", "5001"))
BACKLOG = int(os.getenv("TRACKER_BACKLOG", "100")) # Aumentado para suportar mais peers
BUFFER_SIZE = int(os.getenv("TRACKER_BUFFER_SIZE", "4096"))
DECAY_LAMBDA = float(os.getenv("DECAY_LAMBDA", "0.0001"))
