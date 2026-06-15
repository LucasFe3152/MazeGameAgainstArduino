#ifndef MAZE_PROTOCOL_H
#define MAZE_PROTOCOL_H

#include <Arduino.h>

// Bit masks for walls
#define WALL_NORTH 0x01
#define WALL_SOUTH 0x02
#define WALL_EAST  0x04
#define WALL_WEST  0x08

void handleSerial();

#endif
