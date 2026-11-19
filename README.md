# Memory Corruption Internals & Compiler Mitigation Lab

![Platform](https://img.shields.io/badge/platform-Linux_x86--64-blue) ![Toolchain](https://img.shields.io/badge/toolchain-GCC%20%7C%20Rust-orange)

Compare two builds of **the same C function**, identify what changed in the ELF, then inspect the source fix. The exercises separate compiler evidence from runtime observation: an ELF can request a non-executable stack, but it cannot prove that every buffer access is valid.

## Build and verify

```sh
docker build -t mitigation-lab .
docker run --rm mitigation-lab
```

Or on x86-64 Linux with GCC/glibc, sanitizer runtimes, Make, Rust, GDB and Python 3.10+:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
make all
make audit
make test
```

## Walkthrough

1. **Stack:** `cd labs/01_stack_mitigations`; run `gdb -q -batch -x inspect_stack.gdb ./hardened`, then repeat with `./unhardened`. The breakpoint is in `puts`; `up` selects the initialized caller frame. Compare the guard load/check in `preview`, not absolute addresses. Use a host that permits local debugging. Both profiles copy only a fixed short string; `./patched` additionally validates external input. No exercise writes into frame metadata.
2. **Heap:** In `labs/02_heap_mitigations`, run `./uaf_demo`, `./patched_heap` and `./safe_equivalent`. The first models rejected operations; neither C binary intentionally triggers an ASan report. Compare the single-owner C convention with Rust's enforced move after `drop`. To see the compile-time diagnostic, uncomment the final borrow in a scratch copy and compile it with `rustc`.
3. **Arithmetic:** In `labs/03_integer_and_format`, run `./int_overflow`. A source-located signed-overflow diagnostic and nonzero exit are expected; no wrapped size is passed to an allocator. `./patched_int` instead rejects an unrepresentable size and accepts a small allocation.
4. **Formatting:** In that same directory, `./format_demo '100% literal'` prints its argument as data. `gcc -fsyntax-only -DCHECK_DIAGNOSTIC -Wformat -Werror=format-security format_demo.c` should reject the nonliteral format without producing a binary.
5. **Audit:** From the root, `python3 auditor/mitigation_audit.py /bin/ls` reads the file without executing it. On the lab profiles, NX stays enabled in both; only the hardened profile should show PIE, full RELRO, canary and fortified-call evidence. `make test` rebuilds fixtures independently of existing binaries.

Read [the architectural guide](THEORY.md) for the page map, sanitizer report anatomy and limits of each mitigation. `make clean` removes generated lab binaries.
