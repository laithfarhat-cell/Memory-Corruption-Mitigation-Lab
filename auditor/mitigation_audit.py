"""Report static mitigation evidence, without loading or executing the ELF."""
import argparse
from pathlib import Path

from elftools.common.exceptions import ELFError
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
from rich.console import Console
from rich.table import Table
from rich.text import Text


def inspect(path: Path) -> dict[str, str]:
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        segments = list(elf.iter_segments())
        kinds = {s['p_type'] for s in segments}
        stack = next((s for s in segments if s['p_type'] == 'PT_GNU_STACK'), None)
        now = pie = False
        for segment in segments:
            if segment['p_type'] != 'PT_DYNAMIC':
                continue
            for tag in segment.iter_tags():
                kind, value = tag.entry.d_tag, tag.entry.d_val
                now |= (kind == 'DT_BIND_NOW' or
                        (kind == 'DT_FLAGS' and bool(value & 8)) or
                        (kind == 'DT_FLAGS_1' and bool(value & 1)))
                pie |= kind == 'DT_FLAGS_1' and bool(value & 0x08000000)
        symbols = {sym.name.split('@')[0] for sec in elf.iter_sections()
                   if isinstance(sec, SymbolTableSection) for sym in sec.iter_symbols()}
        typ = elf['e_type']
        return {
            'NX stack': ('Unknown' if stack is None else
                         'Disabled' if stack['p_flags'] & 1 else 'Enabled'),
            'Canary': 'Observed' if '__stack_chk_fail' in symbols else 'Not observed',
            'PIE': ('Yes' if typ == 'ET_DYN' and (pie or 'PT_INTERP' in kinds) else
                    'No' if typ == 'ET_EXEC' else 'Indeterminate'),
            'RELRO': ('No RELRO' if 'PT_GNU_RELRO' not in kinds else
                      'Full RELRO' if now else 'Partial RELRO'),
            'FORTIFY': 'Observed' if any(s.startswith('__') and s.endswith('_chk')
                                         for s in symbols) else 'Not observed',
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+', type=Path)
    errors = Console(stderr=True, markup=False)
    failed = False
    for path in parser.parse_args().paths:
        try:
            findings = inspect(path)
        except (OSError, ELFError) as exc:
            errors.print(f'{path}: {exc}')
            failed = True
            continue
        table = Table('Property', 'ELF evidence', title=Text(str(path)))
        for key, value in findings.items():
            table.add_row(key, value)
        Console().print(table)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
