import socket
import struct

def OuveMultcast():

    # Configurações do Multicast
    MCAST_GRP = '239.255.0.1'  # Deve coincidir com o do remetente
    MCAST_PORT = 6789          # Deve coincidir com o do remetente

    # Criando o socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Vincula o socket à porta multicast
    sock.bind(('', MCAST_PORT))  # '' permite ouvir em todas as interfaces locais

    # Inscreve-se no grupo multicast
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Aguardando mensagens multicast...")
    try:
        while True:
            # Recebe mensagens multicast
            data, addr = sock.recvfrom(1024)  # Tamanho máximo da mensagem
            print(f"Mensagem recebida: {data.decode('utf-8')} de {addr}")

            # Extrai o IP do remetente e tenta conectar
            sender_ip = data.decode('utf-8').split(":")[-1].strip()
            print(f"Tentando conectar ao dispositivo em {sender_ip}...")
            ConectaTCP(sender_ip)
            break
    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        sock.close()

def ConectaTCP(sender_ip):
    # No multicast_listener.py
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    tcp_socket.connect((sender_ip, 12345))
    
    print(tcp_socket.recv(1024).decode('utf-8'))
    
    tcp_socket.close()

