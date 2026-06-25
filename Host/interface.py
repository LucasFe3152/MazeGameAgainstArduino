import pygame
import sys

# mascara dos bits para as paredes
N_WALL = 0x01  # Norte
S_WALL = 0x02  # Sul
L_WALL = 0x04  # Leste
O_WALL = 0x08  # Oeste

# cores
fundo_tela = (30, 30, 30)
fundo_labirinto = (240, 240, 240)
cor_parede = (20, 20, 20)
texto_cor = (255, 255, 255)

class Interface:
    def __init__(self, n, tamanho_celula=30):
        # inicializa o pygame e configura a tela (humano e ia lado a lado
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
        self.font = pygame.font.SysFont("Comic Sans MS", 24)
        self.clock = pygame.time.Clock()

    def desenha_labirinto(self, labirinto, offset_x, offset_y, titulo):
        # desenha o título/fundo do labirinto
        labirinto_rect = (offset_x, offset_y, self.n * self.tamanho_celula, self.n * self.tamanho_celula)
        pygame.draw.rect(self.tela, fundo_labirinto, labirinto_rect)
        texto = self.font.render(titulo, True, texto_cor)
        self.tela.blit(texto, (offset_x, offset_y - 40))

#finalize