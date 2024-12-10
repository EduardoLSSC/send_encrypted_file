import socket
import hashlib
from cryptography.fernet import Fernet

def send_encrypted_file(client_socket):
    filepath = 'exemplo.txt'
    file_hash = calculate_file_hash(filepath)
    print(f"Hash do arquivo antes da criptografia: {file_hash}")
    encrypted_message = encrypt(filepath)
    client_socket.send(file_hash.encode())
    client_socket.send(b'\n')
    client_socket.send(encrypted_message)
    print("Arquivo criptografado e hash enviados com sucesso!")

def calculate_file_hash(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def encrypt(filepath):
    with open('chave.key', 'rb') as filekey:
        chave = filekey.read()
    fernet = Fernet(chave)
    with open(filepath, 'rb') as arquivo:
        conteudo = arquivo.read()
    criptografado = fernet.encrypt(conteudo)
    return criptografado

def client():
    host = '192.168.0.144'
    port = 65432
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    send_encrypted_file(client_socket)
    client_socket.close()

if __name__ == "__main__":
    client()
