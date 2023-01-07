# ofacd - Organize files and clean directories
> Create a directory tree and rules for files that will be moved to there
```python
src_path = Directory(src_path)
dst_path = Directory(dst_path)
rule = Rule(src_path, dst_path)

rule.add(lambda x: x.replace('_', '__'))

for fof in a.fofs:
	r.execute(fof)
```
