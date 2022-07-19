#include "model.h"

void loop() {
    scan();
    classify();
    delay(3000);
}

void classify() {
    Serial.print("You are in ");
    Serial.println(classIdxToName(predict(features)));
}
