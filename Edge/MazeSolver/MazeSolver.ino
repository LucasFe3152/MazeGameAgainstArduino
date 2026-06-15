#include "maze_protocol.h"
#include "q_learning.h"

void setup() {
  Serial.begin(115200);
  // TODO: Initialize game state
}

void loop() {
  // TODO: Handle serial communication and Q-learning steps
  handleSerial();
}
