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

Add rules to the directory, rules will affect directories and files in it
```python
from ofacd import Rule


rule = Rule(path='.')

all_rules = {
	'dir_<name>': (lambda x: x.title(),),
	'file_<name>': (lambda x: x.lower(),),
	'shared_<name>': (lambda x: x.replace('_', '__'),),
	'finalyze_<name>': (lambda data: data,),
}
for rule_key, rules in all_rules.items():
	rule.set_rule(rule_key, rules)

rule.execute(rules_order=('dir_<name>', 'file_<name>', 'schared_<name>'))
rule.finalyze()
```

### Install
```bash
pip install ofacd
# or
pip install git+https://github.com/ames0k0/ofacd
```
