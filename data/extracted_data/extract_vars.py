import re
import pathlib
import json
import sys

# Extract keys from queries/*.txt

f_names = [f for f in pathlib.Path('../').glob('*.txt')]
var_defs = {}
qa = []

for f_name in f_names:
    with open(f_name) as fin:
        for l in fin.readlines():
            if ':' in l:
                pat = re.compile('^\[([^\[\]]*)\]\s*:\s*(.*)')
                match = pat.match(l)
                if match:
                    name, defn = match.groups()
                    var_defs[name] = defn
    sys.stdout.flush()
print(json.dumps(var_defs, indent=4, sort_keys=True))
sys.stdout.flush()