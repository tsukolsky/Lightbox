#include <iostream>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <wiringPi.h>
#include <softPwm.h>
#include <signal.h>

using namespace std;

//#define TEST

#define NUM_OF_PINS 7

int main(int argc, char* argv[])
{
	const unsigned int wiringPiPins[NUM_OF_PINS]  = {7,0,1,2,3,4,5};
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

	(void)signal(SIGINT,control_event);
	(void)signal(SIGQUIT,control_event);

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


#ifdef TEST
	int i = 0, numOfPins = NUM_OF_PINS;
	for (i = 0; i < numOfPins; i++)
	{
		pinMode(wiringPiPins[i], OUTPUT);
		digitalWrite(wiringPiPins[i],LOW);
		softPwmCreate(wiringPiPins[i], 0, intensity);
		softPwmWrite(wiringPiPins[i],intensity);
	}
#else
	pinMode(pinNumber, OUTPUT);
	digitalWrite(pinNumber, LOW);
	softPwmCreate(pinNumber, 0, intensity);
	softPwmWrite(pinNumber, intensity);
#endif
	while(1)
	{
		delay(10);
	}

	return 0;
}

void control_event(int sig)
{
	cout << "Exit called" << endl;
	int i = 0;
	int numOfPins = NUM_OF_PINS;
	const unsigned int wiringPiPins[NUM_OF_PINS]  = {7,0,1,2,3,4,5};

	for (i = 0; i < numOfPins; i++)
	{
		softPwmWrite(wiringPiPins[i],0);
		digitalWrite(wiringPiPins[i],LOW);
	}
	delay(100);
	exit(0);
}
