#include <Servo.h>
Servo wing;

void setup() {
  pinMode(2, OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(6,OUTPUT);
  Serial.begin(115200);
  wing.attach(6);

}

void loop() {
  if (Serial.available() > 0){
    int msg = Serial.parseInt();

    if (msg == 0){
      digitalWrite(3, HIGH);
      digitalWrite(2, LOW);
      wing.write(60);
    }

    if (msg == 1){
      digitalWrite(2, HIGH);
      digitalWrite(3, LOW);
      wing.write(120);
    }
  }
  else if (Serial.available() == 0){
    digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      wing.write(60);
      digitalWrite(6, LOW);
  }

}
