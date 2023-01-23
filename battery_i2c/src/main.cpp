#include<Arduino.h>
#include <Wire.h>

void setup() {
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(115200);  // start serial for output
  // LED 
  pinMode(13, OUTPUT);
  
}

void out_values(byte regAddress, byte devAddress, byte arrLen)
{
  byte dataVal[arrLen];
  Wire.beginTransmission(devAddress);
  //Add the one byte register address
  Wire.write(regAddress);
  //Send out buffer and log response
  byte ack = Wire.endTransmission();

  //If data is ackowledged, proceed
  if( ack == 0 ){
    //Request a number of bytes from the device address
    Wire.requestFrom( devAddress , arrLen);
    //If there is data in the in buffer
    delay(100);
    if( Wire.available() > 0 ){
      //Cycle through, loading data into array
      for( uint8_t i = 0; i < arrLen; i++ ){
        //dataVal[i] = Wire.read();
        char c = Wire.read();
        Serial.print(c);
      }
    }
  }

}


void read_all(byte devAddress)
{

  uint8_t bytes_requested[43] = {2,2,2,2,2,2,1,2,2,2,2,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,4,4,4,4,4,4,4,4};

  //  ,0x20 ,0x21 ,0x22 ,0x2F,
  // uint8_t bytes_requested[47] = {2,2,2,2,2,2,1,2,2,2,2,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,21,21,5,21,2,2,2,2,2,2,1,4,4,4,4,4,4,4,4};

  byte registers[43] = {0x01 ,0x02 ,0x03 ,0x04 ,0x05 ,0x06 ,0x07 ,0x08 ,0x09 ,0x0A ,0x0B ,0x0C ,0x0D ,0x0E ,0x0F ,0x10,
                      0x11 ,0x12 ,0x13 ,0x14 ,0x15 ,0x16 ,0x17 ,0x18 ,0x19 ,0x1A ,0x1B ,0x1C,
                      0x3C ,0x3D ,0x3E ,0x3F ,0x4A ,0x4B ,0x4F ,0x50 ,0x51 ,0x52 ,0x53 ,0x54 ,0x55 ,0x56 ,0x57};
  //  ,0x20 ,0x21 ,0x22 ,0x2F,

  int len_reg = 43;//= sizeof(registers)/sizeof(registers[0]);

  int total_bytes = 0;
  for (int i = 0; i < len_reg; i++) {
    total_bytes += bytes_requested[i];
  }

  char dataVal[total_bytes];

  // for i from 0 to len_reg
  for (uint8_t i = 0; i < len_reg; i++) {
    Wire.beginTransmission(devAddress);
    //Add the one byte register address
    Wire.write(registers[i]);
    //Send out buffer and log response
    byte ack = Wire.endTransmission();

    //If data is ackowledged, proceed
    if( ack == 0 )
    {
      //Request a number of bytes from the device address
      Wire.requestFrom( devAddress ,  (int16_t)bytes_requested[i]);
      //If there is data in the in buffer
      delay(10);
      if( Wire.available() > 0 ){
        //Cycle through, loading data into array
        for( uint8_t i = 0; i < bytes_requested[i]; i++ ){
          //dataVal[i] = Wire.read();
          char c = Wire.read();
          //dataVal[i] = c;
          Serial.print(c);
          delay(10);
        }
      }
    }
  }
  // send out data
  for (int i = 0; i < total_bytes; i++) {
    digitalWrite(13, HIGH);
    Serial.print(dataVal[i]);
    // toggke LED
    digitalWrite(13, LOW);
  }
}


void loop() {
  byte devAddress = 0x0B; // device address
  digitalWrite(13, HIGH);
  if (Serial.read() == 1) {
      // byte regAddress = Serial.read(); fyrir single byte lesningu
      digitalWrite(13, LOW);
      delay(100);
      read_all(devAddress);
      //out_values(regAddress, devAddress, arrLen);
      
    }
  
}