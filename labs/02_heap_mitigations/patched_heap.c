#include <stdio.h>
#include <stdlib.h>
/* Borrow only during this call; keep release responsibility with the caller. */
static void report(const int *value) { printf("%d\n", *value); }
int main(void) {
    int *owner = malloc(sizeof *owner);
    if (!owner) return 1;
    *owner = 42;
    report(owner);
    free(owner);
}
