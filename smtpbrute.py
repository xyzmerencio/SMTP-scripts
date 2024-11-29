#!/usr/bin/python3

import socket
import sys
import re

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 script.py <IP> <WORDLIST>")
        sys.exit(1)

    ip_address = sys.argv[1]
    user_file = sys.argv[2]

    try:
        with open(user_file, 'r') as file:
            for line in file:
                username = line.strip()
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
                        tcp.connect((ip_address, 25))
                        banner = tcp.recv(1024).decode('utf-8', errors='ignore')
                        tcp.sendall(f"VRFY {username}\r\n".encode('utf-8'))
                        response = tcp.recv(1024).decode('utf-8', errors='ignore')

                        if re.search(r"\b252\b", response):
                            print(f"Usuário encontrado: {username}")
                except socket.error as e:
                    print(f"Erro ao conectar com o servidor: {e}")
                    continue
    except FileNotFoundError:
        print(f"Arquivo '{user_file}' não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
