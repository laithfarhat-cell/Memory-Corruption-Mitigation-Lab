BASE = -Wall -Wextra -g -fno-omit-frame-pointer -fno-optimize-sibling-calls
HARD = -O2 -fstack-protector-strong -D_FORTIFY_SOURCE=2 -fPIE -pie -Wl,-z,relro,-z,now,-z,noexecstack
.PHONY: all
all: unhardened hardened patched
unhardened: vulnerable_stack.c
	$(CC) $(BASE) -O0 -fno-stack-protector -fno-pie -no-pie -Wl,-z,norelro,-z,noexecstack $< -o $@
hardened: vulnerable_stack.c
	$(CC) $(BASE) $(HARD) -fno-ipa-cp $< -o $@
patched: patched_stack.c
	$(CC) $(BASE) $(HARD) $< -o $@
