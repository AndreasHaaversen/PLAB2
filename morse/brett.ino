// Include libraries
#include <Bounce2.h>
#include <elapsedMillis.h>

// Define pin constants
const int dotOut = 9;
const int dashOut = 8;
const int buttonIn = 6;

// Define time constant
const unsigned long T = 300;

// Debouncer object that handles debouncing of the button
Bounce debouncer = Bounce();

// Timers
elapsedMillis buttonPress;
elapsedMillis pause;

void setup() {
    Serial.begin(9600);
    pinMode(dotOut, OUTPUT);
    pinMode(dashOut, OUTPUT);
    pinMode(buttonIn, INPUT_PULLUP);
    // Configures the debouncer
    debouncer.attach(buttonIn);
    debouncer.interval(5);
}

void loop() {
    debouncer.update();
    if(debouncer.fell()){
        // Button pushed, check how long the last pause was
        if(pause > 3.5*T && pause <6.5*T){
            Serial.print(3);
        } else if( pause > 6.5*T && pause < 9.5*T){
            Serial.print(4);
        } else if (pause > 10*T){
            Serial.print(5);
    }
    // reset timer
        buttonPress = 0;
    } else if(debouncer.rose()) {
        // Button released, check how long is was pressed.
        if(buttonPress < T){
            Serial.print(1);
            flashDot();
        } else if(buttonPress < 3*T) {
            Serial.print(2);
            flashDash();
        }
        // reset timer
        pause = 0;
    }

}

// Helpermethods
void flashDot() {
    digitalWrite(dotOut, HIGH);
    delay(100);
    digitalWrite(dotOut, LOW);
}

void flashDash() {
    digitalWrite(dashOut, HIGH);
    delay(100);
    digitalWrite(dashOut, LOW);
}