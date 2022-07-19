#include "model.h"
#include "WiFi.h"
//#include "hello.h"

//#include "eloquent.h"
using namespace Eloquent;

Eloquent::ML::Port::SVM classifier;

#define MAX_NETWORKS 21

float features[MAX_NETWORKS];
char *knownNetworks[MAX_NETWORKS] = {"paya1", "Airtel", "FTTH", "Jaishree", "www.excitel.com", "pwd555307", "TP-Link_B65C", "88Medha", "151*", "TanuAbhi136", "JioFiber-Dinesh_4G", "Sunny", "DoozyPixie", "MALHOTRA", "ladoobala", "Rahul Iyer _ 2g", "BatCave", "157medha", "Sagar 1", "airtel171", "pranav4g"};

void setup()
{
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    // sayhello();
}

void loop()
{
    scan();
    printFeatures();
    classify();

    delay(500);
}

void classify()
{
    Serial.print("You are in ");

    Serial.println(classifier.predictLabel(features));
}

void scan()
{
    int numNetworks = WiFi.scanNetworks();

    resetFeatures();

    // assign RSSIs to feature vector
    for (int i = 0; i < numNetworks; i++)
    {
        String ssid = WiFi.SSID(i);
        // Serial.println(ssid);
        int networkIndex = getIndexByKey(ssid.c_str());

        // only create feature if the current SSID is a known one
        if (!isnan(networkIndex))
            features[networkIndex] = WiFi.RSSI(i);
    }
}

// reset all features to 0
void resetFeatures()
{
    int numFeatures = sizeof(features) / sizeof(double);

    for (int i = 0; i < numFeatures; i++)
        features[i] = 0;
}
void printFeatures()
{
    int numFeatures = sizeof(features) / sizeof(double);

    for (int i = 0; i < numFeatures; i++)
    {
        Serial.print(features[i]);
        Serial.print(i == numFeatures - 1 ? 'n' : ',');
    }
    Serial.println("");
}

int getIndexByKey(const char *key)
{
    for (int i = 0; i < sizeof(knownNetworks) / sizeof(char *); i++)
        if (!strcmp(key, knownNetworks[i]))
            return i;

    return -1;
}
