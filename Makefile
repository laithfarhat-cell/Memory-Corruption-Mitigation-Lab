PYTHON ?= python3
STACK = labs/01_stack_mitigations
.PHONY: all stack heap arithmetic test audit clean
all: stack heap arithmetic
stack:
	$(MAKE) -C $(STACK)
heap:
	$(MAKE) -C labs/02_heap_mitigations
arithmetic:
	$(MAKE) -C labs/03_integer_and_format
audit: stack
	$(PYTHON) auditor/mitigation_audit.py $(STACK)/unhardened $(STACK)/hardened
test:
	$(PYTHON) -m pytest -q
clean:
	rm -f $(STACK)/unhardened $(STACK)/hardened $(STACK)/patched labs/02_heap_mitigations/uaf_demo labs/02_heap_mitigations/patched_heap labs/02_heap_mitigations/safe_equivalent labs/03_integer_and_format/int_overflow labs/03_integer_and_format/patched_int labs/03_integer_and_format/format_demo
