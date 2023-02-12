#include <SoftwareSerial.h>
#include <MPU9250_WE.h>
#include <Wire.h>
#define MPU9250_ADDR 0x68

MPU9250_WE mpu = MPU9250_WE(MPU9250_ADDR);

SoftwareSerial bluetooth(0,1);

void setup() 
{
    Serial.begin(115200);
    bluetooth.begin(115200);

    Wire.begin(); // IMU
    if(!mpu.init())
    {
      Serial.println("MPU9250 connection failed.");
    }
    else
    {
      Serial.println("MPU9250 is connected.");
    }

    Serial.println("Position sensor on a flat surface and do not move it.\nCalibrating...");
    delay(1000);
    mpu.autoOffsets();
    Serial.println("Done.");

    mpu.enableGyrDLPF();
    //mpu.disableGyrDLPF(MPU9250_BW_WO_DLPF_8800); // bandwidth without DLPF
    
    /*  Digital Low Pass Filter for the gyroscope must be enabled to choose the level. 
     *  MPU9250_DPLF_0, MPU9250_DPLF_2, ...... MPU9250_DPLF_7 
     *  
     *  DLPF    Bandwidth [Hz]   Delay [ms]   Output Rate [kHz]
     *    0         250            0.97             8
     *    1         184            2.9              1
     *    2          92            3.9              1
     *    3          41            5.9              1
     *    4          20            9.9              1
     *    5          10           17.85             1
     *    6           5           33.48             1
     *    7        3600            0.17             8
     *    
     *    Lowest noise using level 6  
     */
    mpu.setGyrDLPF(MPU9250_DLPF_6);
}

void loop() 
{
    xyzFloat gyr = mpu.getGyrValues();

    Serial.print(0);// 0:left | 1:right
    Serial.print(",");
    Serial.print(gyr.x);
    Serial.print(",");
    Serial.print(gyr.y);
    Serial.print(",");
    Serial.println(gyr.z);

    bluetooth.print(0);// 0:left | 1:right
    bluetooth.print(",");
    bluetooth.print(gyr.x);
    bluetooth.print(",");
    bluetooth.print(gyr.y);
    bluetooth.print(",");
    bluetooth.println(gyr.z);

    delay(50);
}
