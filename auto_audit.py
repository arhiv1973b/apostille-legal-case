import hashlib
import os

def get_hash(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

print("🔍 Запуск аудита целостности данных...")
files = [f for f in os.listdir('KNOWLEDGE_BASE') if f.endswith('.md')]
for f in files:
    print(f"File: {f} | SHA-256: {get_hash('KNOWLEDGE_BASE/'+f)}")
