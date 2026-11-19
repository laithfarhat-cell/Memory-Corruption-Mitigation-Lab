/* Isolated arithmetic probe: UBSan terminates before size reaches malloc. */
#include <limits.h>
int main(void) {
    volatile int count = INT_MAX;
    volatile int bytes = count * 2;
    (void)bytes;
}
