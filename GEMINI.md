# Contexto do Projeto: 2Kb de RAM e um sonho

## Objetivo Principal
Este repositório contém um sistema de Edge AI competitivo desenvolvido para a DataWeek. O projeto consiste em uma corrida em tempo real para resolver um labirinto: um usuário humano operando via teclado contra um Arduino rodando um modelo de Q-Learning on-device.

## Restrições Críticas de Desenvolvimento
* **Memória SRAM Limitada:** O Arduino possui apenas 2KB de RAM. Todas as soluções em C/C++ devem priorizar economia extrema de memória.
* **Tipagem Estrita:** É estritamente proibido o uso de `float` ou `double` no Arduino, a menos que seja matematicamente inevitável. A Tabela Q deve utilizar inteiros de 8 bits (`int8_t` ou `uint8_t`) escalonados.
* **Alocação Dinâmica:** Evite `malloc()` ou `String` no Arduino para prevenir fragmentação de memória e *stack crash*.
* **Processamento Paralelo:** O host (Python) nunca deve bloquear a renderização da interface enquanto aguarda a comunicação Serial.

## Estrutura de Dados do Labirinto
O labirinto é representado por uma matriz $N \times N$. Para economizar memória no microcontrolador, o estado das paredes de cada célula deve ser codificado em um único byte usando operações *bitwise* nos 4 bits menos significativos (LSB):

* **Bit 0 (0x01):** Parede ao Norte
* **Bit 1 (0x02):** Parede ao Sul
* **Bit 2 (0x04):** Parede a Leste
* **Bit 3 (0x08):** Parede a Oeste

## Protocolo de Comunicação Serial

A comunicação entre o Host e o Edge ocorre via interface Serial. Os pacotes devem ser curtos e possuir marcadores de início e fim.

| Comando (Python -> Arduino) | Descrição |
| :--- | :--- |
| `<INIT,N>` | Inicia uma nova partida informando o tamanho $N$ do labirinto. |
| `<ROW,y,data>` | Envia uma linha do labirinto (array de bytes codificados com paredes). |
| `<START>` | Libera o Arduino para iniciar o treinamento e a corrida. |
| `<END,winner>` | Sinaliza o fim do jogo. `winner` pode ser `H` (Humano) ou `A` (Arduino). |

| Comando (Arduino -> Python) | Descrição |
| :--- | :--- |
| `<ACK>` | Confirmação genérica de recebimento de pacote. |
| `<MOVE,x,y>` | Informa o passo consolidado pelo Q-Learning no caminho ótimo. |
| `<WIN>` | Arduino informa que alcançou a célula de saída. |

## Módulos do Sistema

### 1. Host (Python)
* **Gerador:** Cria labirintos usando algoritmos como *Recursive Backtracker* e valida a solubilidade via Busca em Largura (BFS).
* **Interface:** Utiliza `pygame` ou `turtle` para desenhar dois painéis simultâneos (Humano vs. IA).
* **Threads:** * `Main`: Gerencia o loop da interface, input do usuário de 60 FPS e regras de vitória.
  * `SerialTx`: Thread responsável por empacotar e enviar o labirinto gerado.
  * `SerialRx`: Thread em escuta contínua para atualizar o cursor do Arduino na tela baseado nas mensagens `<MOVE,x,y>`.

### 2. Edge (Arduino / C++)
* **Decodificador:** Lê a matriz via Serial e reconstrói o mapa de bits na memória local.
* **Agente Q-Learning:** * Implementa a equação de Bellman adaptada para inteiros.
  * Executa a política $\epsilon$-greedy para exploração/explotação do labirinto.
  * Ao estabilizar o aprendizado de um caminho (ou atingir um limite de episódios), reporta a trajetória via Serial.
* **Gerenciador de Estado:** Ouve constantemente a Serial para parar a execução caso receba um comando `<END>`.