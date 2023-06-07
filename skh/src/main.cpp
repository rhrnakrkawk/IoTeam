#include <Arduino.h>
#include <IO7F8266.h>
#include <SSD1306.h>
#include <ArduinoJson.h>
#include <string>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <vector>
// HTTPClient http;
// WiFiClient wificlient;
const int pulseA = 12;
const int pulseB = 13;
const int pushSW = 2;
volatile int lastEncoded = 0;
volatile int encoderValue = 0;
volatile bool pressed = false;

const char *ssid = "heesane";
const char *pass = "97289728";
SSD1306 display(0x3c, 4, 5, GEOMETRY_128_32);

HTTPClient http;
HTTPClient httppost;
HTTPClient orderhttp;
HTTPClient edge_orderhttp;

WiFiClient clientGet;
WiFiClient clientPost;
WiFiClient orderclient;
WiFiClient edge_orderclient;

int amounts[10];
int menu = 0;
int first_price = 0;
int second_price = 0;
int third_price = 0;
int total_price = 0;
int person_num = 0;
int amount_num = 0;
int num;

String user_html = "";
String staff_content = "";
String number = "";
String number2 = "";
String price = "";
String content = "";
String person = "";
String names[3];
int prices[3];
String price_display[3];
int table_id = 1;       // 아두이노별로 다르게할것
String table_id1 = "1"; // 아두이노별로 다르게할것
boolean order_flag = false;
boolean staff_flag = false;
boolean person_Post = false;
boolean pay_post = false;

unsigned long lastPublishMillis = -pubInterval;
char *ssid_pfix = (char *)"skh_button";
void contentpush()
{
  if (encoderValue < 10)
  {
    content = "Spoon";
  }
  else if (encoderValue > 9 && encoderValue < 20)
  {
    content = "Chopsticks";
  }
  else if (encoderValue > 19 && encoderValue < 30)
  {
    content = "Water";
  }
  else if (encoderValue > 29 && encoderValue < 40)
  {
    content = "Tissue";
  }
  else if (encoderValue > 39 && encoderValue < 60)
  {
    content = "Staff Call";
  }
  else if (encoderValue > 59)
  {
    encoderValue = 0;
  }
}

void number2push()
{
  if (encoderValue < 10)
  {
    number2 = "1";
  }
  else if (encoderValue > 9 && encoderValue < 20)
  {

    number2 = "2";
  }
  else if (encoderValue > 19 && encoderValue < 30)
  {

    number2 = "3";
  }
  else if (encoderValue > 29 && encoderValue < 40)
  {

    number2 = "4";
  }
  else if (encoderValue > 39 && encoderValue < 50)
  {

    number2 = "5";
  }
  else if (encoderValue > 49 && encoderValue < 70)
  {

    number2 = "6";
  }
  else if (encoderValue > 69)
  {
    encoderValue = 0;
  }
}
void numberpush()
{
  if (encoderValue < 10)
  {
    number = "1";
    amount_num = 1;
    num = 1;
  }
  else if (encoderValue > 9 && encoderValue < 20)
  {
    number = "2";
    amount_num = 2;
    num = 2;
  }
  else if (encoderValue > 19 && encoderValue < 30)
  {
    number = "3";
    amount_num = 3;
    num = 3;
  }
  else if (encoderValue > 29 && encoderValue < 40)
  {
    number = "4";
    amount_num = 4;
    num = 4;
  }
  else if (encoderValue > 39 && encoderValue < 50)
  {
    number = "5";
    amount_num = 5;
    num = 5;
  }
  else if (encoderValue > 49 && encoderValue < 70)
  {
    number = "6";
    amount_num = 6;
    num = 6;
  }
  else if (encoderValue > 69)
  {
    encoderValue = 0;
  }
}
void person_numberpush()
{
  if (encoderValue < 10)
  {
    person = "1";
    person_num = 1;
  }
  else if (encoderValue > 9 && encoderValue < 20)
  {
    person = "2";
    person_num = 2;
  }
  else if (encoderValue > 19 && encoderValue < 30)
  {
    person = "3";
    person_num = 3;
  }
  else if (encoderValue > 29 && encoderValue < 50)
  {
    person = "4";
    person_num = 4;
  }
  else if (encoderValue > 49)
  {
    encoderValue = 0;
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
  if (encoderValue > 255)
  {
    encoderValue = 255;
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

boolean edge_OrderPost(int number_1) // 엣지서버 http통신
{
  if (order_flag == true)
  {

    String edge_server = "http://192.168.133.99:4400/order?";
    String edge_tableid = "table_id=" + table_id1 + "&";
    String edge_menu = "menu=" + names[number_1] + "&";
    String edge_quantity = "amount=" + number;
    String edge = "http://192.168.133.99:4400/order?" + edge_tableid + edge_menu + edge_quantity;
    Serial.println(edge);
    edge_orderhttp.begin(edge_orderclient, edge);
    order_flag = false;

    int edge_httpResponseCode = edge_orderhttp.GET();

    if (edge_httpResponseCode > 0)
    {
      Serial.println(edge_httpResponseCode);
      edge_orderhttp.end();
      delay(300);
      return true;
    }
    else
    {
      Serial.print("Error code: ");
      Serial.println(edge_httpResponseCode);
      edge_orderhttp.end();
      return false;
    }
  }
  if (staff_flag == true)
  {

    staff_flag = false;
    staff_content = content + number2;
    String edge_server = "http://192.168.133.99:4400/call?";
    String edge_tableid = "table_id=" + table_id1;
    String edge_call = "&call=" + staff_content;
    String edge = edge_server + edge_tableid + edge_call;
    edge_orderhttp.begin(edge_orderclient, edge);
    Serial.println(edge);
    int edge_httpResponseCode = edge_orderhttp.GET();

    if (edge_httpResponseCode > 0)
    {
      Serial.println(edge_httpResponseCode);
      edge_orderhttp.end();
      delay(300);
      return true;
    }
    else
    {
      Serial.print("Error code: ");
      Serial.println(edge_httpResponseCode);
      edge_orderhttp.end();
      return false;
    }
  }
  else
    return false;
}

boolean OrderPost(int number) // 주문 서버에 전송
{
  if (order_flag == true)
  {
    order_flag = false;
    StaticJsonDocument<512> jsonDoc;
    jsonDoc["table_id"] = table_id;
    JsonArray menus = jsonDoc.createNestedArray("menus");
    JsonObject menu1 = menus.createNestedObject();
    menu1["food_name"] = names[number];
    menu1["amount"] = amount_num;
    jsonDoc["is_paid"] = "false";
    serializeJsonPretty(jsonDoc, Serial);

    orderhttp.begin(orderclient, "http://3.216.219.9:4400/api/orders/create");
    orderhttp.addHeader("Content-Type", "application/json");

    String jsonString;
    serializeJson(jsonDoc, jsonString);
    int httpResponseCode = orderhttp.POST(jsonString);
    // int httpResponseCode = -1; // 엣지서버 테스트용
    if (httpResponseCode > 0)
    {
      String response = orderhttp.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
      orderhttp.end();
      delay(300);
      return true;
    }
    else // 본서버에 문제가 생겼을시 엣지서버로 주문전송
    {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
      orderhttp.end();
      if (menu == 1)
      {
        order_flag = true;
        Serial.println("menu1");
        edge_OrderPost(1);
      }
      if (menu == 2)
      {
        order_flag = true;
        Serial.println("menu2");
        edge_OrderPost(2);
      }
      if (menu == 3)
      {
        order_flag = true;
        Serial.println("menu3");
        edge_OrderPost(3);
      }

      return false;
    }
  }
  if (staff_flag == true)
  {
    staff_flag = false;
    StaticJsonDocument<512> jsonDoc;

    staff_content = content + " " + number2;
    jsonDoc["table_id"] = table_id;
    jsonDoc["call"] = "true";
    jsonDoc["content"] = staff_content;
    jsonDoc["is_paid"] = "false";

    serializeJsonPretty(jsonDoc, Serial);

    orderhttp.begin(orderclient, "http://3.216.219.9:4400/api/orders/call");
    orderhttp.addHeader("Content-Type", "application/json");

    String jsonString;
    serializeJson(jsonDoc, jsonString);
    int httpResponseCode = orderhttp.POST(jsonString);
    // int httpResponseCode = -1; // 엣지서버 테스트용
    if (httpResponseCode > 0)
    {
      String response = orderhttp.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
      orderhttp.end();
      delay(300);
      return true;
    }
    else // 본서버에 문제가 생겼을시 엣지서버로 직원호출전송
    {
      staff_flag = true;
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
      Serial.println("error_call");
      orderhttp.end();
      edge_OrderPost(0);
      return false;
    }
  }
  else
    return false;
}

boolean PersonPost() // 서버에 사람수 POST
{
  if (person_Post == true)
  {
    person_Post = false;
    StaticJsonDocument<512> root;
    JsonObject data = root.to<JsonObject>();
    data["table_id"] = table_id; // 테이브랑이디;
    data["customer_count"] = person_num;
    data["total_price"] = 0;

    httppost.begin(clientPost, "http://3.216.219.9:4400/api/tables/create");
    httppost.addHeader("Content-Type", "application/json");

    String jsonString;
    serializeJson(root, jsonString);
    int httpResponseCode = httppost.POST(jsonString);

    serializeJsonPretty(data, Serial);
    if (httpResponseCode > 0)
    {
      String response = httppost.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
      httppost.end();
      delay(300);
      return true;
    }
    else
    {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
      httppost.end();
      return false;
    }
  }
  if (pay_post == true)
  {
    pay_post = false;
    StaticJsonDocument<512> root;
    JsonObject data = root.to<JsonObject>();
    data["table_id"] = table_id;
    data["is_paid"] = true;
    String serveradr = "http://3.216.219.9:4400/api/tables/pay/" + table_id1;
    httppost.begin(clientPost, serveradr); // 나중에 숫자 1로 바꿀것
    httppost.addHeader("Content-Type", "application/json");

    // String jsonString1;
    // serializeJson(root, jsonString1);
    int httpResponseCode = httppost.GET();

    serializeJsonPretty(data, Serial);
    if (httpResponseCode > 0)
    {
      Serial.println(httpResponseCode);
      httppost.end();
      delay(300);
      return true;
    }
    else
    {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
      httppost.end();
      return false;
    }
  }
  else
    return false;
}

boolean GetFoodList() // 기기를 켜면 부팅되면서 서버에서 메뉴를 가져옴
{
  http.begin(clientGet, "http://3.216.219.9:4400/api/foods/list");

  int httpCode = http.GET();
  // 응답받기
  if (httpCode > 0)
  {
    String payload = http.getString();
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, payload);

    JsonArray foodList = doc["food_list"];

    int index = 0;

    for (JsonObject food : foodList)
    {

      names[index] = food["name"].as<String>();
      prices[index] = food["price"].as<int>();
      price_display[index] = food["price"].as<String>();
      index++;
    }

    // 배열에 저장된 값들을 출력 또는 사용

    delay(100);
    http.end();
    return true;
  }
  else
  {
    Serial.printf("오류발생\n");
    return false;
  }
}
boolean PersonDisplay() // 테이블 생성을 위해 사람수를 먼저 입력
{
  while (true)
  {
    Serial.println(encoderValue);
    delay(400);
    person_numberpush();
    display.clear();
    display.drawString(35, 0, "person");
    display.drawString(80, 0, person);
    display.display();
    if (pressed == true)
    {
      person_Post = true;
      pressed = false;
      delay(200);
      encoderValue = 0;
      PersonPost(); // 서버에 사람수 POST
      delay(500);
      break;
    }
  }
  return true;
}

boolean menuAmout() // 메뉴 양 선택 및 가격oled출력
{
  while (true)
  {
    delay(500);
    Serial.println(encoderValue);
    numberpush();
    if (menu == 1)
    {
      total_price = prices[0] * num;
      price = String(total_price);
      display.clear();
      display.drawString(35, 0, names[0]);
      display.drawString(0, 10, "Menu num: ");
      display.drawString(55, 10, number);
      display.drawString(0, 20, "Price:");
      display.drawString(55, 20, price);
      display.display();
      if (pressed == true)
      {
        pressed = false;
        order_flag = true;
        OrderPost(0); // 주문 서버에 전송
        encoderValue = 0;
        return true;
      }
    }
    if (menu == 2)
    {
      total_price = prices[1] * num;
      price = String(total_price);
      display.clear();
      display.drawString(35, 0, names[1]);
      display.drawString(0, 10, "Menu num: ");
      display.drawString(55, 10, number);
      display.drawString(0, 20, "Price:");
      display.drawString(55, 20, price);
      display.display();
      if (pressed == true)
      {
        pressed = false;
        order_flag = true;
        OrderPost(1); // 주문 서버에 전송
        encoderValue = 0;
        return true;
      }
    }
    if (menu == 3)
    {
      total_price = prices[2] * num;
      price = String(total_price);
      display.clear();
      display.drawString(35, 0, names[2]);
      display.drawString(0, 10, "Menu num: ");
      display.drawString(55, 10, number);
      display.drawString(0, 20, "Price:");
      display.drawString(55, 20, price);
      display.display();
      if (pressed == true)
      {
        pressed = false;
        order_flag = true;
        OrderPost(2); // 주문 서버에 전송
        encoderValue = 0;
        return true;
      }
    }
  }
}

boolean stfAmount() // 숟가락이나 젓가락 같이 개수가 필요한 호출
{
  while (true)
  {
    delay(800);
    Serial.println(encoderValue);
    number2push();
    display.clear();
    display.drawString(35, 0, "Staff call");
    display.drawString(0, 10, "Content: ");
    display.drawString(50, 10, content);
    display.drawString(0, 20, "Count:");
    display.drawString(50, 20, number2);
    display.display();
    if (pressed == true)
    {
      staff_flag = true;
      pressed = false;
      encoderValue = 0;
      OrderPost(0); // 직원호출을 서버에 올리는 함수
      return true;
    }
  }
}
boolean stfCall()
{
  while (true)
  {
    Serial.println(encoderValue);
    delay(400);
    contentpush();
    display.clear();
    display.drawString(35, 0, "Staff call");
    display.drawString(0, 10, "Content: ");
    display.drawString(50, 10, content);
    display.display();
    if (pressed == true && (content == "Spoon" || content == "Chopsticks"))
    {
      pressed = false;
      delay(100);
      encoderValue = 0;
      stfAmount();
      return true;
    }
    else if (pressed == true)
    {
      pressed = false;
      delay(100);
      encoderValue = 0;
      staff_flag = true;
      OrderPost(0);
      return true;
    }
  }
}

boolean menuSelect() // 메뉴,직원호출,결제
{
  while (true)
  {
    delay(800);
    Serial.printf("encoder value: %d \n", encoderValue);
    if (encoderValue < 10) // 첫번째메뉴
    {
      delay(500);
      display.clear();
      display.drawString(35, 0, names[0]);
      display.drawString(35, 20, price_display[0]);
      display.display();
      if (pressed == true)
      {
        pressed = false;
        delay(200);
        encoderValue = 0;
        delay(400);
        menu = 1;
        menuAmout();
      }
    }
    else if (encoderValue > 9 && encoderValue < 20) // 두번째메뉴
    {
      delay(500);
      display.clear();
      display.drawString(35, 0, names[1]);
      display.drawString(35, 20, price_display[1]);
      display.display();
      if (pressed == true)
      {
        pressed = false;
        delay(200);
        encoderValue = 0;
        delay(400);
        menu = 2;
        menuAmout();
      }
    }
    else if (encoderValue > 19 && encoderValue < 30) // 세번째메뉴
    {
      delay(500);
      display.clear();
      display.drawString(35, 0, names[2]);
      display.drawString(35, 20, price_display[2]);
      display.display();
      if (pressed == true)
      {
        pressed = false;
        delay(200);
        encoderValue = 0;
        delay(400);
        menu = 3;
        menuAmout();
      }
    }
    else if (encoderValue > 29 && encoderValue < 40)
    {
      delay(500);
      display.clear();
      display.drawString(35, 0, "Staff call"); // 스태프호출
      display.display();
      if (pressed == true)
      {
        pressed = false;
        delay(200);
        encoderValue = 0;
        stfCall();
      }
    }
    else if (encoderValue > 39 && encoderValue < 50)
    {
      delay(500);
      display.clear();
      display.drawString(35, 0, "pay"); // 결제하고 나가기 > 테이블 초기화
      display.display();
      if (pressed == true)
      {
        pressed = false;
        delay(200);
        encoderValue = 0;
        pay_post = true;
        PersonPost();
        return true;
      }
    }
    else if (encoderValue > 59)
    {
      encoderValue = 0;
    }
  }
}

void setup()
{
  Serial.begin(115200);
  pinMode(pushSW, INPUT_PULLUP);
  pinMode(pulseA, INPUT_PULLUP);
  pinMode(pulseB, INPUT_PULLUP);
  attachInterrupt(pushSW, buttonClicked, FALLING);
  attachInterrupt(pulseA, handleRotary, CHANGE);
  attachInterrupt(pulseB, handleRotary, CHANGE);
  initDevice();

  WiFi.mode(WIFI_STA);
  WiFi.begin((const char *)cfg["ssid"], (const char *)cfg["w_pw"]);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  // main setup
  Serial.printf("\nIP address : ");
  Serial.println(WiFi.localIP());
  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);
  display.display();
  GetFoodList();
}

void loop()
{

  delay(200);

  PersonDisplay();

  delay(200);
  menuSelect();
}