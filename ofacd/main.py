#/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable
from pathlib import Path


class DirectoryStructure:
  def __init__(self, root_path: str):
    self.root_path = root_path
  def add(self, *dirs):
    pass
  def create(self):
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
