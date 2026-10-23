
#include <Arduino.h>

//heartbeat
const uint8_t HEARTBEAT_LED = LED_BUILTIN;
unsigned long lastBlink = 0;
bool ledState = false;

// MINI TESLA V1 - MOTOR CONTROL
// Teensy 4.1 + 2x Cytron MDD10A

enum Motor { FL = 0, RL = 1, FR = 2, RR = 3 };

// Exact wiring
const uint8_t PWM_PINS[4] = {2, 4, 3, 5};
const uint8_t DIR_PINS[4] = {6, 8, 7, 9};

// Adjust after checking wheel directions
const bool REVERSED[4] = {
    true, true, false, false
};

// Initial testing limits
const int TEST_PWM = 80;       // 0-255
const unsigned long PULSE_MS = 300;

bool motionActive = false;
unsigned long motionStart = 0;

void stopMotors() {
    for (int i = 0; i < 4; i++) {
        analogWrite(PWM_PINS[i], 0);
    }
    motionActive = false;
}

// Speed range: -255 to +255
void setMotor(int id, int speed) {
    speed = constrain(speed, -255, 255);

    if (REVERSED[id]) {
        speed = -speed;
    }

    // Disable PWM before changing direction
    analogWrite(PWM_PINS[id], 0);

    digitalWrite(DIR_PINS[id],
                 speed >= 0 ? HIGH : LOW);

    analogWrite(PWM_PINS[id], abs(speed));
}

// Order: FL, RL, FR, RR
void drive(int fl, int rl, int fr, int rr) {
    stopMotors();

    setMotor(FL, fl);
    setMotor(RL, rl);
    setMotor(FR, fr);
    setMotor(RR, rr);

    motionStart = millis();
    motionActive = true;
}

void setup() {
    for (int i = 0; i < 4; i++) {
        pinMode(PWM_PINS[i], OUTPUT);
        pinMode(DIR_PINS[i], OUTPUT);

        digitalWrite(DIR_PINS[i], LOW);
        analogWrite(PWM_PINS[i], 0);
    }

    pinMode(LED_BUILTIN, OUTPUT);

    Serial.begin(115200);

    Serial.println("MINI TESLA V1 READY");
    Serial.println("1/2/3/4: Test individual motors");
    Serial.println("W/S: Forward / Reverse");
    Serial.println("A/D: Strafe left / right");
    Serial.println("Q/E: Rotate left / right");
    Serial.println("X: Stop");
}

void loop() {

  //heartbeat LED for teensy
  
  if (millis() - lastBlink >= 500) {
      lastBlink = millis();

      ledState = !ledState;
      digitalWrite(LED_BUILTIN, ledState);
  }


    // Automatic stop after 300 ms
    if (motionActive &&
        millis() - motionStart >= PULSE_MS) {
        stopMotors();
        Serial.println("AUTO STOP");
    }

    if (Serial.available() == 0) {
        return;
    }

    char cmd = Serial.read();

    // Ignore line endings
    if (cmd == '\n' || cmd == '\r') {
        return;
    }

    // Accept uppercase and lowercase commands
    if (cmd >= 'A' && cmd <= 'Z') {
        cmd += ('a' - 'A');
    }

    const int p = TEST_PWM;

    switch (cmd) {
        case '1':
            drive(p, 0, 0, 0);
            break;
        case '2':
            drive(0, p, 0, 0);
            break;
        case '3':
            drive(0, 0, p, 0);
            break;
        case '4':
            drive(0, 0, 0, p);
            break;

        case 'w':
            drive(p, p, p, p);
            break;
        case 's':
            drive(-p, -p, -p, -p);
            break;

        // Mecanum X wheel configuration
        case 'a':
            drive(-p, p, p, -p);
            break;
        case 'd':
            drive(p, -p, -p, p);
            break;

        case 'q':
            drive(-p, -p, p, p);
            break;
        case 'e':
            drive(p, p, -p, -p);
            break;

        case 'x':
            stopMotors();
            Serial.println("STOPPED");
            return;

        default:
            Serial.println("Unknown command");
            return;
    }

    Serial.print("Command: ");
    Serial.println(cmd);
}
