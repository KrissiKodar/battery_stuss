// i2c device at address 0x0B

// read from i2c device at address 0x0B, from register 0x09

// Wire Master Reader
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Reads data from an I2C/TWI slave device
// Refer to the "Wire Slave Sender" example for use with this

// Created 29 March 2006

// This example code is in the public domain.

#include<Arduino.h>
#include <Wire.h>

void setup() {
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(9600);  // start serial for output
  // LED 
  pinMode(13, OUTPUT);
}

void print_data(byte data[], int len) {
  // print the data as 1 16-bit integer
  //for (int i = 0; i < len; i++) {
  //  Serial.print(data[i], HEX);
  //  Serial.print(" ");
  //}
  // data is little endian, flip the bytes around
  for (int i = len - 1; i >= 0; i--) {
    Serial.print(data[i], HEX);
    //Serial.print(" ");
  }
  //Serial.print("= ");
  // also print out converted to one 16-bit integer in decimal
  //uint16_t val = data[0] << 8 | data[1];
  // data is little endian, so shift the first byte 8 bits to the left
  //uint16_t val = data[0] | data[1] << 8;
  //Serial.print(val);
}

// output values to serial



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
    Wire.requestFrom( devAddress , (int16_t) arrLen );
    //If there is data in the in buffer
    if( Wire.available() > 0 ){
      //Cycle through, loading data into array
      for( uint8_t i = 0; i < arrLen; i++ ){
        dataVal[i] = Wire.read();
      }
    }
  }
  print_data(dataVal, arrLen);
}


// read all registers 0x01 to 0x1C,
// and output the values to serial
void read_all_registers() {
  byte devAddress = 0x0B; // device address
  byte regAddress = 0x01; // register address
  byte arrLen = 2; // number of bytes to read
  for (int i = 0; i < 28; i++) {
    out_values(regAddress, devAddress, arrLen);
    delay(100);
    regAddress++;
  }
}


void loop() {
  byte devAddress = 0x0B; // device address
  byte arrLen = 2;
  // wait for serial command from user
  // the serial command will be the register address
  // the program should then write out the data from that register

  if (Serial.available() > 0) {
      byte regAddress = Serial.read();
      digitalWrite(13, HIGH);
      delay(100);
      read_all_registers();
      //out_values(regAddress, devAddress, arrLen);
      digitalWrite(13, LOW);
    }
  
}