#include "do_surveyor.h"
// Connect the DO probes at A0-A8
Surveyor_DO DO_Probes[8]= {
  Surveyor_DO(A0),
  Surveyor_DO(A1),
  Surveyor_DO(A2),
  Surveyor_DO(A3),
  Surveyor_DO(A4),
  Surveyor_DO(A5),
  Surveyor_DO(A6),
  Surveyor_DO(A7)
}

// Define probe/pump control pins
const int lsbDevBit = 2;  //D2
const int midDevBit = 3; //D3
const int msbDevBit = 4;  //D4
const int devEnable = 5; //D5

// Track current device
int curDevice = 0;

uint8_t user_bytes_received = 0;
const uint8_t bufferlen = 32;
char user_data[bufferlen];

void parse_cmd(char* string) {
  strupr(string);
  String cmd = String(string);

  // Calibration command code from ATLAS DO library
  if(cmd.startsWith("CAL")){
    int index = cmd.indexOf(',');
    if(index != -1){
      String param = cmd.substring(index+1, cmd.length());
      if(param.equals("CLEAR")){
        DO.cal_clear();
        Serial.println("CALIBRATION CLEARED");
      }
    }
    else{
      DO.cal();
      Serial.println("DO CALIBRATED");
    }
  }
  // Pump command code 
  //  Enabling pumps
  else if (cmd.startsWith("next")) {
    int index = cmd.indexOf('-');
    if (index != -1) {
      String dev = cmd.substring(index+1, cmd.length());

      curDevice = dev.toInt();

      // Turn off power to controller
      digitalWrite(devEnable, LOW);

      // Update control bits
      digitalWrite(lsbDevBit, bitRead(curDevice, 0));
      digitalWrite(midDevBit, bitRead(curDevice, 1));
      digitalWrite(msbDevBit, bitRead(curDevice, 2));

      // Enable device controller
      digitalWrite(devEnable, HIGH);
    }
  }
}

void setup() {
  // Set device control pins to output
  pinMode(lsbDevBit, OUTPUT);
  pinMode(midDevBit, OUTPUT);
  pinMode(msbDevBit, OUTPUT);
  pinMode(devEnable, OUTPUT);

  Serial.begin(9600);
  delay(200);
  // Serial.println(F("Use command \"CAL\" to calibrate the circuit to 100% saturation in air\n\"CAL,CLEAR\" clears the calibration"));

  // Enable probe communications
  for (int i = 0; i < 8; i++) {
    DO_Probes[i].begin();
  }
  // if(!DO_0.begin()){
  //   Serial.println("Error starting probe 0");
  // }
  // if(!DO_1.begin()){
  //   Serial.println("Error starting probe 1");
  // }
  // if(!DO_2.begin()){
  //   Serial.println("Error starting probe 2");
  // }
  // if(!DO_3.begin()){
  //   Serial.println("Error starting probe 3");
  // }
  // if(!DO_4.begin()){
  //   Serial.println("Error starting probe 4");
  // }
  // if(!DO_5.begin()){
  //   Serial.println("Error starting probe 5");
  // }
  // if(!DO_6.begin()){
  //   Serial.println("Error starting probe 6");
  // }
  // if(!DO_7.begin()){
  //   Serial.println("Error starting probe 7");
  // }
}

void loop() {
  if (Serial.available() > 0) {
    user_bytes_received = Serial.readBytesUntil(13, user_data, sizeof(user_data));
  }

  if (user_bytes_received) {
    parse_cmd(user_data);
    user_bytes_received = 0;
    memset(user_data, 0, sizeof(user_data));
  }
  
  Serial.println(DO_Probes[curDevice].read_do_percentage());
  delay(1000);
}