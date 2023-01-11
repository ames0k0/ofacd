# ofacd - Organize files and clean directories
> Create a directory tree and rules for files that will be moved to there
Create a directory structre
```python
from ofacd import DirectoryStructure

ds = DirectoryStructure('z_l0')
ds.add((
	'a_l1', ('b_l2', 'c_l2', ('d_l3', 'e_l3')),
))
ds.add((((('f_l1',)))))

# print(ds.dirs)
# [
# 	PosixPath('z_l0/a_l1/b_l2'),
# 	PosixPath('z_l0/a_l1/c_l2/d_l3'),
# 	PosixPath('z_l0/a_l1/c_l2/e_l3'),
# 	PosixPath('z_l0/f_l1')
# ]

ds.create()
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
