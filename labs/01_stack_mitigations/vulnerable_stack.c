/* Inspection baseline: an unchecked copy would be unsafe for arbitrary input.
 * The only caller supplies a short literal; never accept external input here. */
#include <stdio.h>
#include <string.h>
static __attribute__((noinline)) void preview(const char *text) {
    char local[32];
    strcpy(local, text);
    puts(local);
}
int main(void) { preview("frame inspection"); }
