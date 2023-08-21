// work modes:
// 1 - idle
// 2 - voltage measuring

float input_volt = 0.0;
int work_mode = 1;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available())
  {
    int temp_mode = Serial.readString().toInt();
    if (temp_mode) 
    {
      work_mode  = temp_mode;
    }
  }

  if (work_mode == 2)
  {
    int analogvalue = analogRead(A0);
    input_volt = (analogvalue * 5.0) / 1024.0;
    if (input_volt != 0.0)
    {
      Serial.print("v=");
      Serial.println(input_volt, 6);
    }
  } else {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    Serial.println("Hello from arduino");
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
  }
}
