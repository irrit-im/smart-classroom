#include <SoftwareSerial.h> // importing UART library for bluetooth
#include <VoiceRecognitionV3.h> // voice recognition module library
 
#define R_PIN 10 // RGB LED pins
#define G_PIN 9
#define B_PIN 8

#define xAxisPin A1 // Joystick pins
#define yAxisPin A0
#define joystickButtonPin 4

#define bluetoothRX 5 // Bluetooth pins
#define bluetoothTX 6

#define voiceRecognitionRX 2 // Voice recognition pins
#define voiceRecognitionTX 3
#define voiceCommandCount 3 // Number of voice commands stored in the system
 
String photo_command = "photo\n"; // BT to Raspberry
 
// BT
SoftwareSerial hc05(bluetoothRX, bluetoothTX); // Bluetooth object creation
 
// VR module
VR myVR(voiceRecognitionRX, voiceRecognitionTX); // Voice recognition object creation
uint8_t records[voiceCommandCount]; //Array of VR module commands that get uploaded to the code
uint8_t buf[64]; // Buffer to store recognition results
 
// Joystick position
int xPlace;
int yPlace;
 
void setupSerial(){
  Serial.begin(9600); // Start serial communication with computer
}
 
bool setupBluetooth() {
  hc05.begin(38400); // Start serial communication with BT
  return true; // Return success
}
 
void setupVoiceRecognition(){
  myVR.begin(9600); //Start serial communication with VR module
  if (myVR.clear() == 0) { // Check if module responds
    Serial.println("VR Module ready");
  } else {
    Serial.println("VR Module not found or error");
    while (1); // Stop execution if module is not detected
  }
 
// Load the command list
  records[0] = 0; // "צלם"
  records[1] = 1; // "On"
  records[2] = 2; // דו 4
 
  for (int i = 0; i < voiceCommandCount; i++) { // Loading commands into module memory
    if (myVR.load(records[i]) >= 0) { // Checks if record can be loaded
      Serial.print("Loaded record ");
      Serial.println(records[i]);
    } else {
      Serial.print("Cannot load record "); // Updates if a command was not loaded
      Serial.println(records[i]);
    }
  }
}
 
void setupRGB(){
  pinMode(R_PIN, OUTPUT); // Setting RGB light pins as output
  pinMode(G_PIN, OUTPUT);
  pinMode(B_PIN, OUTPUT);
  digitalWrite(R_PIN, LOW); // Turns off the RGB light at the beginning of the program
  digitalWrite(G_PIN, LOW);
  digitalWrite(B_PIN, LOW);
}
 
void setup() {
  pinMode(joystickButtonPin, INPUT);
  setupSerial();
  if (setupBluetooth()) Serial.println("Bluetooth Ready"); //Make sure the BT can connect
  setupVoiceRecognition();
  setupRGB(); 
}
 
void readJoystick(){
  xPlace = map(analogRead(xAxisPin),0,874,0,100); // Converts joystick values ​​from a range of 0-874 to 0 to 100
  yPlace = map(analogRead(yAxisPin),0,874,0,100);
}
 
void sendJoystickBluetooth() {
  hc05.print(xPlace); // Sends joystick values
  hc05.print(",");
  hc05.print(yPlace);
  hc05.print("\n");
}
 
void blinkLEDColor(String color) {
  if (color == "purple") {
    digitalWrite(R_PIN, HIGH); // Color purple = red + blue
    digitalWrite(G_PIN, LOW);
    digitalWrite(B_PIN, HIGH);
  }
  delay(1000); // Light on for a second
  digitalWrite(R_PIN, LOW); // Turn off RGB LED
  digitalWrite(G_PIN, LOW);
  digitalWrite(B_PIN, LOW);
}
 
void handleVoiceCommand() {
  int recognized = myVR.recognize(buf, 50); // Attempts to recognize a voice command and stores the result in buf
  if (recognized > 0) { // Checks if a command that was loaded into the code was found
    int command = buf[1]; // Extracts recognized command ID from buf
    Serial.print("Command detected: ");
    Serial.println(command);
 
    if (command >= 0) { // If a valid command was found
      hc05.println(photo_command); // Send photo command to Raspberry Pi
      blinkLEDColor("purple"); // Turn on RGB LED
    }
  }
}
 
void loop() { // Runs the program
  readJoystick();
  if (digitalRead(joystickButtonPin)==LOW) sendJoystickBluetooth();
  handleVoiceCommand();
  delay(20); // 50Hz update rate
}
