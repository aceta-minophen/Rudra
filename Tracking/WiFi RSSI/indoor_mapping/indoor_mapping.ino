
#include "WiFi.h"

//#include "eloquent.h"

//using namespace Eloquent::DataStructures;

#define MAX_NETWORKS 10

double features[MAX_NETWORKS];
char *knownNetworks[MAX_NETWORKS] = {"paya1", "Airtel", "FTTH", "Jaishree", "www.excitel.com", "pwd555307", "TP-Link_B65C", "88Medha", "151*", "TanuAbhi136"};

void setup() {
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
}

void loop() {
    scan();
    printFeatures();
    delay(3000);
}

void scan() {
    int numNetworks = WiFi.scanNetworks();

    resetFeatures();

    // assign RSSIs to feature vector
    for (int i = 0; i < numNetworks; i++) {
        String ssid = WiFi.SSID(i);
        int networkIndex = getIndexByKey(ssid.c_str());

        // only create feature if the current SSID is a known one
        if (!isnan(networkIndex))
            features[networkIndex] = WiFi.RSSI(i);
    }
}

// reset all features to 0
void resetFeatures() {
    int numFeatures = sizeof(features) / sizeof(double);

    for (int i = 0; i < numFeatures; i++)
        features[i] = 0;
}
void printFeatures() {
    int numFeatures = sizeof(features) / sizeof(double);

    for (int i = 0; i < numFeatures; i++) {
        Serial.print(features[i]);
        Serial.print(i == numFeatures - 1 ? 'n' : ',');
    }
    Serial.println("");
}

int getIndexByKey( const char *key )
{
  for ( int i = 0; i < sizeof( knownNetworks ) / sizeof( char * ); i++ )
    if ( !strcmp( key, knownNetworks[i] ) )
      return i;
      
  return -1;
}
