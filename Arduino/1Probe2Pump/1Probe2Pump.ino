#include "do_surveyor.h"
// Connect the DO probe at A0
Surveyor_DO DO = Surveyor_DO(A0);

// Define Pump control pins
const int agitationPump = 15; //AKA A1
const int aerationPump = 16;  //AKA A0

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
  else if (cmd.startsWith("EnablePump")) {
    int index = cmd.indexOf('-');
    if (index != -1) {
      String pump = cmd.substring(index+1, cmd.length());

      if(pump.equals("0")) {
        // Enable pump 0 / agitation pump
        digitalWrite(agitationPump, HIGH)
      }
      else if(pump.equals("1")) {
        // Enable pump 1 / aeration pump
        digitalWrite(aerationPump, HIGH)
      }
    }
  }
  else if (cmd.startsWith("DisablePump")) {
    int index = cmd.indexOf('-');
    if (index != -1) {
      String pump = cmd.substring(index+1, cmd.length());

      if(pump.equals("0")) {
        // Disable pump 0 / agitation pump
        digitalWrite(agitationPump, LOW)
      }
      else if(pump.equals("1")) {
        // Disable pump 1 / aeration pump
        digitalWrite(aerationPump, LOW)
      }
    }
  }
}

void setup() {
  // Set pump control pins to output
  pinMode(agitationPump, OUTPUT);
  pinMode(aerationPump, OUTPUT);

  Serial.begin(9600);
  delay(200);
  // Serial.println(F("Use command \"CAL\" to calibrate the circuit to 100% saturation in air\n\"CAL,CLEAR\" clears the calibration"));
  if(DO.begin()){
    // Serial.println("Loaded EEPROM");
  }
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
  
  Serial.println(DO.read_do_percentage());
  delay(1000);
}