from pathlib import Path
import shutil
import subprocess
import sys

import pytest
from auditor.mitigation_audit import inspect

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def stack(tmp_path_factory):
    dest = tmp_path_factory.mktemp('profiles')
    for name in ('Makefile', 'vulnerable_stack.c', 'patched_stack.c'):
        shutil.copy(ROOT / 'labs/01_stack_mitigations' / name, dest)
    subprocess.run(['make'], cwd=dest, check=True)
    return dest


@pytest.mark.parametrize('name,canary,pie,relro,fortify', [
    ('unhardened', 'Not observed', 'No', 'No RELRO', 'Not observed'),
    ('hardened', 'Observed', 'Yes', 'Full RELRO', 'Observed'),
])
def test_profiles(stack, name, canary, pie, relro, fortify):
    assert inspect(stack / name) == {'NX stack': 'Enabled', 'Canary': canary,
                                     'PIE': pie, 'RELRO': relro, 'FORTIFY': fortify}


def test_partial_relro(stack):
    binary = stack / 'partial'
    subprocess.run(['gcc', 'patched_stack.c', '-Wl,-z,relro,-z,lazy', '-o', binary],
                   cwd=stack, check=True)
    assert inspect(binary)['RELRO'] == 'Partial RELRO'


def test_bad_input():
    result = subprocess.run([sys.executable, ROOT / 'auditor/mitigation_audit.py',
                             ROOT / 'README.md'], capture_output=True, text=True)
    assert result.returncode == 1 and 'README.md' in result.stderr
