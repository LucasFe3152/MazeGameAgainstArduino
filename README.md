# 2Kb de RAM e um sonho

Bem-vindo ao **2Kb de RAM e um sonho**, um projeto de demonstração de Edge AI focado em eficiência e aprendizado por reforço, desenvolvido para a **DataWeek**. 

Este projeto coloca você (humano) em uma corrida de resolução de labirintos contra um Arduino. Enquanto você usa o teclado para encontrar a saída, o microcontrolador recebe o labirinto em tempo real, treina um algoritmo de Q-Learning diretamente no hardware e tenta encontrar o caminho ideal para te vencer. Tudo isso limitado a míseros 2 Kilobytes de SRAM.

## 🧠 Arquitetura do Projeto

O sistema é dividido em dois nós principais operando em paralelo e se comunicando via interface Serial.

### 1. O Computador (Python / Host)
Responsável pela infraestrutura, geração do ambiente e interface com o usuário.
* **Geração de Ambiente:** Cria labirintos aleatórios e garante, matematicamente, que são solúveis.
* **Interface Gráfica (Pygame/Turtle):** Renderiza duas instâncias do labirinto simultaneamente (Jogador vs. Edge AI).
* **Comunicação Multithread:** * Uma *thread* dedicada ao envio assíncrono da topologia do labirinto para o Arduino.
  * Uma *thread* em escuta constante via PySerial para capturar e espelhar as decisões do algoritmo na tela.
* **Juiz da Partida:** Monitora o progresso de ambos, declara o vencedor na GUI e sinaliza o fim do jogo via Serial.

### 2. O Arduino (Edge AI / Agente)
O coração do projeto. Demonstra que inteligência artificial não requer data centers, mas sim otimização inteligente de recursos.
* **Recepção de Dados:** Recebe a matriz do labirinto via Serial.
* **Otimização de Memória Extrema:** O mapa é armazenado em uma matriz $N \times N$ de bytes. Utiliza operações *bitwise* para mapear paredes: apenas 4 bits por célula (Norte, Sul, Leste, Oeste), economizando espaço vital para o algoritmo.
* **Q-Learning On-Device:** Roda o treinamento por reforço localmente. O Arduino explora, aprende e explota o ambiente.
* **Feedback em Tempo Real:** Cada decisão consolidada no "melhor caminho" (política ótima) é transmitida de volta ao Python.
* **Loop de Jogo:** Ao receber a flag de término (vitória ou derrota), limpa a memória e aguarda o próximo desafio.

## 📂 Estrutura do Repositório

O repositório está dividido em duas partes principais: **Host** (o computador que roda o jogo e gerencia a interface) e **Edge** (o Arduino que resolve o labirinto).

*   **`Host/` (Python)**:
    *   `main.py`: Ponto de entrada da aplicação, gerencia a interface gráfica e o loop principal do jogo.
    *   `maze_generator.py`: Contém a lógica de geração do labirinto (ex: Recursive Backtracker) e validação (Busca em Largura - BFS).
    *   `serial_comm.py`: Gerencia as *threads* de comunicação Serial (Tx e Rx) para interagir com o microcontrolador de forma assíncrona.
    *   `requirements.txt`: Lista de dependências do projeto Python (como `pygame` e `pyserial`).
*   **`Edge/` (Arduino / C++)**:
    *   **`MazeSolver/`**: Diretório contendo o sketch do Arduino (requisito da Arduino IDE).
        *   `MazeSolver.ino`: Arquivo principal do Arduino, gerencia o fluxo principal (`setup` e `loop`).
        *   `maze_protocol.h` / `.cpp`: Lida com o recebimento do mapa via Serial, utilizando operações *bitwise* para compactar o labirinto, e envio das ações do agente.
        *   `q_learning.h` / `.cpp`: Implementação local do algoritmo de Q-Learning (Equação de Bellman) estritamente adaptada para variáveis inteiras e mínimo uso de RAM (2KB limit).

## 🚀 Como Executar

### Pré-requisitos
* Python 3.x
* Bibliotecas: `pygame`, `pyserial`
* Arduino IDE (para compilar e enviar o código C++)
* Uma placa Arduino (Uno, Nano, ou qualquer uma com pelo menos 2KB de RAM)

### Instalação
1. Clone este repositório:
   ```bash
   git clone [https://github.com/LucasFe3152/MazeGameAgainstArduino.git](https://github.com/LucasFe3152/MazeGameAgainstArduino.git)
   cd MazeGameAgainstArduino
