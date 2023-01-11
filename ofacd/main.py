#/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Callable, Iterable
from pathlib import Path


class DirectoryStructure:
  def __init__(self, root_dir: str):
    self.root_dir = Path(root_dir)
    self.dirs = []

  def add(self, dirs: Iterable, parent_dir: Path | None = None) -> None:
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


class Directory:
  def __init__(self, path: str) -> None:
    self.path = path
  def fofs(self) -> Path:
    pass


class FOF:
  def __init__(self, path: Path | str) -> None:
    pass


class Rule:
  """ Destination
  """
  def __init__(self, path: Directory) -> None:
    self.path = path
    self.dir_rules = tuple()
    self.file_rules = tuple()
    self.shared_rules = tuple()

  def set_dir_rules(self, *rules: Callable) -> None:
    self.dir_rules = rules
  def set_file_rules(self, *rules: Callable) -> None:
    self.file_rules = rules
  def add(self, *rules: Callable) -> None:
    self.shared_rules.extend(rules)

  def execute(self):
    pass
