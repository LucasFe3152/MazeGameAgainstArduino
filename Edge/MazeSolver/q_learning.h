#ifndef Q_LEARNING_H
#define Q_LEARNING_H

#include <Arduino.h>
#include "maze_protocol.h"

#define REWARD_COLISION -40
#define REWARD_EXIT 120
#define REWARD_STEP -1

#define TRAINING_STEPS 150
#define MAX_TRAINING_EPISODES 350

enum AgentActions {
    NORTH,
    SOUTH,
    EAST,
    WEST
};


class QLearningAgent {
    private:                                                                                                                                                         
        int8_t qTable[MAX_MAZE_SIZE][MAX_MAZE_SIZE][4]; // Matriz Q estática                                                                                          
        int8_t agentX;                                                                                                                                                
        int8_t agentY;
        
        int8_t exitX;                                                                                                                                                
        int8_t exitY;     
        
        int8_t currentAction;

        uint16_t episodesTrained;

        int8_t epsilon;
        int8_t gama = 1;
        int8_t alpha = 1;

        bool isValidMove(int8_t x, int8_t y, int8_t action);
        void getNextState(int8_t x, int8_t y, int8_t action, int8_t &nextX, int8_t &nextY);
        int8_t getMaxQ(int8_t x, int8_t y);
        int8_t getReward(int8_t x, int8_t y, int8_t action);
        void sendMove(int8_t x, int8_t y) ;
        AgentActions getRandomAction();

    public:
        QLearningAgent();
        void init();
        void trainEpisodes(uint8_t n);
        void resetAgent(bool randomStart = false);
        int8_t chooseBestMove(int8_t x, int8_t y);

        void startSolving();
        bool solveStep();
    };

extern QLearningAgent agent;

#endif
