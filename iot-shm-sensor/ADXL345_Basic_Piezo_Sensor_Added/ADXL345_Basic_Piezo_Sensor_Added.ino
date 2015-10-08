 #define LOG_OUT 1 // use the log payload function
 #define FFT_N 128 // set to 256 point fft
 
//Add the SPI library so we can communicate with the ADXL345 sensor
#include <SPI.h>
#include <XBee.h>
#include <FFT.h>
#include <Time.h>
#include <Wire.h>

//Assign the Chip Select signal to pin 10.
int CS=10;

//This is a list of some of the registers available on the ADXL345.
//To learn more about these and the rest of the registers on the ADXL345, read the datasheet!
XBee xbee;

char POWER_CTL = 0x2D;	//Power Control Register
char ADXL345_BW_RATE = 0x2c;
char DATA_FORMAT = 0x31;
char DATAX0 = 0x32;	//X-Axis Data 0
char DATAX1 = 0x33;	//X-Axis Data 1
char DATAY0 = 0x34;	//Y-Axis Data 0
char DATAY1 = 0x35;	//Y-Axis Data 1
char DATAZ0 = 0x36;	//Z-Axis Data 0
char DATAZ1 = 0x37;	//Z-Axis Data 1

const int X_ACCEL = 1;
const int Y_ACCEL = 2;
const int Z_ACCEL = 3;
const int PIEZO = 4;
uint8_t X_ACCEL_ARR[] = {X_ACCEL};
uint8_t Y_ACCEL_ARR[] = {Y_ACCEL};
uint8_t Z_ACCEL_ARR[] = {Z_ACCEL};
uint8_t PIEZO_ARR[] = {PIEZO};

uint8_t accelX_input[FFT_N*2];
uint8_t accelY_input[FFT_N*2];
uint8_t accelZ_input[FFT_N*2];

const int TIME_SIZE = 4;
const int TYPE_SIZE = 1;
const int TOTAL_PAYLOAD_SIZE = TYPE_SIZE + FFT_N/2 + TIME_SIZE;

//This buffer will hold values read from the ADXL345 registers.
unsigned char values[10];

uint8_t payload[TOTAL_PAYLOAD_SIZE];
uint8_t timeArr[TIME_SIZE];
time_t currentTime;
XBeeAddress64 gatewayAddress64 = XBeeAddress64(0x00000000, 0x00000000);
ZBTxRequest zbTx = ZBTxRequest(gatewayAddress64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();


void setup(){ 
  //Initiate an SPI communication instance.
  SPI.begin();
  //Configure the SPI connection for the ADXL345.
  SPI.setDataMode(SPI_MODE3);
  //Create a serial connection to display the data on the terminal.
  Serial.begin(9600);
  xbee.setSerial(Serial);
  //Set up the Chip Select pin to be an payload from the Arduino.
  pinMode(CS, OUTPUT);
  //Before communication starts, the Chip Select pin needs to be set high.
  digitalWrite(CS, HIGH);
  
  //Put the ADXL345 into +/- 4G range by writing the value 0x01 to the DATA_FORMAT register.
  writeRegister(DATA_FORMAT, 0x01);
  //Put the ADXL345 into Measurement Mode by writing 0x08 to the POWER_CTL register.
  writeRegister(POWER_CTL, 0x08);  //Measurement mode  int xarr[FFT_N];
  for(int i = 0; i < FFT_N*2; i+=2) {
    fft_input[i+1] = 0;
  }
  setRate(1600.0);
}

void updateTime() {
  currentTime = now();
  timeArr[0] = currentTime & 0xFF;
  timeArr[1] = currentTime >> 8 & 0xFF;
  timeArr[2] = currentTime >> 16 & 0xFF;
  timeArr[3] = currentTime >> 24 & 0xFF;
}

void updateFFTInputs() {
  
}

void updateFFTInput(uint8_t* accel_type_arr) {
  memcpy(&payload[FFT_N/2 + TIME_SIZE], accel_type_arr, TYPE_SIZE);
  uint8_t accel_type = accel_type_arr[0];
  switch(accel_type) {
    case X_ACCEL:
      for(int i = 0; i < FFT_N*2; i += 2) {
        readRegister(DATAX0, 6, values);
        fft_input[i] = getXReading(values);
        fft_input[i+1] = 0; // set odd bins to 0
      }
      break;
    case Y_ACCEL:
      for(int i = 0; i < FFT_N*2; i += 2) {
        readRegister(DATAX0, 6, values);
        fft_input[i] = getYReading(values);
        fft_input[i+1] = 0; // set odd bins to 0
      }
      break;
    case Z_ACCEL:
      for(int i = 0; i < FFT_N*2; i += 2) {
        readRegister(DATAX0, 6, values);
        fft_input[i] = getZReading(values);
        fft_input[i+1] = 0; // set odd bins to 0
      }
      break;
    case PIEZO:
      for(int i = 0; i < FFT_N*2; i+=2) {
        fft_input[i] = getPReading(values); //current piezo reading
        fft_input[i+1] = 0; 
      }
  }
  fft_window(); // window the data for better frequency response
  fft_reorder(); // reorder the data before doing the fft
  fft_run(); // process the data in the fft
  fft_mag_log(); // take the payload of the fft
  sei(); // turn interrupts back on
}

int getXReading(unsigned char* reading) {
   return ((int)reading[1]<<8)|(int)reading[0];
}

int getYReading(unsigned char* reading) {
   return ((int)reading[3]<<8)|(int)reading[2];
}

int getZReading(unsigned char* reading) {
   return ((int)reading[5]<<8)|(int)reading[4];
}

int getPReading(unsigned char* reading){
    return((int)analogRead(A0));
}

void updatePayload(uint8_t* type) {
  memcpy(&payload[FFT_N/2 + TIME_SIZE], type, TYPE_SIZE);
  updateTime();
  memcpy(&payload[0], timeArr, TIME_SIZE);
  updateFFTInput(type);
  memcpy(&payload[TIME_SIZE], fft_log_out, FFT_N/2);
}

void loop(){
  updatePayload(X_ACCEL_ARR);
  xbee.send(zbTx);
  delay(1000);


  updatePayload(Y_ACCEL_ARR);
  xbee.send(zbTx);
  delay(1000);

  updatePayload(Z_ACCEL_ARR);
  xbee.send(zbTx);
  delay(1000);
  
  updatePayload(PIEZO_ARR);
  xbee.send(zbTx);
  delay(1000);
}

//This function will write a value to a register on the ADXL345.
//Parameters:
//  char registerAddress - The register to write a value to
//  char value - The value to be written to the specified register.
void writeRegister(char registerAddress, char value){
  //Set Chip Select pin low to signal the beginning of an SPI packet.
  digitalWrite(CS, LOW);
  //Transfer the register address over SPI.
  SPI.transfer(registerAddress);
  //Transfer the desired register value over SPI.
  SPI.transfer(value);
  //Set the Chip Select pin high to signal the end of an SPI packet.
  digitalWrite(CS, HIGH);
}

//This function will read a certain number of registers starting from a specified address and store their values in a buffer.
//Parameters:
//  char registerAddress - The register addresse to start the read sequence from.
//  int numBytes - The number of registers that should be read.
//  char * values - A pointer to a buffer where the results of the operation should be stored.
void readRegister(char registerAddress, int numBytes, unsigned char * values){
  //Since we're performing a read operation, the most significant bit of the register address should be set.
  char address = 0x80 | registerAddress;
  //If we're doing a multi-byte read, bit 6 needs to be set as well.
  if(numBytes > 1)address = address | 0x40;
  
  //Set the Chip select pin low to start an SPI packet.
  digitalWrite(CS, LOW);
  //Transfer the starting register address that needs to be read.
  SPI.transfer(address);
  //Continue to read registers until we've read the number specified, storing the results to the input buffer.
  for(int i=0; i<numBytes; i++){
    values[i] = SPI.transfer(0x00);
  }
  //Set the Chips Select pin high to end the SPI packet.
  digitalWrite(CS, HIGH);
}

void setRate(double rate){
  byte _b,_s;
  int v = (int) (rate / 6.25);
  int r = 0;
  while (v >>= 1)
  {
    r++;
  }
  if (r <= 9) { 
    readRegister(ADXL345_BW_RATE, 1, &_b);
    _s = (byte) (r + 6) | (_b & B11110000);
    writeRegister(ADXL345_BW_RATE, _s);
  }
}

void readAccel(int *x, int *y, int *z) {
  readRegister(DATAX0, 6, values); //read the acceleration data from the ADXL345
  // each axis reading comes in 10 bit resolution, ie 2 bytes.  Least Significat Byte first!!
  // thus we are converting both bytes in to one int
  *x = (((int)values[1]) << 8) | values[0];   
  *y = (((int)values[3]) << 8) | values[2];
  *z = (((int)values[5]) << 8) | values[4];
}
