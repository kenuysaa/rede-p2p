import os

# Endereço e porta em que o tracker deve escutar.
HOST = os.getenv("TRACKER_HOST", "0.0.0.0")
PORT = int(os.getenv("TRACKER_PORT", "5001"))

# Número máximo de conexões pendentes na fila do socket.
BACKLOG = int(os.getenv("TRACKER_BACKLOG", "5"))

# Tamanho padrão de buffer para receber mensagens do cliente.
BUFFER_SIZE = int(os.getenv("TRACKER_BUFFER_SIZE", "4096"))
