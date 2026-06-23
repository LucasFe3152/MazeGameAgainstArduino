# Protocolo de Comunicação Serial: Host <-> Edge

Este documento descreve o protocolo de comunicação utilizado para a sincronização, transferência de labirintos e corrida em tempo real entre o **Host (Python)** e o **Edge (Arduino/C++)**.

---

## 1. Estrutura do Pacote
Para garantir robustez física na transmissão serial, todas as mensagens trocadas entre o Host e o Edge devem conter marcadores explícitos de início e fim de pacote:
* **Marcador de Início**: `<` (ASCII `0x3C`)
* **Marcador de Fim**: `>` (ASCII `0x3E`)

Qualquer caractere recebido fora desses delimitadores deve ser sumariamente ignorado pelo receptor. Os argumentos internos de cada comando são separados por vírgula (`,`).

---

## 2. Codificação das Células do Labirinto
O labirinto é uma matriz $N \times N$. Para economizar memória SRAM no Arduino (limite de 2KB), o estado das paredes de cada célula do labirinto é codificado em um único byte usando os 4 bits menos significativos (LSB):

| Bit | Máscara Bitwise | Direção da Parede |
| :---: | :---: | :--- |
| **Bit 0** | `0x01` | Parede ao **Norte** |
| **Bit 1** | `0x02` | Parede ao **Sul** |
| **Bit 2** | `0x04` | Parede a **Leste** |
| **Bit 3** | `0x08` | Parede a **Oeste** |

### Exemplos Práticos de Codificação:
* **Célula sem nenhuma parede (aberta)**: `0` (`0x00`)
* **Célula com parede apenas ao Norte**: `1` (`0x01`)
* **Célula com paredes ao Norte e a Leste**: `1 + 4 = 5` (`0x05`)
* **Célula cercada (todas as 4 paredes)**: `1 + 2 + 4 + 8 = 15` (`0x0F`)

---

## 3. Fluxo de Comandos (Python -> Arduino)

A tabela abaixo descreve as mensagens que o Host Python envia para o Arduino:

| Comando | Formato | Descrição | Comportamento Esperado no Arduino |
| :--- | :--- | :--- | :--- |
| **`INIT`** | `<INIT,N>` | Inicializa uma nova partida informando a dimensão $N$ do labirinto (ex: `8` para um labirinto 8x8). | Zera a matriz do labirinto interna, armazena `mazeSize = N`, limpa contadores e muda o estado para `STATE_RECEIVING_MAZE`. Envia `<ACK>`. |
| **`ROW`** | `<ROW,y,v0,v1,...,vN-1>` | Transmite a linha de índice $y$ (0 a $N-1$) contendo os valores de parede de cada célula em formato decimal separados por vírgula. | Armazena os valores na linha `y` da matriz global `maze[y][x]`. Envia `<ACK>`. Se todas as linhas forem recebidas, muda para `STATE_WAIT_START`. |
| **`START`** | `<START>` | Libera o Arduino para inicializar a tabela de Q-Learning e começar o treinamento e a resolução. | Inicializa a Q-table, muda o estado para `STATE_TRAINING` para treinar em episódios, e responde com `<ACK>`. |
| **`END`** | `<END,winner>` | Informa que a partida atual encerrou. O parâmetro `winner` indica quem venceu: `H` (Humano) ou `A` (Arduino). | Interrompe imediatamente qualquer treinamento ou resolução ativa, limpa estados internos e muda para `STATE_GAME_OVER`. Envia `<ACK>`. |

---

## 4. Fluxo de Comandos (Arduino -> Python)

A tabela abaixo descreve as mensagens que o Arduino envia para o Host Python:

| Comando | Formato | Descrição | Comportamento no Host (Python) |
| :--- | :--- | :--- | :--- |
| **`ACK`** | `<ACK>` | Confirmação genérica de recebimento de comandos. | Serve como controle de fluxo (*handshake*). O Host aguarda o `<ACK>` antes de enviar a próxima linha de labirinto (`ROW`) ou o comando `START` para evitar sobrecarga serial. |
| **`MOVE`** | `<MOVE,x,y>` | Informa a nova posição coordenada $(x,y)$ consolidada pelo agente de Q-Learning na trajetória ótima encontrada. | Atualiza a posição visual do cursor do Arduino na tela do computador para o usuário humano acompanhar a corrida em tempo real. |
| **`WIN`** | `<WIN>` | Sinaliza que o agente de Q-Learning do Arduino atingiu a célula de saída e concluiu o labirinto. | Declara o Arduino como vencedor da partida (caso o humano não tenha chegado antes) e dispara o comando de encerramento `<END,A>`. |

---

## 5. Máquina de Estados (FSM) no Arduino e os Comandos

A FSM do loop principal do Arduino está fortemente acoplada a este protocolo:

```
                  ┌──────────────┐
                  │  STATE_IDLE  │◄─────────────────────────────┐
                  └──────┬───────┘                              │
                         │ Recebe <INIT,N>                      │
                         ▼ (Responde <ACK>)                     │
              ┌──────────────────────┐                          │
              │ STATE_RECEIVING_MAZE │                          │
              └──────────┬───────────┘                          │
                         │ Recebe N linhas <ROW,y,...>          │
                         ▼ (Responde <ACK> a cada linha)        │
                ┌──────────────────┐                            │
                │ STATE_WAIT_START │                            │
                └────────┬─────────┘                            │
                         │ Recebe <START>                       │
                         ▼ (Responde <ACK>)                     │
                ┌──────────────────┐                            │
                │  STATE_TRAINING  ├──────────────────────────┐ │ Recebe <END,winner>
                └────────┬─────────┘                          │ │ (Responde <ACK>)
                         │ Treino Concluído                   │ │
                         ▼                                    │ │
                ┌──────────────────┐                          │ │
                │  STATE_SOLVING   ├────────────────────────┐ │ │
                └────────┬─────────┘                        │ │ │
                         │ Alcança a Saída                  │ │ │
                         ▼ (Envia <WIN>)                    ▼ ▼ │
                ┌──────────────────┐                  ┌─────────┴─┐
                │ STATE_GAME_OVER  ├─────────────────►│  Reset /  │
                └──────────────────┘                  │   IDLE    │
                                                      └───────────┘
```
