"""Import every application module on its own

A module that imports only because another one was loaded first hides an
import cycle, and the application fails as soon as the startup order changes.
Each module gets a fresh interpreter because modules already in sys.modules
would mask the problem.

Run from the project root with: python -m unittest discover tests
"""

# standard library
import os
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def app_modules() -> list[str]:
    "Return the dotted name of every application module, packages excluded"
    return sorted('.'.join(path.relative_to(ROOT).with_suffix('').parts)
                  for path in (ROOT / 'App').rglob('*.py')
                  if path.name != '__init__.py')


def import_module(module: str) -> subprocess.CompletedProcess[str]:
    "Import a module in a new interpreter, without a display"
    env = os.environ | {'QT_QPA_PLATFORM': 'offscreen',
                        'PYTHONDONTWRITEBYTECODE': '1'}
    return subprocess.run([sys.executable, '-c', f'import {module}'],
                          cwd=ROOT, env=env, capture_output=True, text=True)


class ImportTest(unittest.TestCase):

    def test_every_module_imports_on_its_own(self) -> None:
        modules = app_modules()
        self.assertTrue(modules)
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
            results = list(pool.map(import_module, modules))
        for module, result in zip(modules, results):
            with self.subTest(module=module):
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
