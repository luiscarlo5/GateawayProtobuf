import socket
import time
import Gateway_pb2 as proto


class TemperatureSensor(Equipment):
    def __init__(self, dtype, name, ip, port, sensor_id, temperature):
        super().__init__(dtype, name, ip, port)
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.server_socket = None

    def setup_server(self):
        """
        Configura o servidor TCP para escutar conexões.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        print(f"Sensor {self.name} está pronto e escutando em {self.ip}:{self.port}.")

    def handle_request(self, client_socket):
        """
            Lida com uma solicitação recebida.
        """
        try:
            data = client_socket.recv(1024)
            if not data:
                return

            # Interpreta a solicitação usando Protobuf
            request = proto.TemperatureData()
            request.ParseFromString(data)

            # Cria a resposta com os dados do sensor
            response = proto.TemperatureData()
            response.sensor_id = self.sensor_id
            response.temperatura = self.temperature
            response.timestamp = int(time.time())

            # Envia a resposta serializada
            client_socket.sendall(response.SerializeToString())
            print(f"Enviado: Sensor {self.sensor_id}, Temperatura {self.temperature}°C")
        except Exception as e:
            print(f"Erro ao lidar com a solicitação: {e}")
        finally:
            client_socket.close()

    def run(self):
        """
            Inicia o loop principal do servidor, aguardando conexões.
        """
        self.setup_server()

        while True:
            try:
                print("Aguardando conexão...")
                client_socket, addr = self.server_socket.accept()
                print(f"Conexão recebida de {addr}")
                self.handle_request(client_socket)
            except KeyboardInterrupt:
                print("Encerrando servidor...")
                break
            except Exception as e:
                print(f"Erro no servidor: {e}")

        # Fecha o socket do servidor ao sair
        self.server_socket.close()


if __name__ == "__main__":
    # Inicializa o sensor de temperatura
    temp_sensor = TemperatureSensor(
        dtype=proto.DeviceInfo.DeviceType.TEMPERATURE_SENSOR,
        name="TempSensor 1",
        ip="127.0.0.1",
        port=8000,
        sensor_id="TEMP001",
        temperature=25.0,  # Temperatura inicial
    )

    # Envia a identificação antes de começar a escutar
    temp_sensor.send_identification()

    # Inicia o loop do servidor
    temp_sensor.run()
