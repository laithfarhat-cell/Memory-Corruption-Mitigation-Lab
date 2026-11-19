/* Model two invalid requests without retaining or using a dangling pointer. */
#include <stdio.h>
#include <stdlib.h>
int main(void) {
    int *owner = malloc(sizeof *owner);
    if (!owner) return 1;
    *owner = 42;
    free(owner);
    owner = NULL;
    if (!owner) puts("read rejected: object lifetime ended");
    if (!owner) puts("release rejected: already released");
}
