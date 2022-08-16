/*********
  ROBOTIS Summer 2022 Collaboration Project
  Battery Vending Machine

  4S Lipo Battery Voltmeter, Charge Controller, and OLED Display Module with Arduino Mega2560

  Author: Christopher Lai
  Date: 8/16/2022
  Version: v1.1.5
*********/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Define Pin Locations
#define red_btn 28
#define yellow_btn 26
#define blue_btn 24
#define green_btn 22

// Define Variables

// OLED_state contains the menu in which the OLED is currently in
// 0 = Welcome Menu
// 1 = Total BMS Data
// 2 = Battery Cell Data
// 3 = Charge Selection
int OLED_state = 0;

// Battery Stuff
bool battstate = false;
float R1 = 1000.0;
float R2 = 2000.0;
float R3 = 3000.0;
float ref_voltage = 5.0;
int adc_value = 0;
float adc_voltage = 0.0;
float in_voltage = 0.0;

// Semi-Random Number Generation
int counter = 0;
int rand_high = 875;
int rand_low = 800;

// Display States
int full_state = 0;
int cell_state = 0;
int charge_state = 0;
int toggle_state = 0;

// [SETUP FUNCTION] Run through this code once to set things up
void setup() {
  // Use baud rate of 115200
  Serial.begin(115200);

  // Pin Modes
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(A6, INPUT);
  pinMode(A7, INPUT);
  pinMode(A8, INPUT);
  pinMode(A9, INPUT);
  pinMode(A10, INPUT);
  pinMode(A11, INPUT);
  pinMode(A12, INPUT);
  pinMode(A13, INPUT);
  pinMode(A14, INPUT);
  pinMode(A15, INPUT);

  pinMode(red_btn, INPUT);
  pinMode(yellow_btn, INPUT);
  pinMode(blue_btn, INPUT);
  pinMode(green_btn, INPUT);

  digitalWrite(0, LOW);
  digitalWrite(0, LOW);

  // Check for OLED Availability
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  
  display.clearDisplay();

  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("LOADING...");
  display.setCursor(0, 20);
  display.println("Setting Up");
  display.setCursor(0, 40);
  display.println("BVM BMS...");
  display.display(); 
  delay(1000);
}

// [MAIN FUNCTION] Continuous update loop
void loop() {
  int adc_read[16];
  float voltages[16];
  float percents[16];
  float full_batt[4];
  float full_percent[4];

  // Call function to insert ADC values into array
  // read_from_adc(adc_read); // Call this function if you have batteries plugged in!
  randomize_data(adc_read, 2); // Call this function for simulated data (safe testing)

  // Calculate voltages given each battery (assuming 4 batteries, 4S type)
  int temp_count = 0;
  for (int i = 1; i <= 4; i++){
    for (int j = 1; j <= 4; j++){
      voltages[temp_count] = volt_calc(adc_read[temp_count], j, true);
      percents[temp_count] = volt_calc(adc_read[temp_count], j, false);
      temp_count += 1; 
    }
  }

  // Store full voltage values in full_batt array
  float temp_sum = 0;
  for (int i = 0; i <= 3; i++) {
    temp_sum = 0;
    for (int j = 0; j <= 3; j++) {
      temp_sum += voltages[i * 4 + j];
    }
    full_batt[i] = temp_sum;
    full_percent[i] = temp_sum / 16.8 * 100;
  }

  // Arrange battery values for serial monitor print (no fancy)
  String output = "";
  for (int i = 0; i < 16; i++){
    output += String(voltages[i]) + " ";
  }

  // When GREEN button pressed, advance state += 1 (reset logic implemented)
  if (!digitalRead(green_btn)){
    OLED_state += 1;
    toggle_state = false;
    if (OLED_state == 1){
      full_state = 0;
    }
    else if (OLED_state == 2){
      cell_state = 0;
    }
    else if (OLED_state == 3){
      charge_state = 0;
    }
    else if (OLED_state == 4){
      OLED_state = 0;
    }
    delay(250);
  }

  // When RED button is pressed, reset state back to 0
  if (!digitalRead(red_btn)){
    OLED_state = 0;
    delay(250);
  }

  // When YELLOW button is pressed, toggle state
  if (!digitalRead(yellow_btn)){
    toggle_state += 1;
    if (toggle_state == 2){
      toggle_state = 0;
    }
    delay(250);
  }

  // Determine display state to figure out what to print on OLED
  if (OLED_state == 0){
    OLED_display0();
  }
  else if (OLED_state == 1){
    if (!digitalRead(blue_btn)){
      full_state += 1;
      if (full_state == 5){
        full_state = 0;
      }
      delay(250);
    }
    
    if (full_state == 0){
      OLED_display1();
    }
    else if (full_state == 1){
      if (toggle_state == 1){
        OLED_showFull(full_state, full_percent[full_state - 1], toggle_state);
      }
      else{
        OLED_showFull(full_state, full_batt[full_state - 1], toggle_state);
      }
    }
    else if (full_state == 2){
      if (toggle_state == 1){
        OLED_showFull(full_state, full_percent[full_state - 1], toggle_state);
      }
      else{
        OLED_showFull(full_state, full_batt[full_state - 1], toggle_state);
      }
    }
    else if (full_state == 3){
      if (toggle_state == 1){
        OLED_showFull(full_state, full_percent[full_state - 1], toggle_state);
      }
      else{
        OLED_showFull(full_state, full_batt[full_state - 1], toggle_state);
      }
    }
    else if (full_state == 4){
      if (toggle_state == 1){
        OLED_showFull(full_state, full_percent[full_state - 1], toggle_state);
      }
      else{
        OLED_showFull(full_state, full_batt[full_state - 1], toggle_state);
      }
    }
  }
  else if (OLED_state == 2){
    if (!digitalRead(blue_btn)){
      cell_state += 1;
      if (cell_state == 5){
        cell_state = 0;
      }
      delay(250);
    }
    
    if (cell_state == 0){
      OLED_display2();
    }
    else if (cell_state == 1){
      if (toggle_state == 0){
        OLED_showCell(cell_state, voltages[0], voltages[1], voltages[2], voltages[3], toggle_state);
      }
      else{
        OLED_showCell(cell_state, percents[0], percents[1], percents[2], percents[3], toggle_state);
      }
    }
    else if (cell_state == 2){
      if (toggle_state == 0){
        OLED_showCell(cell_state, voltages[4], voltages[5], voltages[6], voltages[7], toggle_state);
      }
      else{
        OLED_showCell(cell_state, percents[4], percents[5], percents[6], percents[7], toggle_state);
      }
    }
    else if (cell_state == 3){
      if (toggle_state == 0){
        OLED_showCell(cell_state, voltages[8], voltages[9], voltages[10], voltages[11], toggle_state);
      }
      else{
        OLED_showCell(cell_state, percents[8], percents[9], percents[10], percents[11], toggle_state);
      }
    }
    else if (cell_state == 4){
      if (toggle_state == 0){
        OLED_showCell(cell_state, voltages[12], voltages[13], voltages[14], voltages[15], toggle_state);
      }
      else{
        OLED_showCell(cell_state, percents[12], percents[13], percents[14], percents[15], toggle_state);
      }
    }
  }
  else if (OLED_state == 3){
    if (!digitalRead(blue_btn)){
      charge_state += 1;
      if (charge_state == 9){
        charge_state = 0;
      }
      delay(250);
    }
    
    if (charge_state == 0){
      OLED_display3();
    }
    else if (charge_state == 1){
      if (toggle_state == 0){
        OLED_showCharge(charge_state, toggle_state);
      }
      else{
        OLED_showCharge(charge_state, toggle_state);
      }
    }
    else if (charge_state == 2){
      if (toggle_state == 0){
        OLED_showCharge(charge_state, toggle_state);
      }
      else{
        OLED_showCharge(charge_state, toggle_state);
      }
    }
    else if (charge_state == 3){
      if (toggle_state == 0){
        OLED_showCharge(charge_state, toggle_state);
      }
      else{
        OLED_showCharge(charge_state, toggle_state);
      }
    }
    else if (charge_state == 4){
      if (toggle_state == 0){
        OLED_showCharge(charge_state, toggle_state);
      }
      else{
        OLED_showCharge(charge_state, toggle_state);
      }
    }
    else if (charge_state == 5){
      if (toggle_state == 0){
        OLED_showCharge(charge_state, toggle_state);
      }
      else{
        OLED_showCharge(charge_state, toggle_state);
      }
    }
    else if (charge_state == 6){
      if (toggle_state == 0){
        OLED_showCharge(charge_state, toggle_state);
      }
      else{
        OLED_showCharge(charge_state, toggle_state);
      }
    }
    else if (charge_state == 7){
      if (toggle_state == 0){
        OLED_showCharge(charge_state, toggle_state);
      }
      else{
        OLED_showCharge(charge_state, toggle_state);
      }
    }
    else if (charge_state == 8){
      if (toggle_state == 0){
        OLED_showCharge(charge_state, toggle_state);
      }
      else{
        OLED_showCharge(charge_state, toggle_state);
      }
    }
  }

  delay(100);

  Serial.println(output);
}

// [FUNCTION] Read from adc and store in central array
int read_from_adc(int * adc_read){
  adc_read[0] = analogRead(A0);
  adc_read[1] = analogRead(A1);
  adc_read[2] = analogRead(A2);
  adc_read[3] = analogRead(A3);
  adc_read[4] = analogRead(A4);
  adc_read[5] = analogRead(A5);
  adc_read[6] = analogRead(A6);
  adc_read[7] = analogRead(A7);
  adc_read[8] = analogRead(A8);
  adc_read[9] = analogRead(A9);
  adc_read[10] = analogRead(A10);
  adc_read[11] = analogRead(A11);
  adc_read[12] = analogRead(A12);
  adc_read[13] = analogRead(A13);
  adc_read[14] = analogRead(A14);
  adc_read[15] = analogRead(A15);
}

// [FUNCTION] Smart randomize number with deprecation constant
int randomize_data(int * adc_read, int dep_const){
  counter += 1;
  if (counter == 100){ // Every 100 seconds, decrease battery reading by dep const
    counter = 0;
    rand_high -= dep_const;
    rand_low -= dep_const;
  }

  // Debug
  // Serial.println(counter);

  // Check if system is lower than threshold, then reset ranges
  if (rand_low <= 412){ // Reasonable value = Halfway point
    rand_high = 875;
    rand_low = 800;
  }

  // Loop through adc_read array and generate random numbers between ranges
  for (int i = 0; i < 16; i++){
    adc_read[i] = random(rand_low, rand_high);
  }
}

// [FUNCTION] Calculate battery voltage given ADC value
float volt_calc(int adc_value, int cell_type, bool battstate){
  adc_voltage = (adc_value * ref_voltage)/1023.0;
  if (cell_type == 1){
    in_voltage = adc_voltage;
  }
  else if (cell_type == 2){
    in_voltage = adc_voltage/(R1/(R1+R1));
  }
  else if (cell_type == 3){
    in_voltage = adc_voltage/(R1/(R1+R2));
  }
  else if (cell_type == 4){
    in_voltage = adc_voltage/(R1/(R1+R3));
  }
  else
  {
    return -1.0;
  }
  
  if (battstate)
  {
    // Returns voltage from each cell
    return in_voltage/(cell_type);
  }
  else
  {
    // Returns a percentage of the nominal voltage
    return in_voltage/(4.2*cell_type) * 100;
  }
}


void OLED_display0()
{
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("WELCOME!");
  display.setCursor(0,20);
  display.println("Testbench");
  display.setCursor(0,40);
  display.println("v1.1.5");
  display.display();
}

void OLED_display1()
{
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("TOTAL DATA");
  display.setCursor(0,20);
  display.setTextSize(1);
  display.println("Press the blue button");
  display.setCursor(0,30);
  display.println("to cycle through data");
  display.setCursor(0,40);
  display.println("Press the yellow btn");
  display.setCursor(0,50);
  display.println("to toggle between V/%");
  display.display();
}

void OLED_showFull(int battnum, float battfull, int toggle)
{
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("BATT #" + String(battnum));
  display.setCursor(0,20);
  display.setTextSize(2);
  if (toggle_state == 0){
    display.println(String(battfull) + "V");
  }
  else{
    display.println(String(battfull) + "%");
  }
  display.display();
}

void OLED_display2()
{
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("BATT DATA");
  display.setCursor(0,20);
  display.setTextSize(1);
  display.println("Press the blue button");
  display.setCursor(0,30);
  display.println("to cycle through data");
  display.setCursor(0,40);
  display.println("Press the yellow btn");
  display.setCursor(0,50);
  display.println("to toggle between V/%");
  display.display();
}

void OLED_showCell(int battnum, float cell1, float cell2, float cell3, float cell4, int toggle)
{
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("BATT #" + String(battnum));
  display.setCursor(0,20);
  display.setTextSize(1);
  if (toggle_state == 0){
    display.println(String(cell1) + "V   " + String(cell2) + "V");
    display.setCursor(0,30);
    display.println(String(cell3) + "V   " + String(cell4) + "V");
  }
  else{
    display.println(String(cell1) + "%   " + String(cell2) + "%");
    display.setCursor(0,30);
    display.println(String(cell3) + "%   " + String(cell4) + "%");
  }
  display.display();
}

void OLED_display3()
{
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("CHARG MODE");
  display.setCursor(0,20);
  display.setTextSize(1);
  display.println("Press the blue btn");
  display.setCursor(0,30);
  display.println("to cycle through batt");
  display.setCursor(0,40);
  display.println("Press the yellow btn");
  display.setCursor(0,50);
  display.println("to toggle charge mode");
  display.display();
}

void OLED_showCharge(int battnum, int toggle)
{
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("BATT #" + String(battnum));
  display.setCursor(0,20);
  display.setTextSize(2);
  if (toggle_state == 0){
    display.println("OFF");
    analogWrite(battnum + 1, 0);
  }
  else{
    display.println("ON");
    analogWrite(battnum + 1, 1023);
  }
  display.display();
}