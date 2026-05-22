#include <SoftwareSerial.h>

#define bluetoothTX 5
#define bluetoothRX 6

String photo_command = "photo\n";
SoftwareSerial hc05(bluetoothTX, bluetoothRX);

void setupSerial(){
  Serial.begin(9600);
}

bool setupBluetooth() {
  hc05.begin(38400);
  return true;
}

void setup() {
  setupSerial();
  if (setupBluetooth()) Serial.println("Bluetooth Ready");
}

void loop() {
  hc05.println("Hello from Arduino");
  delay(1000);
}