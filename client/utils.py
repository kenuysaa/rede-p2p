import hashlib

def get_file_hash(filepath):
    # Gera o hash md5 em blocos para não estourar a RAM com arquivos pesados
    hasher = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            # Lê o arquivo em blocos de 4KB
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"[ERRO] Não foi possível ler o arquivo {filepath}: {e}")
        return None
