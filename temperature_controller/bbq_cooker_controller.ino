#include <SPI.h>
#include "Adafruit_MAX31855.h"
#include <WiFiS3.h>

// Define the pins used for the SPI connection
int thermoDO = 12;
int thermoCS = 10;
int thermoCLK = 13;
Adafruit_MAX31855 thermocouple(thermoCLK, thermoCS, thermoDO);

// WiFi credentials (replace with yours)
const char* ssid = "ATT9lrZ6zY24";
const char* password = "33adc7t%4zbn";

WiFiServer server(80);  // Web server on port 80

void setup() {
  Serial.begin(9600);

  pinMode(2, OUTPUT);

  while (!Serial)
    ;  // Wait for serial monitor (optional)

  // Initialize MAX31855
  if (!thermocouple.begin()) {
    Serial.println("Thermocouple not connected correctly!");
    while (1) delay(500);
  }
  Serial.println("MAX31855 initialized.");

  // Connect to WiFi
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  // Wait for valid IP (fixes 0.0.0.0 issue)
  Serial.print("Waiting for IP address...");
  while (WiFi.localIP() == IPAddress(0, 0, 0, 0)) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nIP address assigned!");

  // Print actual LAN IP
  Serial.print("My LAN IP address: ");
  Serial.println(WiFi.localIP());

  // Start web server
  server.begin();
  Serial.println("Web server started. Open IP in browser.");
}

void loop() {
  // Read temperature
  double temperature = thermocouple.readCelsius();
  String tempStr = isnan(temperature) ? "Error reading temperature!" : String(temperature, 2) + " °C";

  if (temperature >= 20) {
    digitalWrite(2, HIGH);
  } else {
    digitalWrite(2, LOW);
  }
  Serial.print("temp is: ");
  Serial.println(temperature);
  
  WiFiClient client = server.available();  // Listen for clients

  if (client) {
    // Serial.println("New client connected.");
    String request = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        request += c;
        if (c == '\n') {  // End of request line
          // Send HTTP response header
          client.println("HTTP/1.1 200 OK");
          client.println("Content-type:text/html");
          client.println("Connection: close");
          client.println();


          // Send HTML page
          client.println("<!DOCTYPE html>");
          client.println("<html><head><title>Thermocouple Temp</title>");
          // client.println("<meta http-equiv=\"refresh\" content=\"5\">");  // Auto-refresh every 5s
          client.println("</head><body>");
          client.println("<h1>Thermocouple Temperature</h1>");
          client.println("<p><strong>Temperature: " + tempStr + "</strong></p>");
          client.println("<p>Page refreshes every 5 seconds.</p>");
          client.println("</body></html>");

          client.println();
          client.stop();
          break;
        }
      }
    }
    delay(10);
    // client.stop();
    // Serial.println("Client disconnected.");
  }
}