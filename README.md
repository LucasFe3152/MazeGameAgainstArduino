# 🕹️ 2Kb de RAM e um sonho

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

## 🚀 Como Executar

### Pré-requisitos
* Python 3.x
* Bibliotecas: `pygame` (ou `turtle`), `pyserial`
* Arduino IDE (para compilar e enviar o código C++)
* Uma placa Arduino (Uno, Nano, ou qualquer uma com pelo menos 2KB de RAM)

### Instalação
1. Clone este repositório:
   ```bash
   git clone [https://github.com/seu-usuario/2kb-de-ram-e-um-sonho.git](https://github.com/seu-usuario/2kb-de-ram-e-um-sonho.git)
   cd 2kb-de-ram-e-um-sonho
