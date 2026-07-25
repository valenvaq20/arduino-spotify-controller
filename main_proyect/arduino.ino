const int pin10 = 10;
const int pin11 = 11;
const int pin12 = 12;
const int pin13 = 13;

bool estadoAnterior10 = HIGH;
bool estadoAnterior11 = HIGH;
bool estadoAnterior12 = HIGH;
bool estadoAnterior13 = HIGH;

void setup() {
  Serial.begin(9600);

  pinMode(pin10, INPUT_PULLUP);
  pinMode(pin11, INPUT_PULLUP);
  pinMode(pin12, INPUT_PULLUP);
  pinMode(pin13, INPUT_PULLUP);
}

void loop() {
  bool estado10 = digitalRead(pin10);
  bool estado11 = digitalRead(pin11);
  bool estado12 = digitalRead(pin12);
  bool estado13 = digitalRead(pin13);

  if (estadoAnterior10 == HIGH && estado10 == LOW) {
    Serial.println("10");
  }

  if (estadoAnterior11 == HIGH && estado11 == LOW) {
    Serial.println("11");
  }

  if (estadoAnterior12 == HIGH && estado12 == LOW) {
    Serial.println("12");
  }

  if (estadoAnterior13 == HIGH && estado13 == LOW) {
    Serial.println("13");
  }

  estadoAnterior10 = estado10;
  estadoAnterior11 = estado11;
  estadoAnterior12 = estado12;
  estadoAnterior13 = estado13;

  delay(20); // Pequeño antirrebote
}
