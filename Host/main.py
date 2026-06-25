import pygame
import sys
from maze_generator import gerador_labirinto, eh_soluvel
from serial_comm import SerialManager

# configurações
TAMANHO_LABIRINTO = 16
PORTA_SERIAL = "COM3" # ALTERAR BASEADO NA SUA PORTA SERIAL

# inicio da comunicacao serial
serial_manager = SerialManager(port=PORTA_SERIAL)

valido = False
while not valido:
    labirinto = gerador_labirinto(TAMANHO_LABIRINTO)
    valido = eh_soluvel(labirinto)

# enviando labirinto pro Arduino
serial_manager.envia_labirinto(labirinto)

# interface assume o loop principal do jogo
# implementar a Thread de escuta (SerialRx) para ler os passos <MOVE,x,y>

def main():
    pygame.init()
    # TODO: Setup display, threads, and main game loop
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
