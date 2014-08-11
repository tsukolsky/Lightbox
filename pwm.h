#ifndef PWM_H_
#define PWM_H_

#define HZ4 		0
#define HZ4_ALT		1
#define HZ4_INT		2
#define HZ4_ALT_INT	3
#define HZ6			4
#define SOS_MOD		5
#define CHIRP		6
#define CHRIP_3		7
#define HZ2_50		8
#define HZ2_25		9
#define HZ2_25_INT	10
#define HZ2_50_ALT	11
#define FIXED		12

namespace pwm
{
static unsigned int hz_4[2] = {125, 125};
static unsigned int hz_2[2] = {250, 250};
static unsigned int hz_2_25[2] = {125, 475};
static unsigned int hz_6[2] = {83, 83};
static unsigned int four_three_interrupt[14] = {125, 125, 125, 125, 125, 125, 125, 250, 125, 125, 125, 125, 125, 250};
static unsigned int four_three_cOne[8] = {125, 125, 125, 125, 125, 125, 125, 250};
static unsigned int four_three_cTwo[6] = {125, 125, 125, 125, 125, 250};
static unsigned int chirp_up_cOne[10] = {250, 250, 250, 250, 250, 250, 250, 250, 250, 250};
static unsigned int chirp_up_cTwo[16] = {125, 125,125, 125,125, 125,125, 125,125, 125,125, 125,125, 125,125, 125};
static unsigned int chirp_up_cThree[30] = {83, 83, 83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83};
static unsigned int sos_mod[18] = {125, 125, 125, 125, 125, 125, 375, 125, 375, 125, 375, 125, 125, 125, 125, 125, 125, 300};
static unsigned int hz_2_25_int_cOne[8] = {125, 375, 125, 375, 125, 375, 125, 250};
static unsigned int hz_2_25_int_cTwo[6] = {125, 375, 125, 375, 125, 250};
}


#endif
