
#include "timer.hpp"

using namespace std;

Timer::Timer(double delay0) {
    time(&last_true);
    delay = delay0;
}

bool Timer::test() {
    time_t current_time = time(NULL);
    if (delay <= difftime(current_time, last_true)) {
	last_true = current_time;
	return true;
    }
    return false;
}
