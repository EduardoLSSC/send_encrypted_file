import socket
import hashlib
from cryptography.fernet import Fernet
from colorama import init, Fore, Style

def send_encrypted_file(client_socket):
    filepath = 'exemplo.txt'
    file_hash = calculate_file_hash(filepath)
    print(f"Hash do arquivo antes da criptografia:" + Fore.RED + f" {file_hash}")
    encrypted_message = encrypt(filepath)
    client_socket.send(file_hash.encode())
    client_socket.send(b'\n')
    client_socket.send(encrypted_message)
    print(Fore.GREEN + Style.BRIGHT + "Arquivo criptografado e hash enviados com sucesso!")

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
    print(f"A mensagem envidada pelo cliente é"+ Fore.CYAN + f" {conteudo}")
    return criptografado

def client():
    host = 'COLOCA O IP AQUI'
    port = 65432
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    send_encrypted_file(client_socket)
    client_socket.close()

if __name__ == "__main__":
    init(autoreset = True)
    client()
