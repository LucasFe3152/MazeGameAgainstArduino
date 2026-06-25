import pygame
import sys
from maze_generator import gerador_labirinto, eh_soluvel
from serial_comm import SerialManager
from interface import Interface

# configurações
TAMANHO_LABIRINTO = 5
PORTA_SERIAL = "/dev/ttyUSB0"  

# Mascaras de parede correspondentes a interface
N_WALL = 0x01
S_WALL = 0x02
L_WALL = 0x04
O_WALL = 0x08

# inicio da comunicacao serial
serial_manager = SerialManager(port=PORTA_SERIAL)

def main():
    valido = False
    labirinto = None
    while not valido:
        labirinto = gerador_labirinto(TAMANHO_LABIRINTO)
        valido = eh_soluvel(labirinto)

    # enviando labirinto pro Arduino e iniciando escuta
    serial_manager.envia_labirinto(labirinto)

    # Inicializa a interface gráfica
    interface = Interface(TAMANHO_LABIRINTO)
    
    human_pos = [0, 0]
    vencedor = None
    running = True

    while running:
        # 1. Processamento de Inputs do Jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if vencedor is not None:
                    # Se o jogo acabou, reinicia com ESPAÇO ou fecha com ESC
                    if event.key == pygame.K_SPACE:
                        print("Reiniciando jogo...")
                        valido = False
                        while not valido:
                            labirinto = gerador_labirinto(TAMANHO_LABIRINTO)
                            valido = eh_soluvel(labirinto)
                        human_pos = [0, 0]
                        vencedor = None
                        serial_manager.envia_labirinto(labirinto)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    # Movimentação do jogador humano
                    dx, dy = 0, 0
                    if event.key in (pygame.K_UP, pygame.K_w):
                        if not (labirinto[human_pos[1]][human_pos[0]] & N_WALL):
                            dy = -1
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        if not (labirinto[human_pos[1]][human_pos[0]] & S_WALL):
                            dy = 1
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if not (labirinto[human_pos[1]][human_pos[0]] & O_WALL):
                            dx = -1
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if not (labirinto[human_pos[1]][human_pos[0]] & L_WALL):
                            dx = 1

                    if dx != 0 or dy != 0:
                        nx = human_pos[0] + dx
                        ny = human_pos[1] + dy
                        if 0 <= nx < TAMANHO_LABIRINTO and 0 <= ny < TAMANHO_LABIRINTO:
                            human_pos = [nx, ny]
                            # Verifica se o humano venceu
                            if human_pos == [TAMANHO_LABIRINTO - 1, TAMANHO_LABIRINTO - 1]:
                                vencedor = "H"
                                serial_manager.envia_fimdejogo("H")

        # 2. Atualizações de Estado da IA (Arduino)
        if vencedor is None:
            # Caso o Arduino informe a vitória na serial (<WIN>)
            if serial_manager.winner == "A":
                vencedor = "A"
                serial_manager.envia_fimdejogo("A")
            # Caso o Arduino chegue ao final do labirinto (coordenada n-1, n-1)
            elif list(serial_manager.arduino_pos) == [TAMANHO_LABIRINTO - 1, TAMANHO_LABIRINTO - 1]:
                vencedor = "A"
                serial_manager.envia_fimdejogo("A")

        # Posição atualizada do Arduino
        arduino_pos = list(serial_manager.arduino_pos)

        # 3. Desenho de Tela
        interface.desenha_tudo(labirinto, human_pos, arduino_pos, vencedor)
        interface.clock.tick(60)

    serial_manager.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
