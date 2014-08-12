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

const unsigned int wiringPiPins[NUM_OF_PINS]  = {7,0,1,2,3,4,5};

void control_event(int sig);

void show_fixed_pattern(unsigned int intensity, unsigned int color)
{
	pinMode(wiringPiPins[color], OUTPUT);
	digitalWrite(wiringPiPins[color], LOW);
	softPwmCreate(wiringPiPins[color], 0, RANGE_120HZ);

	// Start the continous signal
	softPwmWrite(wiringPiPins[color],intensity);
	while (1)
	{
		delay(100);
	}
}

void show_tri_color_pattern(unsigned int intensity, unsigned int colorOne, unsigned int strobe_list_one[], unsigned int listOneSize, \
		unsigned int colorTwo, unsigned int strobe_list_two[], unsigned int listTwoSize, unsigned int colorThree, unsigned int strobe_list_three[], unsigned int listThreeSize)
{
	cout << "In tri color pattern" << endl;
	if (colorOne == -1 || colorTwo == -1 || colorThree == -1)
	{
		cout << "Bad colors. Cant be -1" << endl;
		return;
	}

	pinMode(wiringPiPins[colorOne], OUTPUT);
	pinMode(wiringPiPins[colorTwo], OUTPUT);
	pinMode(wiringPiPins[colorThree], OUTPUT);

	digitalWrite(wiringPiPins[colorOne], LOW);
	digitalWrite(wiringPiPins[colorTwo], LOW);
	digitalWrite(wiringPiPins[colorThree], LOW);

	softPwmCreate(wiringPiPins[colorOne], 0, RANGE_120HZ);
	softPwmCreate(wiringPiPins[colorTwo], 0, RANGE_120HZ);
	softPwmCreate(wiringPiPins[colorThree], 0, RANGE_120HZ);

	unsigned int on_dur = 0;
	unsigned int off_dur = 0;

	while(1)
	{
		for (int i = 0; i < listOneSize; i+=2)
		{
			on_dur = strobe_list_one[i];
			off_dur = strobe_list_one[i+1];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[colorOne], intensity);				// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[colorOne], 0);						// Turns strobe off
			delay(off_dur);
		}
		for (int j = 0; j < listTwoSize; j+=2)
		{
			on_dur = strobe_list_two[j];
			off_dur = strobe_list_two[j+1];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[colorTwo], intensity);				// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[colorTwo], 0);						// Turns strobe off
			delay(off_dur);
		}
		for (int k = 0; k < listThreeSize; k+=2)
		{
			on_dur = strobe_list_three[k];
			off_dur = strobe_list_three[k];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[colorThree], intensity);				// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[colorThree], 0);						// Turns strobe off
			delay(off_dur);
		}
	}
}

void show_dual_color_pattern(unsigned int intensity, unsigned int colorOne, unsigned int strobe_list_one[], unsigned int listOneSize, \
		unsigned int colorTwo, unsigned int strobe_list_two[], unsigned int listTwoSize)
{
	cout << "In dual color pattern" << endl;

	if (colorOne == -1 || colorTwo == -1)
	{
		cout << "Bad colors. Cant be -1" << endl;
		return;
	}

	pinMode(wiringPiPins[colorOne], OUTPUT);
	pinMode(wiringPiPins[colorTwo], OUTPUT);

	digitalWrite(wiringPiPins[colorOne], LOW);
	digitalWrite(wiringPiPins[colorTwo], LOW);

	softPwmCreate(wiringPiPins[colorOne], 0, RANGE_120HZ);
	softPwmCreate(wiringPiPins[colorTwo], 0, RANGE_120HZ);

	unsigned int on_dur = 0;
	unsigned int off_dur = 0;

	while(1)
	{
		for (int i = 0; i < listOneSize; i+=2)
		{
			on_dur = strobe_list_one[i];
			off_dur = strobe_list_one[i+1];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[colorOne], intensity);				// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[colorOne], 0);						// Turns strobe off
			delay(off_dur);
		}
		for (int j = 0; j < listTwoSize; j+=2)
		{
			on_dur = strobe_list_two[j];
			off_dur = strobe_list_two[j+1];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[colorTwo], intensity);				// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[colorTwo], 0);						// Turns strobe off
			delay(off_dur);
		}
	}
}

void show_single_color_pattern(unsigned int intensity, unsigned int color, unsigned int strobe_list[], unsigned int listSize)
{
	cout << "In single color pattern" << endl;

	if (color == -1)
	{
		cout << "Color is -1, bad" << endl;
		return;
	}

	pinMode(wiringPiPins[color], OUTPUT);
	digitalWrite(wiringPiPins[color], LOW);
	softPwmCreate(wiringPiPins[color], 0, RANGE_120HZ);

	for (int i = 0; i < listSize; i++)
	{
		cout << "List Entry " << i << " = " << strobe_list[i] << endl;
	}
	unsigned int on_dur = 0;
	unsigned int off_dur = 0;
	while(1)
	{
		for (int i = 0; i < listSize; i+=2)
		{
			on_dur = strobe_list[i];
			off_dur = strobe_list[i+1];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[color], intensity);			// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[color], 0);						// Turns strobe off
			delay(off_dur);

		}
	}
}


int main(int argc, char* argv[])
{
	/* ARGV: 1->Color One, 2->Color Two, 3->Color Three, 4->Intensity, 5->Pattern	*/

	//const unsigned int wiringPiPins[NUM_OF_PINS]  = {7,0,1,2,3,4,5};
	if (argc != 6)
	{
		cout << "Too few input arguments, need three pins and duty cycle: " << argc << endl;
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

	if (colorOne == -1)
	{
		cout << "Color one is bad." << endl;
		return false;
	}
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

	float intensityPerc = intensity/100.0;
	int newIntensity = RANGE_120HZ*intensityPerc;
	cout << "Intensity Percentage is " << intensityPerc << ", final intensity is " << newIntensity << endl;

#ifdef TEST
	int i = 0, numOfPins = NUM_OF_PINS;
	for (i = 0; i < numOfPins; i++)
	{
		pinMode(wiringPiPins[i], OUTPUT);
		digitalWrite(wiringPiPins[i],LOW);
		softPwmCreate(wiringPiPins[i], 0, 10);
		softPwmWrite(wiringPiPins[i],10);
	}
	while(1)
	{
		delay(100);
	}
#else
	switch(pattern)
	{
	case HZ4:
		show_single_color_pattern(newIntensity, colorOne, pwm::hz_4, sizeof(pwm::hz_4)/sizeof(unsigned int));
		break;
	case HZ4_ALT:
		show_dual_color_pattern(newIntensity, colorOne, pwm::hz_4, sizeof(pwm::hz_4)/sizeof(unsigned int), \
				colorTwo, pwm::hz_4, sizeof(pwm::hz_4)/sizeof(unsigned int));
		break;
	case HZ4_INT:
		show_single_color_pattern(newIntensity, colorOne, pwm::four_three_interrupt, sizeof(pwm::four_three_interrupt)/sizeof(unsigned int));
		break;
	case HZ4_ALT_INT:
		show_dual_color_pattern(newIntensity, colorOne, pwm::four_three_cOne, sizeof(pwm::four_three_cOne)/sizeof(unsigned int), \
				colorTwo, pwm::four_three_cTwo, sizeof(pwm::four_three_cTwo)/sizeof(unsigned int));
		break;
	case HZ6:
		show_single_color_pattern(newIntensity, colorOne, pwm::hz_6, sizeof(pwm::hz_6)/sizeof(unsigned int));
		break;
	case SOS_MOD:
		show_single_color_pattern(newIntensity, colorOne, pwm::sos_mod, sizeof(pwm::sos_mod)/sizeof(unsigned int));
		break;
	case CHIRP:
		show_single_color_pattern(newIntensity, colorOne, pwm::chirpup, sizeof(pwm::chirpup)/sizeof(unsigned int));
		break;
	case CHIRP_3:
		show_tri_color_pattern(newIntensity, colorOne, pwm::chirpup_cOne, sizeof(pwm::chirpup_cOne)/sizeof(unsigned int), \
				colorTwo, pwm::chirpup_cTwo, sizeof(pwm::chirpup_cTwo)/sizeof(unsigned int), \
				colorThree, pwm::chirpup_cThree, sizeof(pwm::chirpup_cThree)/sizeof(unsigned int));
		break;
	case HZ2_50:
		show_single_color_pattern(newIntensity, colorOne, pwm::hz_2_50, sizeof(pwm::hz_2_50)/sizeof(unsigned int));
		break;
	case HZ2_25:
		show_single_color_pattern(newIntensity, colorOne, pwm::hz_2_25, sizeof(pwm::hz_2_25)/sizeof(unsigned int));
		break;
	case HZ2_25_INT:
		cout << "2Hz, 25% Interrupt Duty." << endl;
		show_dual_color_pattern(newIntensity, colorOne, pwm::hz_2_25_int_cOne, sizeof(pwm::hz_2_25_int_cOne)/sizeof(unsigned int), \
				colorTwo, pwm::hz_2_25_int_cTwo, sizeof(pwm::hz_2_25_int_cTwo)/sizeof(unsigned int));
		break;
	case HZ2_50_ALT:
		cout << "2Hz, 50% Duty." << endl;
		show_dual_color_pattern(newIntensity, colorOne, pwm::hz_2_50, sizeof(pwm::hz_2_50)/sizeof(unsigned int), \
				colorTwo, pwm::hz_2_50, sizeof(pwm::hz_2_50)/sizeof(unsigned int));
		break;
	case FIXED:
		cout << "Fixed" << endl;
		show_fixed_pattern(newIntensity, colorOne);
		break;
	default:
		break;
	}
#endif

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
