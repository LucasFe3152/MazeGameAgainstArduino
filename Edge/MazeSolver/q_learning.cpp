#include "q_learning.h"

QLearningAgent agent;

int8_t reward;
int8_t dumpRate = 10;

QLearningAgent::QLearningAgent() {
}

void QLearningAgent::init() {
    // TODO: Initialize Q-table
    agentX = 0;
    agentY = 0;
    exitX = mazeSize-1;
    exitY = mazeSize-1;
    epsilon = 100;
    dumpRate = 0;
    episodesTrained = 0;
    memset(qTable, 0, sizeof(qTable));
}

void QLearningAgent::trainEpisodes(uint8_t n) {
    for (uint8_t episode=0; episode<n; episode++){
        resetAgent(true); // Treina com Exploring Starts (posição aleatória)
        for (int i = 0; i < TRAINING_STEPS; i++) {
            int8_t randNumber = random(0, 100);

            if (randNumber < epsilon) {
                currentAction = getRandomAction();
            }else {
                currentAction = chooseBestMove(agentX, agentY);
            }

            int8_t currentX = agentX, currentY = agentY;

            getNextState(currentX, currentY, currentAction, agentX, agentY);

            reward = getReward(currentX, currentY, currentAction);

            int16_t targetQ = reward + (getMaxQ(agentX, agentY) * gama) / 16;
            int16_t currentQ = qTable[currentY][currentX][currentAction];
            int16_t newQ = currentQ + (targetQ - currentQ) / alpha;
            if (newQ > 120) newQ = 120;
            if (newQ < -120) newQ = -120;
            qTable[currentY][currentX][currentAction] = newQ;

            if (agentX == exitX && agentY == exitY) 
                break;
        }

        if (epsilon > 10) {
            epsilon = (epsilon * 98) / 100;
            if (epsilon < 10) {
                epsilon = 10;
            }
        }

        episodesTrained++;

        if (episodesTrained >= MAX_TRAINING_EPISODES) {
            startSolving();
            return;
        }

    }
}

bool QLearningAgent::solveStep() {
    int8_t action = chooseBestMove(agentX, agentY);
    int8_t nextX, nextY;
    getNextState(agentX, agentY, action, nextX, nextY);
    agentX = nextX;
    agentY = nextY;
    sendMove(agentX, agentY);

    return agentX == exitX && agentY == exitY;
}

void QLearningAgent::startSolving() {
    finishTraining();
    resetAgent();
}

void QLearningAgent::sendMove(int8_t x, int8_t y) {
    Serial.print("<MOVE,");
    Serial.print(x);
    Serial.print(",");
    Serial.print(y);
    Serial.println(">");
}

void QLearningAgent::resetAgent(bool randomStart) {
    if (randomStart && mazeSize > 1) {
        do {
            agentX = random(0, mazeSize);
            agentY = random(0, mazeSize);
        } while (agentX == exitX && agentY == exitY);
    } else {
        agentX = 0;
        agentY = 0;
    }
}

bool QLearningAgent::isValidMove(int8_t currentX, int8_t currentY, int8_t action) {
    if (action == NORTH && currentY <= 0) return false;              // Norte                                                                                                
    if (action == SOUTH && currentY >= mazeSize - 1) return false;   // Sul                                                                                                  
    if (action == EAST && currentX >= mazeSize - 1) return false;   // Leste                                                                                                
    if (action == WEST && currentX <= 0) return false;              // Oeste                                                                                                
                                                                                                                                                                    
    uint8_t cell = maze[currentY][currentX];                                                                                                                                    
    if (action == NORTH && (cell & WALL_NORTH)) return false;                                                                                                         
    if (action == SOUTH && (cell & WALL_SOUTH)) return false;                                                                                                         
    if (action == EAST && (cell & WALL_EAST)) return false;                                                                                                          
    if (action == WEST && (cell & WALL_WEST)) return false;                                                                                                          
                                                                                                                                                                    
    return true; // Caminho livre        
}

int8_t QLearningAgent::getReward(int8_t x, int8_t y, int8_t action) {
    if (isValidMove(x, y, action)) {
        int8_t nextX, nextY;
        getNextState(x, y, action, nextX, nextY);
        if (nextX == exitX && nextY == exitY)
            return REWARD_EXIT;
        else
            return REWARD_STEP;
    }else {
        return REWARD_COLISION;
    }
}

void QLearningAgent::getNextState(int8_t currentX, int8_t currentY, int8_t action, int8_t &nextX, int8_t &nextY) {
    nextX = currentX;
    nextY = currentY;
    if (isValidMove(currentX, currentY, action)) {
        if (action == NORTH)
            nextY--;
        else if (action == SOUTH)
            nextY++;
        else if (action == EAST)
            nextX++;
        else
            nextX--;
    }
}

int8_t QLearningAgent::getMaxQ(int8_t x, int8_t y) {
    if (x<0 || y<0 || x>=mazeSize || y>=mazeSize) {
        return 0;
    }

    int8_t maxVal = qTable[y][x][0];

    for (int i=1; i<4; i++) {
        if (qTable[y][x][i] > maxVal)
            maxVal = qTable[y][x][i];
    }

    return maxVal;
}

int8_t QLearningAgent::chooseBestMove(int8_t x, int8_t y) {
    int8_t maxVal = qTable[y][x][0];
    int8_t bestAction = 0;

    for (int i=1; i<4; i++) {
        if (qTable[y][x][i] > maxVal) {
            maxVal = qTable[y][x][i];
            bestAction = i;
        }
    }

    return static_cast<AgentActions>(bestAction);
}

AgentActions QLearningAgent::getRandomAction() {
    int8_t n = random(0, 4);
    return static_cast<AgentActions>(n);
}


