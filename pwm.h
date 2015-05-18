#ifndef PWM_H_
#define PWM_H_

#define HZ4 		0
#define HZ4_ALT		1
#define HZ4_INT		2
#define HZ4_ALT_INT	3
#define HZ6			4
#define SOS_MOD		5
#define CHIRP		6
#define CHIRP_3		7
/*
 * Update for Release1505, remove 2 HZ - 50, 25 and alternating duty cycles
 *
 *
#define HZ2_25		8
#define HZ2_50		9
#define HZ2_50_ALT	10
*/
#define HZ4_10_DUT  8
#define HZ4_20_DUT  9
#define HZ4_30_DUT  10
#define HZ2_25_INT	11
#define FIXED		12
#define CAL			13

namespace pwm
{
/*
 * Calibration Pattern - Non Release Pattern
 */
static unsigned int calibration[2]	= {350, 1650};

/*
 * 4Hz, 50% Duty - Pattern 1
 */
static unsigned int hz_4[2] = {125, 125};

/*
 * Four Three Interrupt 1 Color - Pattern 2
 */
static unsigned int four_three_interrupt[14] = {125, 125, 125, 125, 125, 125, 125, 250, 125, 125, 125, 125, 125, 250};

/*
 * Four Three Interrupt 2 Color - Pattern 3
 */
static unsigned int four_three_cOne[8] = {125, 125, 125, 125, 125, 125, 125, 250};
static unsigned int four_three_cTwo[6] = {125, 125, 125, 125, 125, 250};

/*
 * 6Hz, 50% Duty - Pattern 4
 */
static unsigned int hz_6[2] = {83, 83};

/*
 * SOS - Pattern 5
 */
static unsigned int sos_mod[18] = {125, 125, 125, 125, 125, 125, 375, 125, 375, 125, 375, 125, 125, 125, 125, 125, 125, 300};

/*
 * Chirp Up 1 Color - Pattern 6
 */
static unsigned int chirpup [56] = {250, 250, 250, 250, 250, 250, 250, 250, 250, 250, \
		125, 125,125, 125,125, 125,125, 125,125, 125,125, 125,125, 125,125, 125, \
		83, 83, 83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83
		};

/*
 * Chirp Up 3 Color - Pattern 7
 */
static unsigned int chirpup_cOne[10] = {250, 250, 250, 250, 250, 250, 250, 250, 250, 250};
static unsigned int chirpup_cTwo[16] = {125, 125,125, 125,125, 125,125, 125,125, 125,125, 125,125, 125,125, 125};
static unsigned int chirpup_cThree[30] = {83, 83, 83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83};

/*
 * 4Hz, 10% Duty Interrupt Sequence - Pattern 8
 */
static unsigned int hz_4_10_dut_cOne[8] = {25, 225, 25, 225, 25, 225, 25, 250};
static unsigned int hz_4_10_dut_cTwo[6] = {25, 225, 25, 225, 25, 250};

/*
 * 4Hz, 20% Duty Interrupt Sequence - Pattern 9
 */
static unsigned int hz_4_20_dut_cOne[8] = {50, 200, 50, 200, 50, 200, 50, 250};
static unsigned int hz_4_20_dut_cTwo[6] = {50, 200, 50, 200, 50, 250};

/*
 * 4Hz, 30% Duty Interrupt Sequence - Pattern 10
 */
static unsigned int hz_4_30_dut_cOne[8] = {75, 175, 75, 175, 75, 175, 75, 250};
static unsigned int hz_4_30_dut_cTwo[6] = {75, 175, 75, 175, 75, 250};

/*
 * 2Hz Alternating Intterupt @ 25% Duty - Pattern 11
 */
static unsigned int hz_2_25_int_cOne[8] = {125, 375, 125, 375, 125, 375, 125, 250};
static unsigned int hz_2_25_int_cTwo[6] = {125, 375, 125, 375, 125, 250};

/******************************************
 * 	Deprecated Patterns
 */
/*
 * 2Hz, 50% Duty - Deprecated Pattern
 */
static unsigned int hz_2_50[2] = {250, 250};

/*
 * 2Hz, 25% Duty - Deprecated Pattern
 */
static unsigned int hz_2_25[2] = {125, 375};

}


#endif
