import serial
import threading
import time

class SerialManager:
    def __init__(self, port, baudrate=115200):
        self.timeout = 5  # 5 seconds timeout for waits
        self.serial_port = None
        self.is_connected = False
        self.arduino_pos = (0, 0)
        self.winner = None
        self.rx_thread = None
        self.rx_running = False
        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            self.is_connected = True
            print(f"Connectado na porta {port} com {baudrate} baud.")
        except serial.SerialException as e:
            self.is_connected = False
            print(f"Erro ao conectar na porta {port}: {e}")

    def envia_labirinto(self, labirinto):
        if not self.is_connected:
            print("Não conectado à porta serial.")
            return
        
        # Interrompe escuta anterior para evitar conflito de leitura na serial
        self.stop_rx_loop()
        self.arduino_pos = (0, 0)
        self.winner = None
        
        n = len(labirinto)

        try:
            # envia o tamanho do labirinto
            self.serial_port.write(f"<INIT,{n}>\n".encode('utf-8'))
            self.espera_ack()
            
            # envia cada linha do labirinto
            for y, linha in enumerate(labirinto):
                # Padrão: <ROW,y,COLUNA1,COLUNA2,...,COLUNAN>
                dados_str = ",".join(str(val) for val in linha)
                pacote = f"<ROW,{y},{dados_str}>\n"
                self.serial_port.write(pacote.encode('utf-8'))
                self.espera_ack()

            self.serial_port.write(b"<START>\n") # libera o arduino para iniciar o jogo
            self.espera_ack()
            print("Labirinto enviado com sucesso!")
            
            # Inicia thread de escuta em segundo plano para capturar o progresso do Arduino
            self.start_rx_loop()

        except serial.SerialException as e:
            print(f"Erro ao enviar labirinto: {e}")

    def espera_ack(self):
        # ouve a porta serial até receber um ACK do Arduino (antes do loop de jogo iniciar)
        start_time = time.time()
        buffer = ""
        while (time.time() - start_time) < self.timeout:
            if self.serial_port and self.serial_port.in_waiting > 0:
                char = self.serial_port.read(1).decode('utf-8', errors='ignore')
                buffer += char
                if ">" in buffer:
                    if "ACK" in buffer:
                        return True
                    buffer = ""
        print("ACK nao recebido do arduino. O arduino pode ter travado ou desconectado.")
        return False

    def start_rx_loop(self):
        if not self.rx_running:
            self.rx_running = True
            self.rx_thread = threading.Thread(target=self._rx_loop, daemon=True)
            self.rx_thread.start()
            print("Thread SerialRx iniciada com sucesso.")

    def stop_rx_loop(self):
        self.rx_running = False
        if self.rx_thread:
            # Não fazemos join longo pois a thread é daemon, mas limpamos a referência
            self.rx_thread = None

    def _rx_loop(self):
        buffer = ""
        while self.rx_running and self.is_connected and self.serial_port and self.serial_port.is_open:
            try:
                if self.serial_port.in_waiting > 0:
                    dados = self.serial_port.read(self.serial_port.in_waiting).decode('utf-8', errors='ignore')
                    buffer += dados
                    
                    while "<" in buffer and ">" in buffer:
                        start_idx = buffer.find("<")
                        end_idx = buffer.find(">", start_idx)
                        if end_idx != -1:
                            mensagem = buffer[start_idx+1:end_idx]
                            buffer = buffer[end_idx+1:]
                            self._processa_mensagem(mensagem)
                        else:
                            break
            except Exception as e:
                print(f"Erro na recepção da serial: {e}")
                break
            time.sleep(0.01)

    def _processa_mensagem(self, mensagem):
        partes = mensagem.split(",")
        cmd = partes[0]
        if cmd == "MOVE" and len(partes) == 3:
            try:
                x = int(partes[1])
                y = int(partes[2])
                self.arduino_pos = (x, y)
            except ValueError:
                pass
        elif cmd == "WIN":
            self.winner = "A"
            print("Sinal <WIN> recebido do Arduino!")
    
    def envia_fimdejogo(self, ganhador):
        # sinaliza fim de jogo. vencedor 'H'=humano, 'A'=arduino
        if self.is_connected and self.serial_port:
            cmd = f"<END,{ganhador}>\n".encode('utf-8')
            self.serial_port.write(cmd)
            print(f"Fim de jogo enviado. Vencedor: {ganhador}")

    def close(self):
        self.stop_rx_loop()
        #fechando a conexao serial
        if self.is_connected and self.serial_port and self.serial_port.is_open:
            self.serial_port.close()