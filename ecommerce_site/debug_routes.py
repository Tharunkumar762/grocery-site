import os
print('cwd:', os.getcwd())
from app import app
for rule in sorted(app.url_map.iter_rules(), key=lambda x: x.rule):
    print(rule, list(rule.methods))
