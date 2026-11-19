#include <stdio.h>
#include <string.h>
static __attribute__((noinline)) int preview(const char *text) {
    char local[32];
    /* Reject rather than silently truncate. Include the terminating byte. */
    if (strlen(text) >= sizeof local) return 1;
    strcpy(local, text);
    puts(local);
    return 0;
}
int main(int argc, char **argv) { return preview(argc > 1 ? argv[1] : "frame inspection"); }
