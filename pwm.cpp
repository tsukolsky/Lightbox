#include <iostream>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <wiringPi.h>
#include <softPwm.h>
#include <signal.h>
#include "pwm.h"

using namespace std;

//#define TEST1
//#define TEST2

#define FREQ_100HZ		100
#define FREQ_120HZ		83
#define NUM_OF_PINS 	7

const unsigned int wiringPiPins[NUM_OF_PINS]  = {7,0,1,2,3,4,5};

void control_event(int sig);

int ConvertIntensity(unsigned int inputIntensity)
{
	float intensityPerc = inputIntensity/100.0;
	int newIntensity = FREQ_120HZ*intensityPerc;
	cout << "Intensity Percentage is " << intensityPerc << ", final intensity is " << newIntensity << endl;
	return newIntensity;

}

void show_fixed_pattern(unsigned int color, unsigned int intensity)
{
	pinMode(wiringPiPins[color], OUTPUT);
	digitalWrite(wiringPiPins[color], LOW);
	softPwmCreate(wiringPiPins[color], 0, FREQ_120HZ);

	int newIntensity = ConvertIntensity(intensity);
	// Start the continous signal
	softPwmWrite(wiringPiPins[color],newIntensity);
	while (1)
	{
		delay(100);
	}
}

void show_tri_color_pattern(unsigned int colorOne, unsigned int colorOneInt, unsigned int strobe_list_one[], unsigned int listOneSize, \
		unsigned int colorTwo, unsigned int colorTwoInt, unsigned int strobe_list_two[], unsigned int listTwoSize, \
		unsigned int colorThree, unsigned int colorThreeInt, unsigned int strobe_list_three[], unsigned int listThreeSize)
{
	cout << "In tri color pattern" << endl;
	if (colorOne == -1 || colorTwo == -1 || colorThree == -1)
	{
		cout << "Bad colors. Cant be -1" << endl;
		return;
	}

	int newColorOneIntensity = ConvertIntensity(colorOneInt);
	int newColorTwoIntensity = ConvertIntensity(colorTwoInt);
	int newColorThreeIntensity = ConvertIntensity(colorThreeInt);

	pinMode(wiringPiPins[colorOne], OUTPUT);
	pinMode(wiringPiPins[colorTwo], OUTPUT);
	pinMode(wiringPiPins[colorThree], OUTPUT);

	digitalWrite(wiringPiPins[colorOne], LOW);
	digitalWrite(wiringPiPins[colorTwo], LOW);
	digitalWrite(wiringPiPins[colorThree], LOW);

	softPwmCreate(wiringPiPins[colorOne], 0, FREQ_120HZ);
	softPwmCreate(wiringPiPins[colorTwo], 0, FREQ_120HZ);
	softPwmCreate(wiringPiPins[colorThree], 0, FREQ_120HZ);

	unsigned int on_dur = 0;
	unsigned int off_dur = 0;

	while(1)
	{
		for (int i = 0; i < listOneSize; i+=2)
		{
			on_dur = strobe_list_one[i];
			off_dur = strobe_list_one[i+1];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[colorOne], newColorOneIntensity);				// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[colorOne], 0);						// Turns strobe off
			delay(off_dur);
		}
		for (int j = 0; j < listTwoSize; j+=2)
		{
			on_dur = strobe_list_two[j];
			off_dur = strobe_list_two[j+1];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[colorTwo], newColorTwoIntensity);				// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[colorTwo], 0);						// Turns strobe off
			delay(off_dur);
		}
		for (int k = 0; k < listThreeSize; k+=2)
		{
			on_dur = strobe_list_three[k];
			off_dur = strobe_list_three[k];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[colorThree], newColorThreeIntensity);				// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[colorThree], 0);						// Turns strobe off
			delay(off_dur);
		}
	}
}

void show_dual_color_pattern(unsigned int colorOne, unsigned int colorOneInt, unsigned int strobe_list_one[], unsigned int listOneSize, \
		unsigned int colorTwo, unsigned int colorTwoInt, unsigned int strobe_list_two[], unsigned int listTwoSize)
{
	cout << "In dual color pattern" << endl;

	if (colorOne == -1 || colorTwo == -1)
	{
		cout << "Bad colors. Cant be -1" << endl;
		return;
	}

	int newColorOneIntensity = ConvertIntensity(colorOneInt);
	int newColorTwoIntensity = ConvertIntensity(colorTwoInt);

	pinMode(wiringPiPins[colorOne], OUTPUT);
	pinMode(wiringPiPins[colorTwo], OUTPUT);

	digitalWrite(wiringPiPins[colorOne], LOW);
	digitalWrite(wiringPiPins[colorTwo], LOW);

	softPwmCreate(wiringPiPins[colorOne], 0, FREQ_120HZ);
	softPwmCreate(wiringPiPins[colorTwo], 0, FREQ_120HZ);

	unsigned int on_dur = 0;
	unsigned int off_dur = 0;

	while(1)
	{
		for (int i = 0; i < listOneSize; i+=2)
		{
			on_dur = strobe_list_one[i];
			off_dur = strobe_list_one[i+1];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[colorOne], newColorOneIntensity);				// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[colorOne], 0);						// Turns strobe off
			delay(off_dur);
		}
		for (int j = 0; j < listTwoSize; j+=2)
		{
			on_dur = strobe_list_two[j];
			off_dur = strobe_list_two[j+1];
			//cout << "on duration " << on_dur << ", off duration " << off_dur << endl;
			softPwmWrite(wiringPiPins[colorTwo], newColorTwoIntensity);				// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[colorTwo], 0);						// Turns strobe off
			delay(off_dur);
		}
	}
}

void show_single_color_pattern(unsigned int color, unsigned int intensity, unsigned int strobe_list[], unsigned int listSize)
{
	cout << "In single color pattern" << endl;

	if (color == -1)
	{
		cout << "Color is -1, bad" << endl;
		return;
	}

	int newIntensity = ConvertIntensity(intensity);

	pinMode(wiringPiPins[color], OUTPUT);
	digitalWrite(wiringPiPins[color], LOW);
	softPwmCreate(wiringPiPins[color], 0, FREQ_120HZ);

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
			softPwmWrite(wiringPiPins[color], newIntensity);			// Turns strobe on
			delay(on_dur);
			softPwmWrite(wiringPiPins[color], 0);						// Turns strobe off
			delay(off_dur);

		}
	}
}


int main(int argc, char* argv[])
{
	/* ARGV: 1->Color One, 2->Color One PWM, 3->Color Two, 4->Color two pwm, 5->Color Three, 6->Color three pwm, 7->Pattern	*/

	//const unsigned int wiringPiPins[NUM_OF_PINS]  = {7,0,1,2,3,4,5};
	if (argc != 8)
	{
		cout << "Too few input arguments, need three pins, three intensities, and duty cycle and pattern: " << argc << endl;
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
	pattern = atoi(argv[7]);
	cout << "Pattern number is " << pattern << endl;

	// Get the intensity
	int intensityOne, intensityTwo, intensityThree;
	intensityOne = atoi(argv[4]);
	intensityTwo = atoi(argv[5]);
	intensityThree = atoi(argv[6]);
	cout << "Intensity is " << intensityOne << ", " << intensityTwo << ", " << intensityThree << endl;

	if (wiringPiSetup() == -1)
	{
		cout << "Unable to setup wiring pi!" << endl;
		return 0;
	}
	
#ifdef TEST1
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
		show_single_color_pattern( colorOne, intensityOne, pwm::hz_4, sizeof(pwm::hz_4)/sizeof(unsigned int));
		break;
	case HZ4_ALT:
		show_dual_color_pattern(colorOne, intensityOne, pwm::hz_4, sizeof(pwm::hz_4)/sizeof(unsigned int), \
				colorTwo, intensityTwo, pwm::hz_4, sizeof(pwm::hz_4)/sizeof(unsigned int));
		break;
	case HZ4_INT:
		show_single_color_pattern(colorOne, intensityOne, pwm::four_three_interrupt, sizeof(pwm::four_three_interrupt)/sizeof(unsigned int));
		break;
	case HZ4_ALT_INT:
		show_dual_color_pattern(colorOne, intensityOne, pwm::four_three_cOne, sizeof(pwm::four_three_cOne)/sizeof(unsigned int), \
				colorTwo, intensityTwo, pwm::four_three_cTwo, sizeof(pwm::four_three_cTwo)/sizeof(unsigned int));
		break;
	case HZ6:
		show_single_color_pattern(colorOne, intensityOne, pwm::hz_6, sizeof(pwm::hz_6)/sizeof(unsigned int));
		break;
	case SOS_MOD:
		show_single_color_pattern(colorOne, intensityOne, pwm::sos_mod, sizeof(pwm::sos_mod)/sizeof(unsigned int));
		break;
	case CHIRP:
		show_single_color_pattern(colorOne, intensityOne, pwm::chirpup, sizeof(pwm::chirpup)/sizeof(unsigned int));
		break;
	case CHIRP_3:
		show_tri_color_pattern(colorOne, intensityOne, pwm::chirpup_cOne, sizeof(pwm::chirpup_cOne)/sizeof(unsigned int), \
				colorTwo, intensityTwo, pwm::chirpup_cTwo, sizeof(pwm::chirpup_cTwo)/sizeof(unsigned int), \
				colorThree, intensityThree, pwm::chirpup_cThree, sizeof(pwm::chirpup_cThree)/sizeof(unsigned int));
		break;

	/*
	case HZ2_50:
		show_single_color_pattern(colorOne, intensityOne, pwm::hz_2_50, sizeof(pwm::hz_2_50)/sizeof(unsigned int));
		break;
	case HZ2_25:
		show_single_color_pattern(colorOne, intensityOne, pwm::hz_2_25, sizeof(pwm::hz_2_25)/sizeof(unsigned int));
		break;
	case HZ2_50_ALT:
		cout << "2Hz, 50% Duty." << endl;
		show_dual_color_pattern(colorOne, intensityOne, pwm::hz_2_50, sizeof(pwm::hz_2_50)/sizeof(unsigned int), \
				colorTwo, intensityTwo, pwm::hz_2_50, sizeof(pwm::hz_2_50)/sizeof(unsigned int));
		break;
		*/
	case HZ4_10_DUT:
		cout << "4Hz, 10% Iterrupt Duty." << endl;
		show_dual_color_pattern(colorOne, intensityOne, pwm::hz_4_10_dut_cOne, sizeof(pwm::hz_4_10_dut_cOne)/sizeof(unsigned int), \
				colorTwo, intensityTwo, pwm::hz_4_10_dut_cTwo, sizeof(pwm::hz_4_10_dut_cTwo)/sizeof(unsigned int));
		break;
	case HZ4_20_DUT:
		cout << "4Hz, 20% Iterrupt Duty." << endl;
		show_dual_color_pattern(colorOne, intensityOne, pwm::hz_4_20_dut_cOne, sizeof(pwm::hz_4_20_dut_cOne)/sizeof(unsigned int), \
				colorTwo, intensityTwo, pwm::hz_4_20_dut_cTwo, sizeof(pwm::hz_4_20_dut_cTwo)/sizeof(unsigned int));
		break;
	case HZ4_30_DUT:
		cout << "4Hz, 30% Iterrupt Duty." << endl;
		show_dual_color_pattern(colorOne, intensityOne, pwm::hz_4_30_dut_cOne, sizeof(pwm::hz_4_30_dut_cOne)/sizeof(unsigned int), \
				colorTwo, intensityTwo, pwm::hz_4_30_dut_cTwo, sizeof(pwm::hz_4_30_dut_cTwo)/sizeof(unsigned int));
		break;
	case HZ2_25_INT:
		cout << "2Hz, 25% Interrupt Duty." << endl;
		show_dual_color_pattern(colorOne, intensityOne, pwm::hz_2_25_int_cOne, sizeof(pwm::hz_2_25_int_cOne)/sizeof(unsigned int), \
				colorTwo, intensityTwo, pwm::hz_2_25_int_cTwo, sizeof(pwm::hz_2_25_int_cTwo)/sizeof(unsigned int));
		break;
	case FIXED:
		cout << "Fixed" << endl;
		show_fixed_pattern(colorOne, intensityOne);
		break;
	case CAL:
		cout << "Calibration" << endl;
		show_single_color_pattern(colorOne, intensityOne, pwm::calibration, sizeof(pwm::calibration)/sizeof(unsigned int));
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
