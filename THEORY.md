# From C objects to virtual pages

On Linux/x86-64 each process sees a virtual address space. Instructions and data share that address space (the Von Neumann model); sharing addresses does not imply sharing permissions. The MMU translates virtual pages and enforces permissions established by the kernel and loader. A plausible layout, not a fixed map:

```
high   initial stack       RW     argv, environment, active call frames
       ↓
       unmapped space / guard pages
       mmap regions        mixed  DSOs, anonymous mappings, large allocations
       ↑
       brk heap            RW     some allocator arenas
       .bss                RW     zero-initialized static storage
       .data               RW     initialized mutable static storage
       .rodata             R      constants, string literals
       .text               RX     machine instructions
low    unmapped
```

Sections organize link-time contents; `PT_LOAD` segments, not section names, determine initial page permissions. `.bss` need not occupy its full size on disk. Adjacent objects can share one writable page: an object boundary is not an MMU boundary.

## Calls and guards

A near `call` saves the continuation address on the stack. With a conventional frame pointer, the callee saves its caller's RBP and uses RBP as a stable frame reference while RSP tracks the stack top. RIP is the *current* instruction pointer, not the saved continuation. Locals, padding and spilled registers vary with the ABI, optimization and compiler. Inlining can remove a frame entirely.

Inspect `preview`'s prologue and epilogue together. In the protected build look for a thread-local guard load, a saved copy in the frame and a comparison before return. A mismatch branches to `__stack_chk_fail`; glibc normally prints “stack smashing detected” and terminates with SIGABRT. A fortified copy can terminate earlier, before the canary changes. Neither mechanism establishes that every write was valid.

## Allocation and lifetime

An allocator supplies suitably aligned storage, often by dividing arenas into chunks. An allocation's usable object extent is the requested size, not padding or neighboring allocator metadata. `free` ends its lifetime, even if pages remain mapped and address bits appear unchanged. A second release violates allocator ownership. Nulling one pointer does not invalidate aliases. Prefer one owner, short borrows and one release site.

ASan instruments accesses and maintains shadow state describing addressability (typically one shadow byte for eight application bytes). Redzones and poisoned freed storage help diagnose misuse. Read an ASan report by separating the **access**, **free**, and **allocation** stacks: the access is where the symptom was detected, not necessarily where ownership went wrong. Quarantine delays reuse; a clean run covers only executed paths. Rust's `Box` moves ownership; a shared borrow cannot outlive its owner in safe Rust.

## Sizes and formats

C signed overflow is undefined, not guaranteed two's-complement wrapping. Unsigned size arithmetic wraps modulo its range, so ordinary UBSan signed-overflow checks do not validate `size_t` multiplication. Check the operation *before* allocating: a successful `malloc` only satisfies the size it received. A format string is a program interpreted by libc. Keep it constant and pass external text as data.

## Defense in depth

| Layer | What it changes | What remains |
|---|---|---|
| Canary | Detects some frame corruption on exit | Earlier or unrelated data corruption |
| NX stack | Requests non-executable stack pages | Invalid reads and writes remain possible |
| PIE + OS ASLR | Permits randomized executable load base | No bounds or lifetime checks |
| Full RELRO | Loader resolves relocations eagerly, then seals the RELRO region | Other mutable data stays writable |
| FORTIFY | Object-size-aware libc operations can reject oversized requests | Unknown sizes and uninstrumented operations |
| ASan | Detects many spatial and temporal errors during testing | Coverage depends on instrumentation and execution |
| UBSan | Diagnoses selected undefined operations | Defined unsigned wrap is not undefined behavior |
| Ownership and checked sizes | Prevent invalid operations at their source | C interfaces still need explicit contracts |

Static ELF evidence is not an attestation of runtime policy. A missing GNU stack header is ambiguous; a DSO can be `ET_DYN` without being a PIE executable. Symbol presence suggests instrumentation, not whole-program coverage; optimization, stripping and static linking can hide evidence. RELRO requires both a protected range and eager binding for the full classification.
