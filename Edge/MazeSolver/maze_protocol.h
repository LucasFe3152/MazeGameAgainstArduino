#ifndef MAZE_PROTOCOL_H
#define MAZE_PROTOCOL_H

#include <Arduino.h>

// Bit masks for walls
#define WALL_NORTH 0x01
#define WALL_SOUTH 0x02
#define WALL_EAST  0x04
#define WALL_WEST  0x08

#define MAX_MAZE_SIZE 12

enum State {
      STATE_IDLE,
      STATE_RECEIVING_MAZE,
      STATE_WAIT_START,
      STATE_TRAINING,
      STATE_SOLVING,
      STATE_GAME_OVER
};

extern int8_t currentState;

extern int8_t mazeSize;
extern int8_t maze[MAX_MAZE_SIZE][MAX_MAZE_SIZE];


void initGame(int8_t n);                                                                                                                                              
void parseCommand(char* packet);  
void handleSerial();
void finishReceiving();
void printMaze();
void startGame();
void finishTraining();
void finishGame();

#endif
