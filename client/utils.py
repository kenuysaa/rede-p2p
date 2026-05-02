import hashlib

def get_file_hash(filepath):
    hasher = hashlib.md5()

    with open(filepath, "rb") as f:
        hasher.update(f.read())

    return hasher.hexdigest()
