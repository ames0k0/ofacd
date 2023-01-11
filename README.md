# ofacd - Organize files and clean directories
> Create a directory tree and rules for files that will be moved to there
Create a directory structre
```python
from ofacd import DirectoryStructure

ds = DirectoryStructure('root_directory')
ds.add((
	'a_l1', ('b_l2', 'c_l2', ('d_l3', 'e_l3')),
))
```

Add rules to the directory
```python
from ofacd import Directory, Rule

src_path = Directory(src_path)
dst_path = Directory(dst_path)
rule = Rule(src_path, dst_path)

rule.add(lambda x: x.replace('_', '__'))

for fof in a.fofs:
	r.execute(fof)
```
