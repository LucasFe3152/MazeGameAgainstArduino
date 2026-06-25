#include "maze_protocol.h"
#include "q_learning.h"

#define MAX_DELTA 250
#define TRAINING_EPISODES 5

char currentMove;

unsigned long int lastTime = 0, currentTime;

bool finishedGame = false;
bool canMove = true;

void restartGame();

void setup() {
  Serial.begin(115200);
  currentState = STATE_IDLE;
}

void loop() {


  // Delay não bloqueante de 2 segundos para o print
  currentTime = millis();
  if ((currentTime - lastTime) > MAX_DELTA) {
    lastTime = currentTime;
    Serial.print("Estado atual: ");
    Serial.println(currentState);
    canMove = true;
  }

  switch (currentState) {
    case (STATE_IDLE):
      handleSerial();
      break;
    case (STATE_RECEIVING_MAZE):
      handleSerial();
      break;
    case (STATE_WAIT_START):
      handleSerial();
      break;
    case (STATE_TRAINING):
      agent.trainEpisodes(TRAINING_EPISODES);
      handleSerial();
      break;
    case (STATE_SOLVING):
      if (canMove) {
        canMove = false;
        finishedGame = agent.solveStep();
        if (finishedGame) {
          Serial.println("<WIN>");
          currentState = STATE_GAME_OVER;
        }
        handleSerial();
      }
      break;
    case (STATE_GAME_OVER):
      restartGame();
      handleSerial();
      break;
  }
}

void restartGame() {
  finishedGame = false;
  currentState = STATE_IDLE;
}
