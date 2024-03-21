import subprocess
import os

try:
    subprocess.check_call(["pip", "install", "nmap", "python-nmap", "whois", "colorama"])
except subprocess.CalledProcessError:
    print("Falha ao instalar os pacotes necessários. Certifique-se de que o pip está instalado.")

import socket
import nmap
import whois
from colorama import init, Fore

init(autoreset=True)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def verificar_udp_tcp(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_tcp.settimeout(1)
        socket_udp.settimeout(1)
        resultado_tcp = socket_tcp.connect_ex((ip, 80))
        resultado_udp = socket_udp.connect_ex((ip, 80))
        socket_tcp.close()
        socket_udp.close()
        if resultado_tcp == 0:
            print(Fore.GREEN + f"{hostname} suporta TCP")
        else:
            print(Fore.RED + f"{hostname} não suporta TCP")
        if resultado_udp == 0:
            print(Fore.GREEN + f"{hostname} suporta UDP")
        else:
            print(Fore.RED + f"{hostname} não suporta UDP")
    except socket.error:
        print(Fore.RED + "Erro: Não foi possível resolver o nome do host")

def verificar_portas_abertas(hostname):
    try:
        nm = nmap.PortScanner()
        nm.scan(hostname, arguments='-p 1-65535 --open')
        for host in nm.all_hosts():
            print(Fore.GREEN + f"Portas abertas para {host}:")
            for proto in nm[host].all_protocols():
                portas = nm[host][proto].keys()
                for porta in portas:
                    print(Fore.YELLOW + f"A porta {porta}/{proto} está aberta")
    except nmap.nmap.PortScannerError:
        print(Fore.RED + "Erro: Não foi possível escanear o host")

def obter_ip(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        print(Fore.GREEN + f"O endereço IP de {hostname} é: {ip}")
    except socket.error:
        print(Fore.RED + "Erro: Não foi possível resolver o nome do host")

def obter_localizacao_do_host(hostname):
    try:
        info_dominio = whois.whois(hostname)
        if info_dominio:
            if 'country' in info_dominio:
                print(Fore.GREEN + f"{hostname} está hospedado em {info_dominio['country']}")
            else:
                print(Fore.RED + "Não foi possível determinar a localização do host")
        else:
            print(Fore.RED + "Não foi possível obter informações do domínio")
    except Exception as e:
        print(Fore.RED + f"Erro: {e}")

def main():
    while True:
        limpar_tela()
        print("\n" + Fore.CYAN + "Menu:")
        print("1. Verificar suporte UDP e TCP de um site")
        print("2. Verificar portas abertas de um site")
        print("3. Obter o endereço IP de um site")
        print("4. Obter localização do host")
        print("5. Sair")

        escolha = input(Fore.YELLOW + "Digite sua escolha: ")

        if escolha == '1':
            hostname = input("Digite o endereço do site: ")
            verificar_udp_tcp(hostname)
        elif escolha == '2':
            hostname = input("Digite o endereço do site: ")
            verificar_portas_abertas(hostname)
        elif escolha == '3':
            hostname = input("Digite o endereço do site: ")
            obter_ip(hostname)
        elif escolha == '4':
            hostname = input("Digite o endereço do site: ")
            obter_localizacao_do_host(hostname)
        elif escolha == '5':
            print(Fore.MAGENTA + "Encerrando o programa.")
            break
        else:
            print(Fore.RED + "Escolha inválida. Por favor, digite um número entre 1 e 5.")

        input(Fore.YELLOW + "Pressione Enter para continuar...")
        limpar_tela()

    print("\n" + Fore.YELLOW + "Zedhacking, salve Alexandre")

if __name__ == "__main__":
    main()
