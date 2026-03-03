// ===================================================
// ABR Detect Heater Controller (Arduino)
// Updated behavior:
// - Blue LED turns on when 10 consecutive NanoVNA resonance
//   readings are within 0.03 MHz.
// - Commands from Pi:
//     START          -> start system
//     STOP           -> stop system
//     VNA:<freq_mhz> -> provide latest resonance in MHz
// - Emergency stop path removed.
// ===================================================

// ===================================================
// SYSTEM MODE SELECTION
// ===================================================
#define MODE_RUN   0
#define MODE_TUNE  1
#define SYSTEM_MODE MODE_RUN

// ===================================================
// PIN ASSIGNMENTS
// ===================================================
const int thermistorPin1 = A0;
const int thermistorPin2 = A5;
const int heaterPin = 3;        // PWM
const int fanPin = 11;          // MOSFET ON/OFF
const int redLEDPin = 8;
const int blueLEDPin = 12;

// ===================================================
// THERMISTOR PARAMETERS
// ===================================================
const float R_FIXED = 15000.0;
const float R0 = 15000.0;
const float T0 = 298.15;
const float BETA = 3740.0;

// ===================================================
// PI CONTROL PARAMETERS
// ===================================================
float T_TARGET = 25.0;
float Kp = 12.0;
float Ki = 0.30;

float integralHeater = 0;

const int PWM_MIN = 80;
const int PWM_MAX = 255;
const float INTEGRAL_MIN = -150;
const float INTEGRAL_MAX = 150;

// ===================================================
// READY + LOCK PARAMETERS
// ===================================================
const float VNA_STABILITY_THRESHOLD_MHZ = 0.03;
const int VNA_STABLE_REQUIRED = 10;
const unsigned long VNA_TIMEOUT_MS = 15000UL;

int vnaStableCount = 0;
float lastVnaMHz = -1.0;
unsigned long lastVnaUpdateMs = 0;

bool isReady = false;
bool isLocked = false;
bool reactionComplete = false;

// ===================================================
// USER CONTROL FLAGS
// ===================================================
bool systemEnabled = false;

// ===================================================
// TIMING
// ===================================================
unsigned long readyTime = 0;
const unsigned long LOCK_DURATION = 180UL * 60UL * 1000UL;

// ===================================================
void stopSystem() {
  analogWrite(heaterPin, 0);
  digitalWrite(fanPin, LOW);
  digitalWrite(redLEDPin, LOW);
  digitalWrite(blueLEDPin, LOW);

  systemEnabled = false;
  isReady = false;
  isLocked = false;
  reactionComplete = false;
  integralHeater = 0;
  vnaStableCount = 0;
  lastVnaMHz = -1.0;

  Serial.println("=== SYSTEM STOPPED ===");
}

// ===================================================
void startSystem() {
  systemEnabled = true;
  isReady = false;
  isLocked = false;
  reactionComplete = false;
  integralHeater = 0;
  vnaStableCount = 0;
  lastVnaMHz = -1.0;
  lastVnaUpdateMs = 0;

  digitalWrite(fanPin, HIGH);
  Serial.println("=== SYSTEM STARTED ===");
}

// ===================================================
float readThermistor(int pin) {
  int adc = analogRead(pin);
  adc = constrain(adc, 1, 1022);

  float Vout = adc * (5.0 / 1023.0);
  float ratio = (5.0 / Vout) - 1.0;
  ratio = max(ratio, 0.001);

  float R = R_FIXED * ratio;
  float tempK = 1.0 / ((1.0 / T0) + (1.0 / BETA) * log(R / R0));

  return tempK - 273.15;
}

// ===================================================
void updateVnaStability(float freqMHz) {
  if (lastVnaMHz < 0.0) {
    vnaStableCount = 1;
  } else {
    float delta = abs(freqMHz - lastVnaMHz);
    if (delta <= VNA_STABILITY_THRESHOLD_MHZ) {
      vnaStableCount++;
    } else {
      vnaStableCount = 1;
    }
  }

  lastVnaMHz = freqMHz;
  lastVnaUpdateMs = millis();

  if (!isReady && vnaStableCount >= VNA_STABLE_REQUIRED) {
    isReady = true;
    isLocked = true;
    readyTime = millis();
    integralHeater = 0;

    Serial.println("=== SYSTEM READY (VNA STABLE) ===");
    Serial.println("15 min reaction started");
  }
}

// ===================================================
void handleSerialCommands() {
  if (!Serial.available()) {
    return;
  }

  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) {
    return;
  }

  if (line == "START" && !systemEnabled) {
    startSystem();
    return;
  }

  if (line == "STOP") {
    stopSystem();
    return;
  }

  if (line.startsWith("VNA:")) {
    String payload = line.substring(4);
    float freqMHz = payload.toFloat();
    if (freqMHz > 0.0) {
      updateVnaStability(freqMHz);
      Serial.print("VNA_MHz: ");
      Serial.print(freqMHz, 6);
      Serial.print("  StableCount: ");
      Serial.println(vnaStableCount);
    }
  }
}

// ===================================================
void setup() {
  Serial.begin(115200);

  pinMode(heaterPin, OUTPUT);
  pinMode(fanPin, OUTPUT);
  pinMode(redLEDPin, OUTPUT);
  pinMode(blueLEDPin, OUTPUT);

  analogWrite(heaterPin, 0);
  digitalWrite(fanPin, LOW);
  digitalWrite(redLEDPin, LOW);
  digitalWrite(blueLEDPin, LOW);

  Serial.println("=== SYSTEM IDLE ===");
  Serial.println("Waiting for START from Pi.");
}

// ===================================================
void loop() {
  handleSerialCommands();

  if (!systemEnabled) {
    delay(50);
    return;
  }

  // If Pi stops sending VNA readings, drop ready state.
  if (lastVnaUpdateMs > 0 && millis() - lastVnaUpdateMs > VNA_TIMEOUT_MS) {
    isReady = false;
    isLocked = false;
    vnaStableCount = 0;
    lastVnaMHz = -1.0;
  }

  float t2 = readThermistor(thermistorPin2);
  static int pwmHeater = 0;

  // ---------- HEATER PI CONTROL ----------
  float error = T_TARGET - t2;

  // Integrator gating (anti-windup)
  if (abs(error) < 0.8 && isLocked) {
    integralHeater += error;
  }

  integralHeater = constrain(integralHeater, INTEGRAL_MIN, INTEGRAL_MAX);

  float effectiveKi = isLocked ? Ki : 0.0;
  pwmHeater = Kp * error + effectiveKi * integralHeater;
  pwmHeater = constrain(pwmHeater, 0, PWM_MAX);

  if (pwmHeater > 0 && pwmHeater < PWM_MIN) {
    pwmHeater = PWM_MIN;
  }

  analogWrite(heaterPin, pwmHeater);

  // ---------- TIMER CHECK ----------
  if (isLocked && millis() - readyTime >= LOCK_DURATION) {
    isLocked = false;
    isReady = false;
    reactionComplete = true;

    analogWrite(heaterPin, 0);
    digitalWrite(fanPin, LOW);

    Serial.println("=== REACTION COMPLETE ===");

    systemEnabled = false;
    reactionComplete = false;
    integralHeater = 0;
    vnaStableCount = 0;
    lastVnaMHz = -1.0;
  }

  // ---------- LED STATUS ----------
  if (isReady) {
    digitalWrite(redLEDPin, LOW);
    digitalWrite(blueLEDPin, HIGH);
  } else if (pwmHeater > 0) {
    digitalWrite(redLEDPin, HIGH);
    digitalWrite(blueLEDPin, LOW);
  } else {
    digitalWrite(redLEDPin, LOW);
    digitalWrite(blueLEDPin, LOW);
  }

  // ---------- SERIAL OUTPUT ----------
  Serial.print("T2: ");
  Serial.print(t2, 2);
  Serial.print("  PWM: ");
  Serial.print(pwmHeater);
  Serial.print("  Locked: ");
  Serial.println(isLocked);

  delay(500);
}
