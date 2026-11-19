.PHONY: all
all: uaf_demo patched_heap safe_equivalent
uaf_demo patched_heap: %: %.c
	$(CC) -Wall -Wextra -O1 -g -fno-omit-frame-pointer -fsanitize=address $< -o $@
safe_equivalent: safe_equivalent.rs
	rustc -g -D warnings $< -o $@
