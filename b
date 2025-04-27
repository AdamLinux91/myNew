
#define waterpump 4
char recievedchar;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(waterpump, OUTPUT);
}

void loop() {

  // put your main code here, to run repeatedly:
  if (Serial.available() > 0 ){
    recievedchar = Serial.read();
    if (recievedchar == '1'){
      digitalWrite(waterpump, 1); 
      
  }
  else{
      digitalWrite(waterpump, 0);
    }
  
  }
  delay(1000
  );
}
