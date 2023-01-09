#/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable
from pathlib import Path


class DirectoryStructure:
  def __init__(self, root_path: str):
    self.root_path = root_path
    self.dirs = []

  def add(self, *dirs: tuple) -> None:
    """Generating the parent and child `dirs` to `create()`

    """
    # XXX: `root/a/b` will be replaced with `root/a/b/c`
    root_dir, *dirs = dirs
    if dirs:
      pass

    prev_d = None

    # 1. single
    # next child
    curr_path = None

    for d in dirs:
      if curr_path is None:
        curr_path = d

    if curr_path:
      self.dirs.append(curr_path)

  def create(self) -> None:
    pass


class Directory:
  def __init__(self, path: str) -> None:
    pass
  def fofs(self) -> Path:
    pass


class FOF:
  def __init__(self, path: Path | str) -> None:
    pass


class Rule:
  """ Destination
  """
  def __init__(self, src: Directory, dst: Directory) -> None:
    self.src = src
    self.dst = dst

  def add(self, *args: Callable) -> None:
    pass

  def execute(self, fof: Path):
    pass
