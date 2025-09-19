import os
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import Self
from typing import Sequence
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


class CustomPath(Path):
  """Mutable Path"""
  RULE: "Rule"


class Rule:
  """Rules to the directories and files
  """
  __slots__ = (
    'path', 'rules',
    'exclude_dirs', 'exclude_files',
    'curr_child_dirs',
  )

  def __init__(
      self: Self,
      path: str,
      exclude_dirs: Sequence[str] | None = None,
      exclude_files: Sequence[str] | None = None,
  ) -> None:
    self.path = CustomPath(path)
    self.rules = {'data': []}
    self.exclude_dirs = exclude_dirs or []
    self.exclude_files = exclude_files or []
    self.curr_child_dirs: Sequence[str] | None = None

  def set_rules(self, key: str, rules: tuple[Callable]) -> None:
    """Setting rules for directories and files

    Keywords on naming rules: `file_`, `dir_`, `shared_`, `finalyze_`
    Keyword to store results: `data`
    """
    self.rules[key] = rules

  def fod(self, rule_key: str, exec_path: CustomPath) -> bool:
    if rule_key.startswith('shared_'):
      return True
    if rule_key.startswith('dir_') and exec_path.is_dir():
      return True
    if rule_key.startswith('file_') and exec_path.is_file():
      return True
    return False

  def _directory_tree_iterator(
      self: Self,
      *,
      exec_path: Path,
      recursive: bool,
  ) -> Generator[Path, None, None]:
    """Yields directory tree

    Yileds absolute path to the files (and directories if recursive)
    Yield order: root_dir, child_dirs, root_files
    """
    root_dir, child_dirs, root_files = next(exec_path.walk())
    # XXX (ames0k0): excludes dirs and files
    child_dirs = set(child_dirs).difference(self.exclude_dirs)
    root_files = set(root_files).difference(self.exclude_files)

    # XXX (ames0k0): yields the `root_dir`, `child_dir` for a `recursive`
    yield CustomPath(root_dir)

    # XXX (ames0k0): Let a `rule` updated `child_dirs`
    self.curr_child_dirs = child_dirs.copy()

    for child_dir in child_dirs:
      child_dirpath = root_dir / child_dir
      yield CustomPath(child_dirpath)

    for root_file in root_files:
      yield CustomPath(root_dir / root_file)

    if not recursive:
      return

    # XXX (ames0k0): Iterate updated `child_dirs`
    for child_dir in self.curr_child_dirs:
      child_dirpath = CustomPath(root_dir / child_dir)
      # XXX (ames0k0): --quite
      if not os.access(child_dirpath, os.R_OK):
        continue
      yield from self._directory_tree_iterator(
        exec_path=child_dirpath,
        recursive=recursive,
      )

  def execute(
      self,
      *,
      rules_order: tuple[str],
      exec_path: Path | None = None,
      recursive: bool = False,
  ) -> None:
    """Executes the rules, for files, for directories and for both
    """
    # XXX (ames0k0): What is it `exec_path` for ?!
    if exec_path is None:
      exec_path = self.path

    if not exec_path.exists():
      return None

    dir_iterator = self._directory_tree_iterator(
      exec_path=exec_path,
      recursive=recursive
    )
    for child in dir_iterator:
      # XXX (ames0k0): Pointer for a current state
      setattr(child, "RULE", self)

      for rule_key in rules_order:
        if not self.fod(rule_key=rule_key, exec_path=child):
          continue

        rules = self.rules[rule_key]
        for rule in rules:
          result = rule(child)

          if result:
            self.rules['data'].append(result)

  def finalyze(self) -> None:
    """Processing the rules execution result (stored data)
    """
    data = self.rules['data']
    if not data:
      return None

    rules = tuple()

    for rule_key in self.rules:
      if rule_key.startswith('finalyze_'):
        rules = self.rules[rule_key]
        break

    for rule in rules:
      rule(data)
