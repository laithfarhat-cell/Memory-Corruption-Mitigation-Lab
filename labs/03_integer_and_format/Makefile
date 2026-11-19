WARN = -Wall -Wextra -Wformat -Wformat-security -Werror=format-security
.PHONY: all
all: int_overflow patched_int format_demo
int_overflow: int_overflow.c
	$(CC) $(WARN) -g -fsanitize=undefined -fno-sanitize-recover=undefined $< -o $@
patched_int format_demo: %: %.c
	$(CC) $(WARN) -O2 $< -o $@
