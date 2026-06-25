import serial
import threading
import time

class SerialManager:
    def __init__(self, port, baudrate=115200):
        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            self.is_connected = True
            print(f"Connectado na porta {port} com {baudrate} baud.")
        except serial.SerialException as e:
            self.is_connected = False
            print(f"Erro ao conectar na porta {port}: {e}")

    def envia_labirinto(self, labirinto):
        # iniciando a transmissao em uma nova thread
        if not self.is_connected:
            print("Não conectado à porta serial.")
            return
        
        n=len(labirinto)

        try:
            # envia o tamanho do labirinto
            self.serial_port.write(f"<INIT,{n}>\n".encode('utf-8'))
            self.espera_ack()
            
            # envia cada linha do labirinto
            for y, linha in enumerate(labirinto):
                cabecalho = f"<LINE,{y}>"
                dados = bytearray(linha) # de int8 p bytes
                rodape = b">\n"

                self.serial_port.write(cabecalho.encode('utf-8') + dados + rodape) # montando o pacote da linha
                self.espera_ack()

            self.serial_port.write(b"<START>\n") # libera o arduino para iniciar o jogo
            self.espera_ack()
            print("Labirinto enviado com sucesso!")

        except serial.SerialException as e:
            print(f"Erro ao enviar labirinto: {e}")

        def espera_ack(self):
            # ouve a porta serial até receber um ACK do Arduino
            start_time = time.time()
            while (time.time() - start_time) < timeout:
                if self.serial_port.in_waiting > 0:
                    linha = self.serial_port.readline().decode('utf-8').strip()
                    if linha == "ACK":
                        return True
            print("ACK nao recebido do arduino. O arduino pode ter travado ou desconectado.")
            return False
        
        def envia_fimdejogo(self, ganhador):
            # sinaliza fim de jogo. vencedor 'H'=humano, 'A'=arduino
            if not self.is_connected:
                cmd = f"<END,{ganhador}>\n".encode('utf-8')
                self.serial_port.write(cmd)
                print(f"Fim de jogo enviado. Vencedor: {ganhador}")

        def close(self):
            #fechando a conexao serial
            if self.is_connected and self.serial_port.is_open:
                self.serial_port.close()