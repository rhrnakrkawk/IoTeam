#include <Arduino.h>
#include <IO7F8266.h>
#include <SSD1306.h>
#include <string>
#include <Wire.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>

const int pulseA = 12;
const int pulseB = 13;
const int pushSW = 2;
const int RELAY =15;
volatile int lastEncoded = 0;
volatile long encoderValue = 0;
volatile bool pressed = false;

String user_html = "";
String content = "";
String jsonString = " ";

int num = 0;

unsigned long lastPublishMillis = -pubInterval;
SSD1306 display(0x3c, 4, 5, GEOMETRY_128_32);
char *ssid_pfix = (char *)"MoonButton";

void message(char *topic, byte *payload, unsigned int payloadLength)
{
  byte2buff(msgBuffer, payload, payloadLength);
  StaticJsonDocument<512> root;
  DeserializationError error = deserializeJson(root, String(msgBuffer));

  if (error)
  {
    Serial.println("handleCommand: payload parse FAILED");
    return;
  }
}

void tableRotary()//Table check
{
  if (encoderValue < 10)
  {
    content = "Table 1";
  }
  else if (encoderValue > 9 && encoderValue < 20)
  {
    content = "Table 2";
  }
  else if (encoderValue > 19 && encoderValue < 30)
  {
    content = "Table 3";
  }
  else if (encoderValue > 29 && encoderValue < 40)
  {
    content = "Monthly Sales";
  }
  else if (encoderValue > 39 && encoderValue < 50)
  {
    content = "Monthly Customer";
  }
  else if (encoderValue > 49 && encoderValue < 60)
  {
    content = "Monthly Best";
  }

}

IRAM_ATTR void handleRotary()
{
  // Never put any long instruction
  int MSB = digitalRead(pulseA); // MSB = most significant bit
  int LSB = digitalRead(pulseB); // LSB = least significant bit

  int encoded = (MSB << 1) | LSB;         // converting the 2 pin value to single number
  int sum = (lastEncoded << 2) | encoded; // adding it to the previous encoded value
  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011)
    encoderValue++;

  if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
    encoderValue--;

  lastEncoded = encoded; // store this value for next time
  if (encoderValue > 61)
  {
    encoderValue = 60;
  }
  else if (encoderValue < 0)
  {
    encoderValue = 0;
  }
}

IRAM_ATTR void buttonClicked()
{
  pressed = true;
  Serial.println("pushed");
}

void setup()
{
  Serial.begin(115200);
  pinMode(pushSW, INPUT_PULLUP);
  pinMode(pulseA, INPUT_PULLUP);
  pinMode(pulseB, INPUT_PULLUP);
  attachInterrupt(pulseA, handleRotary, CHANGE);
  attachInterrupt(pulseB, handleRotary, CHANGE);
  attachInterrupt(pushSW, buttonClicked, FALLING);
  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);
  
  initDevice();
  JsonObject meta = cfg["meta"];
  pubInterval = meta.containsKey("pubInterval") ? meta["pubInterval"] : 0;
  lastPublishMillis = -pubInterval;
  
  WiFi.mode(WIFI_STA);
  WiFi.begin((const char*)cfg["ssid"], (const char*)cfg["w_pw"]);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.printf("\nIP address : ");
  Serial.println(WiFi.localIP());

  client.setCallback(message);
}
WiFiClient client1;
void loop() {
    delay(500);
    Serial.println(encoderValue);
    tableRotary();

    HTTPClient http;

    //테이블 1의 주문내역
    if (encoderValue < 10)
    {
      display.clear();
      display.drawString(35, 00, content);     
      // HTTP GET 요청 보내기
      http.begin(client1, "http://3.216.219.9:4400/api/orders/detail?table_id=1");
      //int httpCode = http.GET();
      String payload;
      String key;
      //API 서버
      if (0) {
        payload = http.getString();
        StaticJsonDocument<200> doc;
        DeserializationError error = deserializeJson(doc, payload);
        display.drawString(20, 11, "Request : "); 
        if (!error) {
          if (doc.containsKey("call")) {
            bool call = doc["call"].as<bool>();
            if (call) {
              // call이 true인 경우
              if (doc.containsKey("content")) {
                String content = doc["content"].as<String>();
                display.drawString(65, 11, content);
              }
            } 
            else {
              // call이 false인 경우
              if (doc.containsKey("menu")) {
                String menu = doc["menu"].as<String>();
                display.drawString(65, 11, menu);
                if (doc.containsKey("amount")) {
                  int amount = doc["amount"].as<int>();
                  display.drawString(20, 22, "Amount : ");
                  display.drawString(65, 22, String(amount));
                }
              }
            }
          }
        }
      Serial.println(payload);
      }
      //EDGE 서버
      else {
        //EDGE서버-table1 주문
        http.begin(client1, "http://192.168.133.99:4400/get/order");
        int httpCode = http.GET();
        String payload1;
        String key;
        if (httpCode > 0) {
          payload1 = http.getString();
          StaticJsonDocument<200> doc1[0];
          DeserializationError error = deserializeJson(doc1[0], payload1);
          if (!error) {
            if (doc1[0].containsKey("table_id")) {
              int table_id = doc1[0]["table_id"].as<int>();
              if (table_id == 1) {
                // table_id = 1인 경우
                if (doc1[0].containsKey("menu")) {
                  String menu = doc1[0]["menu"].as<String>();
		              display.drawString(20,11,menu);
                  if (doc1[0].containsKey("amount")) {
                    int amount = doc1[0]["amount"].as<int>();                  		  
                    display.drawString(65, 11, String(amount)); 
                  }
                }
              }
            }
            Serial.println(payload1);
          }
          
        }
        http.end();
        //EDGE서버-table1 직원호출
        http.begin(client1, "http://192.168.133.99:4400/get/call");
        httpCode = http.GET();
        String payload2;
        if (httpCode > 0) {
          payload2 = http.getString();
          StaticJsonDocument<200> doc2[0];
          DeserializationError error = deserializeJson(doc2[0], payload2);
          if (!error) {
            if (doc2[0].containsKey("table_id")) {
              int table_id = doc2[0]["table_id"].as<int>();
              if (table_id == 1) {
                // table_id = 1인 경우
                if (doc2[0].containsKey("call")) {
                  String call = doc2[0]["call"].as<String>();
                  Serial.println(call);
		              display.drawString(20,22,"Call : ");
                  display.drawString(65,22, call);
                  display.display();
                  
                  
                }
              }
            }
            Serial.println(payload2);
          }  
        }
        http.end();
        if (pressed == true) {
          http.begin(client1, "http://192.168.133.99:4400/clear");
          Serial.println("skh");
          httpCode = http.GET();
          http.end();
          pressed = false;
        }
      } 
      // http통신 종료
      http.end();
      delay(1500);
      display.display();
    }
    
    //테이블 2의 주문내역
    else if (encoderValue > 9 && encoderValue < 20)
    {
      display.clear();
      display.drawString(35, 00, content);     
      // HTTP GET 요청 보내기
      http.begin(client1, "http://3.216.219.9:4400/api/orders/detail?table_id=2");
      //int httpCode = http.GET();
      String payload;
      String key;
      if (0) {
        payload = http.getString();
        StaticJsonDocument<200> doc;
        DeserializationError error = deserializeJson(doc, payload);
        display.drawString(20, 11, "Request : "); 
        if (!error) {
          if (doc.containsKey("call")) {
            bool call = doc["call"].as<bool>();
            if (call) {
              // call이 true인 경우
              if (doc.containsKey("content")) {
                String content = doc["content"].as<String>();
                display.drawString(65, 11, content);
              }
            } 
            else {
              // call이 false인 경우
              if (doc.containsKey("menu")) {
                String menu = doc["menu"].as<String>();
                display.drawString(65, 11, menu);
                if (doc.containsKey("amount")) {
                  int amount = doc["amount"].as<int>();
                  display.drawString(20, 22, "Amount : ");
                  display.drawString(65, 22, String(amount));
                }
              }
            }
          }
        }
      Serial.println(payload);
      }
      //EDGE 서버
      else {
        //EDGE서버-table2 주문
        http.begin(client1, "http://192.168.133.99:4400/get/order");
        int httpCode = http.GET();
        String payload1;
        String key;
        if (httpCode > 0) {
          payload1 = http.getString();
          StaticJsonDocument<200> doc1[0];
          DeserializationError error = deserializeJson(doc1[0], payload1);
          if (!error) {
            if (doc1[0].containsKey("table_id")) {
              int table_id = doc1[0]["table_id"].as<int>();
              if (table_id == 2) {
                // table_id = 2인 경우
                if (doc1[0].containsKey("menu")) {
                  String menu = doc1[0]["menu"].as<String>();
		              display.drawString(20,11,menu);
                  if (doc1[0].containsKey("amount")) {
                    int amount = doc1[0]["amount"].as<int>();                  		  
                    display.drawString(65, 11, String(amount));
                    
                  }
                }
              }
            }
            Serial.println(payload1);
          }
          
        }
        http.end();
        //EDGE서버-table2 직원호출
        http.begin(client1, "http://192.168.133.99:4400/get/call");
        httpCode = http.GET();
        String payload2;
        if (httpCode > 0) {
          payload2 = http.getString();
          StaticJsonDocument<200> doc2[0];
          DeserializationError error = deserializeJson(doc2[0], payload2);
          if (!error) {
            if (doc2[0].containsKey("table_id")) {
              int table_id = doc2[0]["table_id"].as<int>();
              if (table_id == 2) {
                // table_id = 2인 경우
                if (doc2[0][0].containsKey("call")) {
                  String call = doc2[0][0]["call"].as<String>();
                  Serial.println(call);
		              display.drawString(20,22,"Call : ");
                  display.drawString(65,22, call);
                  display.display();             
                }
              }
            }
            Serial.println(payload2);
          }  
        }
        if (pressed == true) {
          http.begin(client1, "http://192.168.133.99:4400/clear");
          httpCode = http.GET();
          http.end();
          pressed = false;
        }
        
      } 
      // http통신 종료
      http.end();
      delay(1500);
      display.display();
    }
    //테이블 3의 주문내역
    else if (encoderValue > 19 && encoderValue < 30)
    {
      display.clear();
      display.drawString(35, 00, content);
      // HTTP GET 요청 보내기
      http.begin(client1, "http://3.216.219.9:4400/api/orders/detail?table_id=3");
      //int httpCode = http.GET();
      String payload;
      String key;
      if (0) {
        payload = http.getString();
        StaticJsonDocument<200> doc;
        DeserializationError error = deserializeJson(doc, payload);
        display.drawString(20, 11, "Request : ");      
        if (!error) {
          if (doc.containsKey("call")) {
            bool call = doc["call"].as<bool>();
            if (call) {
              // call이 true인 경우
              if (doc.containsKey("content")) {
                String content = doc["content"].as<String>();
                display.drawString(65, 11, content);
                display.display();
              }
            } 
            else {
              // call이 false인 경우
              if (doc.containsKey("menu")) {
                String menu = doc["menu"].as<String>();
                display.drawString(65, 11, menu);
                if (doc.containsKey("amount")) {
                  int amount = doc["amount"].as<int>();
                  display.drawString(20, 22, "Amount : ");
                  display.drawString(65, 22, String(amount));
                  display.display();
                }
              }
            }
          }
        }
      Serial.println(payload);
      }
      //EDGE 서버
      else {
        //EDGE서버-table3 주문
        http.begin(client1, "http://192.168.133.99:4400/get/order");
        int httpCode = http.GET();
        String payload1;
        String key;
        if (httpCode > 0) {
          payload1 = http.getString();
          StaticJsonDocument<200> doc1[0];
          DeserializationError error = deserializeJson(doc1[0], payload1);
          if (!error) {
            if (doc1[0].containsKey("table_id")) {
              int table_id = doc1[0]["table_id"].as<int>();
              if (table_id == 3) {
                // table_id = 3인 경우
                if (doc1[0].containsKey("menu")) {
                  String menu = doc1[0]["menu"].as<String>();
		              display.drawString(20,11,menu);
                  if (doc1[0].containsKey("amount")) {
                    int amount = doc1[0]["amount"].as<int>();                  		  
                    display.drawString(65, 11, String(amount));
                  }
                }
              }
            }
          
            Serial.println(payload1);
          }
          
        }
        http.end();
        //EDGE서버-table3 직원호출
        http.begin(client1, "http://192.168.133.99:4400/get/call");
        httpCode = http.GET();
        String payload2;
        if (httpCode > 0) {
          payload2 = http.getString();
          StaticJsonDocument<200> doc2[0];
          DeserializationError error = deserializeJson(doc2[0], payload2);
          if (!error) {
            if (doc2[0].containsKey("table_id")) {
              int table_id = doc2[0]["table_id"].as<int>();
              if (table_id == 3) {
                // table_id = 3인 경우
                if (doc2[0].containsKey("call")) {
                  String call = doc2[0]["call"].as<String>();
                  Serial.println(call);
		              display.drawString(20,22,"Call : ");
                  display.drawString(65,22, call);
                  display.display();
                  
                }
              }
            }
          }
          Serial.println(payload2);
        }  
        
        if (pressed == true) {
          http.begin(client1, "http://192.168.133.99:4400/clear");
          httpCode = http.GET();
          http.end();
          pressed = false;
        }
      } 
      // http통신 종료
      http.end();
      delay(1500);
      display.display();
    }
    //월간 매출
    else if (encoderValue > 29 && encoderValue < 40)
    {
      display.clear();
      display.drawString(35, 00, content);
      // HTTP GET 요청 보내기
      http.begin(client1, "http://3.216.219.9:4400/api/admin/sales/monthly");
      int httpCode = http.GET();
      String sales;
      String payload;
      String key;
      int value;
      if (httpCode > 0) {
        String payload = http.getString();
        StaticJsonDocument<200> doc;
        DeserializationError error = deserializeJson(doc, payload);

        JsonObject obj = doc.as<JsonObject>();
        for (JsonPair kv : obj) {
          key = kv.key().c_str();
          value = kv.value().as<int>();
          
          //"-" 이후의 문자열 추출
          int dashIndex = key.indexOf('-');
          if (dashIndex >= 0) {
            key = key.substring(dashIndex + 1);
          }
          sales = String(key) + " : " + String(value);
          Serial.println(sales);
        }
      }
      // http통신 종료
      http.end();
      delay(1500);
      display.drawString(20, 11, sales); //http.get값
      display.display();
    }
    //월간 고객수
    else if (encoderValue > 39 && encoderValue < 50)
    {
      display.clear();
      display.drawString(35, 00, content);
      // HTTP GET 요청 보내기
      http.begin(client1, "http://3.216.219.9:4400/api/admin/customer/monthly");
      int httpCode = http.GET();
      String count;
      String payload;
      String key;
      int value;
      if (httpCode > 0) {
        String payload = http.getString();
        StaticJsonDocument<200> doc;
        DeserializationError error = deserializeJson(doc, payload);

        JsonObject obj = doc.as<JsonObject>();
        for (JsonPair kv : obj) {
          key = kv.key().c_str();
          value = kv.value().as<int>();
          
          //"-" 이후의 문자열 추출
          int dashIndex = key.indexOf('-');
          if (dashIndex >= 0) {
            key = key.substring(dashIndex + 1);
          }
          count = String(key) + " : " + String(value);
          Serial.println(count);
        }
      }
      // http통신 종료
      http.end();
      delay(1500);
      display.drawString(35, 11, count); //http.get값
      display.display();
    }
    //베스트 메뉴
    else if (encoderValue > 49 && encoderValue < 60)
    {
      display.clear();
      display.drawString(35, 00, content);
      display.drawString(20, 11, "Menu : ");
       
      // HTTP GET 요청 보내기
      http.begin(client1, "http://3.216.219.9:4400/api/admin/populate");
      int httpCode = http.GET();
      String popular;
      if (httpCode > 0) {
        String payload = http.getString();
        StaticJsonDocument<200> doc;
        DeserializationError error = deserializeJson(doc, payload);

        popular = doc["Popular"].as<String>();
        Serial.println(popular);
      }
      // http통신 종료
      http.end();
      delay(1500);
      display.drawString(55, 11, popular); //http.get값
      display.display();        
    }
    client.loop();
    if ((pubInterval != 0) && (millis() - lastPublishMillis > pubInterval)) {
        lastPublishMillis = millis();
    }
}
