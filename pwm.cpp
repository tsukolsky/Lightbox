#include <iostream>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <wiringPi.h>
#include <softPwm.h>
#include <signal.h>

using namespace std;

#define NUM_OF_PINS 7;

//unsigned int literalPins[NUM_OF_PINS] 	= {7,11,12,13,15,16,18};
unsigned int wiringPiPins[NUM_OF_PINS]  = {7,0,1,2,3,4,5};

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


	int i = 0, numOfPins = NUM_OF_PINS;
	for (i = 0; i < numOfPins; i++)
	{
		pinMode(0, OUTPUT);
		digitalWrite(0,LOW);
		softPwmCreate(0, 0, 200);
		softPwmWrite(0,10);
	}
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
	for (i = 0; i < numOfPins; i++)
	{
		softPwmWrite(wiringPiPins[i],0);
		digitalWrite(wiringPiPins[i],LOW);
	}
	delay(100);
	exit(0);
}
