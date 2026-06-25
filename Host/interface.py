import pygame
import sys

# mascara dos bits para as paredes
N_WALL = 0x01  # Norte
S_WALL = 0x02  # Sul
L_WALL = 0x04  # Leste
O_WALL = 0x08  # Oeste

# cores
fundo_tela = (15, 15, 20)
fundo_labirinto = (25, 25, 35)
cor_parede = (70, 130, 180) # Steel blue walls
texto_cor = (240, 240, 240)

class Interface:
    def __init__(self, n, tamanho_celula=30):
        # inicializa o pygame e configura a tela (humano e ia lado a lado)
        pygame.init()
        self.n = n
        self.tamanho_celula = tamanho_celula

        # margens(espacamento)
        self.margem_x = 50
        self.margem_y = 80

        # largura e altura total
        self.largura = (self.n * self.tamanho_celula * 2) + (3 * self.margem_x)
        self.altura = (self.n * self.tamanho_celula) + (2 * self.margem_y)

        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("2Kb de RAM e um Sonho: Humano vs IA (Arduino)")
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.clock = pygame.time.Clock()

    def desenha_labirinto(self, labirinto, offset_x, offset_y, titulo):
        # desenha o título/fundo do labirinto
        labirinto_rect = (offset_x, offset_y, self.n * self.tamanho_celula, self.n * self.tamanho_celula)
        pygame.draw.rect(self.tela, fundo_labirinto, labirinto_rect)

        # Célula inicial (0, 0) em verde suave
        start_rect = (offset_x, offset_y, self.tamanho_celula, self.tamanho_celula)
        pygame.draw.rect(self.tela, (34, 139, 34), start_rect) # Forest Green

        # Célula final (n-1, n-1) em vermelho suave
        end_rect = (offset_x + (self.n - 1) * self.tamanho_celula, offset_y + (self.n - 1) * self.tamanho_celula, self.tamanho_celula, self.tamanho_celula)
        pygame.draw.rect(self.tela, (178, 34, 34), end_rect) # Firebrick Red

        # Desenha as paredes
        for y in range(self.n):
            for x in range(self.n):
                val = labirinto[y][x]
                cell_left = offset_x + x * self.tamanho_celula
                cell_top = offset_y + y * self.tamanho_celula
                cell_right = cell_left + self.tamanho_celula
                cell_bottom = cell_top + self.tamanho_celula

                if val & N_WALL:
                    pygame.draw.line(self.tela, cor_parede, (cell_left, cell_top), (cell_right, cell_top), 2)
                if val & S_WALL:
                    pygame.draw.line(self.tela, cor_parede, (cell_left, cell_bottom), (cell_right, cell_bottom), 2)
                if val & L_WALL:
                    pygame.draw.line(self.tela, cor_parede, (cell_right, cell_top), (cell_right, cell_bottom), 2)
                if val & O_WALL:
                    pygame.draw.line(self.tela, cor_parede, (cell_left, cell_top), (cell_left, cell_bottom), 2)

        texto = self.font.render(titulo, True, texto_cor)
        self.tela.blit(texto, (offset_x, offset_y - 40))

    def desenha_jogador(self, x, y, offset_x, offset_y, cor):
        # desenha o jogador centralizado na célula (x, y)
        cx = offset_x + x * self.tamanho_celula + self.tamanho_celula // 2
        cy = offset_y + y * self.tamanho_celula + self.tamanho_celula // 2
        raio = self.tamanho_celula // 3
        # Desenha brilho
        pygame.draw.circle(self.tela, (cor[0], cor[1], cor[2], 100), (cx, cy), raio + 4, 1)
        pygame.draw.circle(self.tela, cor, (cx, cy), raio)

    def desenha_tudo(self, labirinto, jogador_pos, arduino_pos, vencedor=None):
        self.tela.fill(fundo_tela)

        # Desenha labirinto do jogador humano
        self.desenha_labirinto(labirinto, self.margem_x, self.margem_y, "JOGADOR (VOCÊ)")
        self.desenha_jogador(jogador_pos[0], jogador_pos[1], self.margem_x, self.margem_y, (0, 255, 255)) # Cyan player

        # Desenha labirinto do Arduino
        offset_arduino_x = (self.n * self.tamanho_celula) + 2 * self.margem_x
        self.desenha_labirinto(labirinto, offset_arduino_x, self.margem_y, "EDGE AI (ARDUINO)")
        self.desenha_jogador(arduino_pos[0], arduino_pos[1], offset_arduino_x, self.margem_y, (255, 215, 0)) # Gold Arduino

        # Se houver vencedor, desenha overlay de fim de jogo
        if vencedor:
            overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.tela.blit(overlay, (0, 0))

            msg = "VITÓRIA DO HUMANO!" if vencedor == "H" else "VITÓRIA DO ARDUINO!"
            cor_msg = (0, 255, 255) if vencedor == "H" else (255, 215, 0)

            texto_vitoria = self.font.render(msg, True, cor_msg)
            rect_vitoria = texto_vitoria.get_rect(center=(self.largura // 2, self.altura // 2 - 20))
            self.tela.blit(texto_vitoria, rect_vitoria)

            texto_sub = self.font.render("Pressione ESPAÇO para reiniciar ou ESC para sair", True, (200, 200, 200))
            rect_sub = texto_sub.get_rect(center=(self.largura // 2, self.altura // 2 + 30))
            self.tela.blit(texto_sub, rect_sub)

        pygame.display.flip()