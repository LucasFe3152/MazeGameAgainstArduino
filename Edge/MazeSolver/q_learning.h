#ifndef Q_LEARNING_H
#define Q_LEARNING_H

#include <Arduino.h>

// TODO: Define Q-learning parameters and structures
// Use int8_t/uint8_t for Q-table as per constraints

class QLearningAgent {
public:
    QLearningAgent();
    void init();
    void step();
};

#endif
