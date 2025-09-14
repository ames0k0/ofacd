"""Creates `__init__.py` files for all subdirectories

Creates Dirs and Files (and Removes)
-----------------
	root/
		a/
			b/__init__.py
			c/__init__.py
			__init__.py
"""

if __name__ != "__main__":
	exit(1)

import os
import sys
import shutil
import importlib
from pathlib import Path

sys.path.append(
	(Path(os.getcwd()).parent).as_posix()
)
importlib.import_module("ofacd")

from ofacd.main import DirectoryStructure
from ofacd.main import Rule

ROOT_DIR = "root"

def create_files(dirpath: Path):
	filepath = dirpath / "__init__.py"
	filepath.touch(exist_ok=True)
	return filepath

ds = DirectoryStructure(ROOT_DIR)
rule = Rule(path=ROOT_DIR)

def clean_up():
	if not ds.root_dir.exists():
		return
	shutil.rmtree(path=ROOT_DIR, ignore_errors=True)
	print()
	print('---------- DIRS DELETED ----------')
	print(ROOT_DIR)

def init_directory_structure():
	ds.add(
		(
			'a',
			('b', 'c',),
		)
	)
	ds.create()
	print('---------- DIRS CREATED ----------')
	for dir in ds.root_dir.rglob("*"):
		print(dir)

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
	print()
	print('---------- FILES CREATED ---------')
	for file in ds.root_dir.rglob("*.py"):
		print(file)

clean_up()
init_directory_structure()
init_rule()
clean_up()