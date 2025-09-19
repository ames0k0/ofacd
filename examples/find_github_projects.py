"""Recursively searches for a `.git` folder
"""

if __name__ != "__main__":
	exit(1)

import os
import sys
import importlib
from pathlib import Path

sys.path.append(
	(Path(os.getcwd()).parent).as_posix()
)
importlib.import_module("ofacd")

from ofacd.main import Rule
from ofacd.main import CustomPath

ROOT_DIR = "."

for d in sys.argv[1:]:
	d = Path(d)
	if not d.is_dir():
		# XXX (ames0k0): --quite
		continue
	ROOT_DIR = d
	break

def create_files(dirpath: Path) -> CustomPath:
	if (dirpath / ".git").exists():
		print('>', dirpath)
		dirpath.RULE.curr_child_dirs.remove(dirpath.name)
	return dirpath

rule = Rule(
	path=str(ROOT_DIR),
	exclude_dirs=["pgdata", ".git", ".venv", ".env", "__pycache__", "node_modules", "venv", "env"],
	exclude_files=[".env", "__init__.py"],
)

def init_rule():
	rule.set_rules(
		key='dir_add_init_files',
		rules=(
			create_files,
		)
	)
	rule.execute(
		rules_order=(
			'dir_add_init_files',
		),
		recursive=True,
	)

init_rule()