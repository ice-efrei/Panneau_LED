#include <FastLED.h>
#include <arduinoFFT.h>
#include <SPI.h>

#define SWITCH_PIN 4  // Pin connected to switch button
#define LED_PIN 3   // Pin connected to LED

// FastLED parameters
#define BRIGHTNESS  30
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
#define UPDATES_PER_SECOND 100

// Params for width and height
const uint8_t kMatrixWidth = 30;
const uint8_t kMatrixHeight = 40;
#define NUM_LEDS (kMatrixWidth * kMatrixHeight)

// Param for different pixel layouts
const bool kMatrixSerpentineLayout = true;
const bool kMatrixVertical = false;

// FastLed arrays
CRGB led_safe[ NUM_LEDS + 1];
CRGB* const leds(led_safe + 1);

// Led matrix utility functions
uint16_t XY( uint8_t x, uint8_t y)
{
  uint16_t i;
  
  if( kMatrixSerpentineLayout == false) {
    if (kMatrixVertical == false) {
      i = (y * kMatrixWidth) + x;
    } else {
      i = kMatrixHeight * (kMatrixWidth - (x+1))+y;
    }
  }

  if( kMatrixSerpentineLayout == true) {
    if (kMatrixVertical == false) {
      if( y & 0x01) {
        // Odd rows run backwards
        uint8_t reverseX = (kMatrixWidth - 1) - x;
        i = (y * kMatrixWidth) + reverseX;
      } else {
        // Even rows run forwards
        i = (y * kMatrixWidth) + x;
      }
    } else { // vertical positioning
      if ( x & 0x01) {
        i = kMatrixHeight * (kMatrixWidth - (x+1))+y;
      } else {
        i = kMatrixHeight * (kMatrixWidth - x) - (y+1);
      }
    }
  }
  
  return i;
}
uint16_t XYsafe( uint8_t x, uint8_t y)
{
  if( x >= kMatrixWidth) return -1;
  if( y >= kMatrixHeight) return -1;
  return XY(x,y);
}

// Audio analyser parameters
#define SAMPLES 64            //Must be a power of 2
#define MAX_DEVICES  4   // Total number display modules
#define CLK_PIN   13  // Clock pin to communicate with display
#define DATA_PIN  11  //   Data pin to communicate with display
#define CS_PIN    10  // Control pin to   communicate with display
#define xres 30      // Total number of  columns in   the display, must be <= SAMPLES/2
#define yres 40      // Total number of  rows   in the display

// Audio analyser variables   
double vReal[SAMPLES];
double vImag[SAMPLES];
char data_avgs[xres];

int AnalyserPattern[]={0, 128, 192, 160, 144, 136, 132, 130, 129};
int yvalue, displaycolumn , displayvalue, peaks[xres], displaymode = 1;
const int buttonPin   = 5;    // the number of the pushbutton pin
int state = HIGH;             //   the current reading from the input pin
int previousState = LOW;   // the previous   reading from the input pin
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers

arduinoFFT FFT = arduinoFFT();                                    // FFT object

// Output switch variables
bool prevstatus = false;
int counter = 0, arduino_output = 0;
static uint8_t hue;

void setup() {
    ADCSRA = 0b11100101;      // set ADC to free running mode   and set pre-scalar to 32 (0xe5)
    ADMUX = 0b00000000;       // use pin A0 and   external voltage reference

    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(BRIGHTNESS);
    
    pinMode(SWITCH_PIN,INPUT_PULLUP);

    pinMode(30, OUTPUT);
    pinMode(31, OUTPUT);
    pinMode(32, OUTPUT);

    Serial.begin(9600);
    delay(50);            // wait to get reference   voltage stabilized
}

void updateOutput(){
    int sensorValue = digitalRead(SWITCH_PIN);

    if (!sensorValue && !prevstatus) {
        counter = (counter + 1)%4;
        prevstatus = true;
    }else if (sensorValue && prevstatus){
        prevstatus = false;
    }

    if (counter == 0) {
        digitalWrite(30, HIGH);
        digitalWrite(31, LOW);
        digitalWrite(32, LOW);
    }else if (counter == 1) {
        digitalWrite(30, LOW);
        digitalWrite(31, HIGH);
        digitalWrite(32, LOW);
    }else if (counter == 2) {
        digitalWrite(30, LOW);
        digitalWrite(31, LOW);
        digitalWrite(32, HIGH);
        arduino_output = 0;
    }else if (counter == 3) {
        digitalWrite(30, LOW);
        digitalWrite(31, LOW);
        digitalWrite(32, HIGH);
        arduino_output = 1;
    }else{
        digitalWrite(30, LOW);
        digitalWrite(31, LOW);
        digitalWrite(32, LOW);
    }
}

void audioToArray(){   
    // ++ Sampling
   for(int i=0; i<SAMPLES; i++)
    {
        while(!(ADCSRA & 0x10));  // wait for ADC to complete current conversion ie ADIF bit set
        ADCSRA = 0b11110101;  // clear ADIF bit so that ADC can do next operation (0xf5)
        int value = ADC - 512 ;  // Read from ADC and subtract DC offset caused value
        vReal[i]= value/8;  // Copy to bins after compressing
        vImag[i] = 0;                         
    }
    // -- Sampling

    // ++ FFT
    FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
    FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
    FFT.ComplexToMagnitude(vReal,   vImag, SAMPLES);
    // -- FFT

    // ++ re-arrange FFT result   to match with no. of columns on display ( xres )
    int step = (SAMPLES/2)/xres;   
    int c=0;
    for(int i=0; i<(SAMPLES/2); i+=step)  
    {
        data_avgs[c] = 0;
        for (int k=0 ; k < step ; k++) {
            data_avgs[c] = data_avgs[c] + vReal[i+k];
        }
        data_avgs[c] = data_avgs[c]/step; 
        c++;
    }
    // -- re-arrange FFT result to match with no. of columns on display ( xres )
    
    // ++ send to display according measured value 
    for(int i=0; i < xres; i++)
    {
        data_avgs[i] = constrain(data_avgs[i],0,80);             // set max & min values for buckets
        data_avgs[i] = map(data_avgs[i], 0, 80, 0, yres);        // remap averaged values to yres
        yvalue=data_avgs[i];

        peaks[i] = peaks[i]-1;    // decay by one light
        if (yvalue > peaks[i])   
            peaks[i] = yvalue ;
        yvalue = peaks[i];    
        displayvalue=AnalyserPattern[yvalue];
        for (int j = 0; j < yres; j++) {
            if (j < yvalue)
            {
                leds[XY(i, j)] = CRGB(214, 236, 239);
            }else{
                leds[XY(i, j)] = CRGB(0, 0, 0);
            }
        }
     }
}

void matrixExample(){
    uint32_t ms = millis();
    int32_t yHueDelta32 = ((int32_t)cos16( ms * (27/1) ) * (350 / kMatrixWidth));
    int32_t xHueDelta32 = ((int32_t)cos16( ms * (39/1) ) * (310 / kMatrixHeight));
    
    uint8_t startHue8 = ms / 65536;
    int8_t yHueDelta8 = yHueDelta32 / 32768;
    int8_t xHueDelta8 = xHueDelta32 / 32768;

    uint8_t lineStartHue = startHue8;
    for( uint8_t y = 0; y < kMatrixHeight; y++) {
        lineStartHue += yHueDelta8;
        uint8_t pixelHue = lineStartHue;      
        for( uint8_t x = 0; x < kMatrixWidth; x++) {
            pixelHue += xHueDelta8;
            leds[ XY(x, y)] = CHSV(pixelHue, 255, 255);
        }
    }
}

void loop() {
    updateOutput();
    if (arduino_output == 0) {
        audioToArray();
    }else{
        matrixExample();
    }
    FastLED.show();
    FastLED.delay(1000 / UPDATES_PER_SECOND);
}
