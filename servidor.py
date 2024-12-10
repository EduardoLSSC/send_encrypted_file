import socket
from cryptography.fernet import Fernet
import hashlib

def decrypt_message(message, chave):
    fernet = Fernet(chave)
    descriptografado = fernet.decrypt(message)
    with open('arquivo_enviado_descriptografado.txt', 'wb') as arquivo_enviado_descriptografado:
        arquivo_enviado_descriptografado.write(descriptografado)
    return descriptografado

def server():
    chave = Fernet.generate_key()
    with open('chave.key', 'wb') as filekey:
        filekey.write(chave)
    host = '192.168.0.144'
    port = 65432
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Servidor aguardando conexões...")
    client_socket, addr = server_socket.accept()
    print(f"Conexão estabelecida com {addr}")
    file_hash = client_socket.recv(1024).decode()
    print(f"Hash recebido do arquivo: {file_hash}")
    client_socket.recv(1)
    encrypted_data = client_socket.recv(1024)
    print("Arquivo criptografado recebido!")
    try:
        print(f"Conteúdo criptografado:\n{encrypted_data}")
        decrypted_message = decrypt_message(encrypted_data, chave)
        print("Mensagem descriptografada!")
        decrypted_hash = hashlib.md5(decrypted_message).hexdigest()
        print(f"Hash do arquivo descriptografado: {decrypted_hash}")
        if file_hash == decrypted_hash:
            print("O arquivo foi transmitido com integridade!")
        else:
            print("O hash não corresponde! O arquivo pode ter sido alterado.")
    except Exception as e:
        print(f"Erro durante a decriptação: {e}")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    server()
