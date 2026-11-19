#include <stdio.h>
int main(int argc, char **argv) {
    const char *input = argc > 1 ? argv[1] : "100% literal\n";
#ifdef CHECK_DIAGNOSTIC
    printf(input); /* Negative compile test only. */
#else
    printf("%s", input);
#endif
}
