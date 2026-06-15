import pygame
import sys
from maze_generator import MazeGenerator
from serial_comm import SerialManager

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
