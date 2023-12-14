#ifndef TIMER
#define TIMER

#include <time.h>
#include <sstream>

class Timer {
public:
    Timer(double delay);
    bool test();

private:
    double delay;
    time_t last_true;
};



#endif
