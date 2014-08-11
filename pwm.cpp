#include <iostream>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <wiringPi.h>
#include <softPwm.h>
#include <signal.h>
#include "pwm.h"

using namespace std;

//#define TEST

#define PERIOD_MS		10
#define ONE_MS			10
#define RANGE_120HZ		8*ONE_MS
#define NUM_OF_PINS 	7

void control_event(int sig);

int main(int argc, char* argv[])
{
	/* ARGV: 1->Color One, 2->Color Two, 3->Color Three, 4->Intensity, 5->Pattern	*/

	const unsigned int wiringPiPins[NUM_OF_PINS]  = {7,0,1,2,3,4,5};
	if (argc != 5)
	{
		cout << "Too few input arguments, need three pins and duty cycle" << endl;
		return 0;
	}
	else
	{
		cout << "Input args are " << argv[1] << ", " << argv[2] << ", " << argv[3] << " and " << argv[4] << " and " << argv[5] << endl;
		//return  0;
	}

	(void)signal(SIGINT,control_event);
	(void)signal(SIGQUIT,control_event);
	(void)signal(SIGKILL,control_event);
	(void)signal(SIGSTOP,control_event);
	(void)signal(SIGTERM,control_event);

	// Get the colors
	int colorOne, colorTwo, colorThree;
	colorOne = atoi(argv[1]);
	colorTwo = atoi(argv[2]);
	colorThree = atoi(argv[3]);
	cout << "Color one is " << colorOne << ", color two is " << colorTwo << ", color three is " << colorThree << endl;

	// Get the pattern: argv[5],  0-12
	int pattern;
	pattern = atoi(argv[5]);
	cout << "Pattern number is " << pattern << endl;

	// Get the intensity
	int intensity;
	intensity = atoi(argv[4]);
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
		softPwmCreate(wiringPiPins[i], 0, 10);
		softPwmWrite(wiringPiPins[i],10);
	}
#else
	pinMode(wiringPiPins[pinNumber], OUTPUT);
	digitalWrite(wiringPiPins[pinNumber], LOW);
	softPwmCreate(wiringPiPins[pinNumber], 0, RANGE_120HZ);

	float intensityPerc = intensity/100.0;
	int newIntensity = RANGE_120HZ*intensityPerc;
	cout << "Intensity Percentage is " << intensityPerc << ", final intensity is " << newIntensity << endl;

	softPwmWrite(wiringPiPins[pinNumber], newIntensity);
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
