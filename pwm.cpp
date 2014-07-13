#include <iostream>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <wiringPi.h>
#include <softPwm.h>

using namespace std;

int main(int argc, char* argv[])
{
	if (argc != 3)
	{
		cout << "Too few input arguments, need pin number and duty cycle" << endl;
		return 0;
	}
	else
	{
		cout << "Input args are " << argv[1] << " and " << argv[2] << endl;
		//return  0;
	}

	// Get the pin number
	int pinNumber;
    pinNumber = atoi(argv[1]);
	cout << "Pin number is " << pinNumber << endl;

	// Get the intensity
	int intensity;
	intensity = atoi(argv[2]);
	cout << "Intensity is " << intensity << endl;

	if (wiringPiSetup() == -1)
	{
		cout << "Unable to setup wiring pi!" << endl;
		return 0;
	}

	pinMode(pinNumber, OUTPUT);
	digitalWrite(pinNumber,LOW);
	if (softPwmCreate(pinNumber, intensity) == 0)
	{
		cout << "Started successfully!" << endl;
	}
	else
	{
		cout << "Unable to start PWM!" << endl;
	}
	return 0;
}
