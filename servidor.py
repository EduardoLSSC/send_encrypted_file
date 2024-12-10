import socket
from cryptography.fernet import Fernet
import hashlib
from colorama import init, Fore, Style, Back

def decrypt_message(message, chave):
    fernet = Fernet(chave)
    descriptografado = fernet.decrypt(message)
    with open('arquivo_enviado_descriptografado.txt', 'wb') as arquivo_enviado_descriptografado:
        arquivo_enviado_descriptografado.write(descriptografado)
    print(f"A mensagem descriptografada é" + Fore.CYAN + f" {descriptografado}")
    return descriptografado

def server():
    chave = Fernet.generate_key()
    with open('chave.key', 'wb') as filekey:
        filekey.write(chave)
    host = 'COLOCA O IP AQUI'
    port = 65432
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(Fore.YELLOW + "Servidor aguardando conexões...")
    client_socket, addr = server_socket.accept()
    print(Fore.CYAN + f"Conexão estabelecida com {addr}")
    file_hash = client_socket.recv(1024).decode()
    print(f"Hash recebido do arquivo:" + Fore.RED + f" {file_hash}")
    client_socket.recv(1)
    encrypted_data = client_socket.recv(1024)
    print(Fore.GREEN + "Arquivo criptografado recebido!")
    try:
        print(Fore.CYAN + f"Conteúdo criptografado:\n" + Style.RESET_ALL + f" {encrypted_data}")
        decrypted_message = decrypt_message(encrypted_data, chave)
        print(Fore.GREEN +  "Mensagem descriptografada!")
        decrypted_hash = hashlib.md5(decrypted_message).hexdigest()
        print(Fore.BLUE +f"Hash do arquivo descriptografado:" + Style.RESET_ALL + f" {decrypted_hash}")
        if file_hash == decrypted_hash:
            print(Fore.GREEN + "O arquivo foi transmitido com integridade!")
            
        else:
            print(Fore.RED + Style.BRIGHT + Back.LIGHTWHITE_EX +"O hash não corresponde! O arquivo pode ter sido alterado.")
    except Exception as e:
        print(Fore.RED + f"Erro durante a decriptação: {e}")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    init(autoreset = True)
    server()
