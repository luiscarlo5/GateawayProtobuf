import socket
import Gateway_pb2 as photo # Agora você pode importar como se estivesse no mesmo diretório


class DeviceManager:
    """Classe para gerenciar dispositivos conectados ao gateway."""
    def __init__(self):
        self.devices = {}

    def update_device(self, device_id, data):
        self.devices[device_id] = data

    def display_devices(self):
        print("Estado atual dos dispositivos conectados:")
        for device_id, data in self.devices.items():
            print(f"  {device_id}: {data}")


class Gateway:
    def __init__(self):
        print("Inicializando o Gateway...")
        self.device_manager = DeviceManager()
        self.tcp_server()

    def tcp_server(self):
        TCP_PORT = 12345
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind(("", TCP_PORT))
        tcp_server.listen(5)
        print(f"Servidor TCP ouvindo na porta {TCP_PORT}...")

        while True:
            conn, addr = tcp_server.accept()
            print(f"Conexão estabelecida com {addr}")
            data = conn.recv(4096)

            if not data:
                conn.close()
                continue

            self.process_message(data, addr)
            conn.sendall(b"Mensagem processada com sucesso!")
            conn.close()

    def process_message(self, data, addr):
        """Processa mensagens de dispositivos e atualiza o estado."""
        try:
            # Tenta decodificar como `TemperatureData`
            temp_data = photo.TemperatureData()
            temp_data.ParseFromString(data)
            self.device_manager.update_device(
                temp_data.sensor_id,
                f"Temperatura: {temp_data.temperatura}°C, Timestamp: {temp_data.timestamp}"
            )
            print(f"[{addr}] Sensor de Temperatura: {temp_data.sensor_id}, "
                  f"Valor: {temp_data.temperatura}°C")
            return

        except Exception:
            pass

        try:
            # Tenta decodificar como `LedControl`
            led_data = photo.LedControl()
            led_data.ParseFromString(data)
            self.device_manager.update_device(
                led_data.led_id,
                f"LED: {'Ligado' if led_data.ligar else 'Desligado'}, Timestamp: {led_data.timestamp}"
            )
            print(f"[{addr}] Controle de LED: {led_data.led_id}, "
                  f"Ligar: {'Sim' if led_data.ligar else 'Não'}")
            return

        except Exception:
            pass

        try:
            # Tenta decodificar como `HumidityData`
            humidity_data = photo.HumidityData()
            humidity_data.ParseFromString(data)
            self.device_manager.update_device(
                humidity_data.sensor_id,
                f"Umidade: {humidity_data.umidade}%, Timestamp: {humidity_data.timestamp}"
            )
            print(f"[{addr}] Sensor de Umidade: {humidity_data.sensor_id}, "
                  f"Valor: {humidity_data.umidade}%")
            return

        except Exception:
            print(f"[{addr}] Mensagem recebida não corresponde a nenhum tipo conhecido.")
            return


# Teste do Gateway
if __name__ == "__main__":
    gateway = Gateway()
