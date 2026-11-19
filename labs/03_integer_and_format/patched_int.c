#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
static int allocate(size_t count) {
    size_t bytes;
    if (__builtin_mul_overflow(count, sizeof(uint32_t), &bytes)) return 1;
    void *p = malloc(bytes);
    if (!p) return 1;
    free(p);
    return 0;
}
int main(void) {
    if (!allocate(SIZE_MAX)) return 1;
    puts("oversize request rejected");
    return allocate(4);
}
