#/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Callable, Iterable
from pathlib import Path


class DirectoryStructure:
  """Creating a directory structure from iterable directory names

  Not validating the given `ds` to `add()`, don't test it
  """
  def __init__(self, root_dir: str):
    self.root_dir = Path(root_dir)
    self.dirs = []

  def add(self,
          dirs: Iterable[str | Iterable[str]],
          parent_dir: Path | None = None
  ) -> None:
    """Generating the parent and child `dirs` to `create()`
    """
    if parent_dir is None:
      parent_dir = self.root_dir
    if not dirs:
      self.dirs.append(parent_dir)
    for parent in dirs:
      if not isinstance(parent, str):
        # `root/a/b` will be replaced with `root/a/b/c`
        self.add(parent, self.dirs.pop())
        continue
      self.dirs.append(parent_dir / parent)

  def create(self) -> None:
    """Super-mkdir; create a leaf directory and all intermediate ones
    """
    for child_dir in self.dirs:
      os.makedirs(child_dir, exist_ok=True)


class Rule:
  """Rules to the directories and files
  """
  __slots__ = ('path', 'rules')

  def __init__(self, path: str) -> None:
    self.path = Path(path)
    self.rules = {'data': []}

  def set_rules(self, key: str, rules: tuple[Callable]) -> None:
    """Setting rules for directories and files

    Keywords on naming rules: `file_`, `dir_`, `shared_`, `finalyze_`
    Keyword to store results: `data`
    """
    self.rules[key] = rules

  def fod(self, rule_key: str, exec_path: Path) -> bool:
    if rule_key.startswith('shared_'):
      return True
    if rule_key.startswith('dir_') and exec_path.isdir():
      return True
    if rule_key.startswith('file_') and exec_path.isfile():
      return True
    return False

  def execute(
      self,
      rules_order: tuple[str],
      exec_path: Path | None = None, recursive: bool = True,
  ) -> None:
    """Executes the rules, for files, for directories and for both
    """
    if exec_path is None:
      exec_path = self.path

    if not exec_path.exists():
      return None

    for rule_key in rules_order:
      if not fod:
        continue

      rules = self.rules[rule_key]
      for rule in rules:
        result = rule(exec_path)

        if result:
          rules['data'].append(result)

    if not recursive:
      return None

    for child in exec_path.iterdirs():
      self.execute(rules_order, child, recursive)

  def finalyze(self) -> None:
    """Processing the rules execution result (stored data)
    """
    data = self.rules['data']
    if not data:
      return None

    rules = tuple()

    for rule_key in self.rules.keys:
      if rule_key.startswith('finalyze_'):
        rules = self.rules[rule_key]
        break

    for rule in rules:
      rule(data)
