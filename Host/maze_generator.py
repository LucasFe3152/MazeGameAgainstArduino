import random
from collections import deque

# mascaras dos bits para as paredes 
N_WALL = 0x01  
S_WALL = 0x02  
L_WALL = 0x04  
O_WALL = 0x08  

def gerador_labirinto(n):
    # inicia o labirinto nxn com todas as paredes
    labirinto = [[N_WALL | S_WALL | L_WALL | O_WALL for _ in range(n)] for _ in range(n)]

    #  matriz nxn de células visitadas
    visitadas = [[False for _ in range(n)] for _ in range(n)]
    
    # ponto de partida
    start_x, start_y = 0, 0
    visitadas[start_y][start_x] = True
    
    # pilha para backtracking
    stack = deque()
    stack.append((start_x, start_y))
    
    while stack:
        x, y = stack[-1]
        
        # Lista de vizinhos não visitados
        vizinhos = []
        
        # Norte
        if y > 0 and not visitadas[y - 1][x]: 
            vizinhos.append((x, y - 1, N_WALL, S_WALL))
        # Sul
        if y < n - 1 and not visitadas[y + 1][x]:  
            vizinhos.append((x, y + 1, S_WALL, N_WALL))
        # Oeste
        if x > 0 and not visitadas[y][x - 1]:  
            vizinhos.append((x - 1, y, O_WALL, L_WALL))
        # Leste
        if x < n - 1 and not visitadas[y][x + 1]:  
            vizinhos.append((x + 1, y, L_WALL, O_WALL))
        
        if vizinhos:
            # pega um vizinho aleatório
            nx, ny, parede_a_remover, parede_a_adicionar = random.choice(vizinhos)
            
            # remove a parede entre a célula atual e o vizinho escolhido
            labirinto[y][x] &= ~parede_a_remover
            labirinto[ny][nx] &= ~parede_a_adicionar
            
            # marca o vizinho como visitado e adiciona à pilha
            visitadas[ny][nx] = True
            stack.append((nx, ny))
        else:
            # se não houver vizinhos não visitados, volta na pilha
            stack.pop()
    
    return labirinto

def eh_soluvel(labirinto):
    # usa busca em largura (BFS) para verificar se há um caminho do início ao fim
    n = len(labirinto)
    start_x, start_y = 0, 0
    end_x, end_y = n - 1, n - 1
    
    fila = deque() # fila para a Busca em Largura armazenando tuplas 
    fila.append((start_x, start_y))
    
    c_visitadas = set() # conjunto para rastrear células já visitadas e evitar loops infinitos
    c_visitadas.add((start_x, start_y))
    
    while fila:
        x, y = fila.popleft()
        
        if x == end_x and y == end_y: # verifica se alcançou o destino final
            return True
            
        # le as paredes atuais da célula e verifica os vizinhos alcançáveis (caminhos sem parede)
        current_walls = labirinto[y][x]
        
        # tentativa Norte
        if y > 0 and not (current_walls & N_WALL):
            if (x, y - 1) not in c_visitadas:
                c_visitadas.add((x, y - 1))
                fila.append((x, y - 1))
                
        # tentativa Sul
        if y < n - 1 and not (current_walls & S_WALL):
            if (x, y + 1) not in c_visitadas:
                c_visitadas.add((x, y + 1))
                fila.append((x, y + 1))
                
        # tentativa Leste (direita)
        if x < n - 1 and not (current_walls & L_WALL):
            if (x + 1, y) not in c_visitadas:
                c_visitadas.add((x + 1, y))
                fila.append((x + 1, y))
                
        # tentativa Oeste (esquerda)
        if x > 0 and not (current_walls & O_WALL):
            if (x - 1, y) not in c_visitadas:
                c_visitadas.add((x - 1, y))
                fila.append((x - 1, y))        
    return False    # o labirinto é insolúvel se a fila esvaziar sem alcançar o destino final

# -teste-
if __name__ == "__main__":
    tamanho = 16
    labirinto = gerador_labirinto(tamanho)
    
    soluvel = eh_soluvel(labirinto)
    
    print(f"Labirinto {tamanho}x{tamanho} gerado com sucesso.")
    if soluvel:
        print("o labirinto eh soluvel")
    else:
        print("o labirinto NAO eh soluvel")