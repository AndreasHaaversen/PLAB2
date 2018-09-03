#include <Bounce2.h>

#include <elapsedMillis.h>

const int dotOut = 9;
const int dashOut = 8;
const int buttonIn = 6;

const unsigned long T = 300;

Bounce debouncer = Bounce();

elapsedMillis buttonPress;
elapsedMillis pause;

void setup() {
    Serial.begin(9600);
    pinMode(dotOut, OUTPUT);
    pinMode(dashOut, OUTPUT);
    pinMode(buttonIn, INPUT_PULLUP);
    debouncer.attach(buttonIn);
    debouncer.interval(5);
}

void loop() {
    debouncer.update();
    if(debouncer.fell()){
        if(pause > 3.5*T && pause <6.5*T){
            Serial.print(3);
        } else if( pause > 6.5*T && pause < 9.5*T){
            Serial.print(4);
        } else if (pause > 10*T){
            Serial.print(5);
    }
        buttonPress = 0;
    } else if(debouncer.rose()) {
        if(buttonPress < T){
            Serial.print(1);
            flashDot();
        } else if(buttonPress < 3*T) {
            Serial.print(2);
            flashDash();
        }
        pause = 0;
    }

}

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