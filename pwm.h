#ifndef PWM_H_
#define PWM_H_

namespace pwm
{
static unsigned int hz_4 = {125, 125};
static unsigned int hz_2 = {250, 250};
static unsigned int hz_2_25 = {125, 475};
static unsigned int hz_6 = {83, 83};
static unsigned int four_three_interrupt = {125, 125, 125, 125, 125, 125, 125, 250, 125, 125, 125, 125, 125, 250};
static unsigned int four_three_cOne = {125, 125, 125, 125, 125, 125, 125, 250};
static unsigned int four_three_cTwo = {125, 125, 125, 125, 125, 250};
static unsigned int chirp_up_cOne = {250, 250, 250, 250, 250, 250, 250, 250, 250, 250};
static unsigned int chirp_up_cTwo = {125, 125,125, 125,125, 125,125, 125,125, 125,125, 125,125, 125,125, 125};
static unsigned int chirp_up_cThree = {83, 83, 83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83,83, 83};
static unsigned int sos_mod = {125, 125, 125, 125, 125, 125, 375, 125, 375, 125, 375, 125, 125, 125, 125, 125, 125, 300};
static unsigned int hz_2_25_int_cOne = {125, 375, 125, 375, 125, 375, 125, 250};
static unsigned int hz_2_25_int_cTwo = {125, 375, 125, 375, 125, 250};
}


#endif
