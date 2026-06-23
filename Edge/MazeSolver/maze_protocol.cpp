#include "maze_protocol.h"
#include "q_learning.h"

int8_t currentState = STATE_IDLE;

int8_t mazeSize;
int8_t maze[MAX_MAZE_SIZE][MAX_MAZE_SIZE];
int8_t currentRow;

uint8_t rxIndex;
char rxBuffer[256];

bool recvActive = false;

void handleSerial() {
    while (Serial.available() > 0) {
        char c = Serial.read();

        switch(c) {
            case '<':
                recvActive = true;
                rxIndex = 0;
                break;
            case '>':
                if (recvActive) {
                    rxBuffer[rxIndex] = '\0';
                    recvActive = false;
                    parseCommand(rxBuffer);
                }
                break;
            default:
                if (recvActive && (rxIndex < (sizeof(rxBuffer)-1))) {
                    rxBuffer[rxIndex++] = c;
                }
        }
    }
}

void parseCommand(char* packet) {                                                                                                                                 
        char* savePtr;                                                                                                                                                
        char* cmd = strtok_r(packet, ",", &savePtr);                                                                                                                  
                                                                                                                                                                      
        if (cmd == NULL) return;                                                                                                                                      
                                                                                                                                                                      
        if (strcmp(cmd, "INIT") == 0) {               
            char* sizeToken = strtok_r(NULL, ",", &savePtr);
            if (sizeToken) {
                int8_t n = atoi(sizeToken);
                initGame(n);                                                                                                                                     
            }
        }                                                                                                                                                             
        else if (strcmp(cmd, "ROW") == 0) {                                                                                                                           
            char* yToken = strtok_r(NULL, ",", &savePtr);
            if (yToken) {
                currentRow = atoi(yToken);
                for (int8_t i=0; i<mazeSize; i++) {
                    char* n = strtok_r(NULL, ",", &savePtr);
                    if (n) {
                        maze[currentRow][i] = atoi(n);                                                                                                                                  
                    }
                }
                Serial.println("<ACK>");
                if (currentRow == mazeSize-1) {
                    finishReceiving();
                }
            }
        }                                                                                                                                                             
        else if (strcmp(cmd, "START") == 0) {                                                                                                                         
            startGame();                                                                                                                                        
        }                                                                                                                                                             
        else if (strcmp(cmd, "END") == 0) {                                                                                                                           
            char* winnertToken = strtok_r(NULL, ",", &savePtr);
            finishGame();                                                                                                                      
        }                                                                                                                                                             
}   

void initGame(int8_t n) {
    Serial.println("Mudei de estado para RECEIVING_MAZE");
    
    if (n > MAX_MAZE_SIZE) {
        n = MAX_MAZE_SIZE;
    }

    memset(maze, 0, sizeof(maze));
    mazeSize = n;
    currentState = STATE_RECEIVING_MAZE;
    Serial.println("<ACK>");
}

void finishReceiving() {
    currentState = STATE_WAIT_START;
    Serial.println("Mudei de estado para WAIT_START");
    printMaze();
}

void printMaze() {
    for (int8_t i=0; i<mazeSize; i++) {
        for (int8_t j=0; j<mazeSize; j++) {
            Serial.print(maze[i][j]);
            Serial.print(" ");
        } 
        Serial.println("");
    }
}

void startGame() {
    Serial.println("Mudei de estado para TRAINING");
    currentState = STATE_TRAINING;
    Serial.println("<ACK>");
    agent.init();
}

void finishTraining() {
    currentState = STATE_SOLVING;
    Serial.println("Mudei de estado para SOLVING");
}

void finishGame() {
    currentState = STATE_GAME_OVER; 
    Serial.println("Mudei de estado para GAME_OVER");
}