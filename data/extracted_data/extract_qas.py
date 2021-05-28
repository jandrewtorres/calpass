import re
import pathlib
import json
import sys

# Extract qs and as from normalized.txt
qa = []

with open("../normalized.txt") as fin:
    line_count = 0
    complete_count = 0
    for l in fin.readlines():
        line_count += 1
        pat = re.compile('\|(.*)\|(.*)$')
        ans = pat.findall(l)
        if len(ans) > 0:
            qa.append(ans[0])
            complete_count += 1
print(json.dumps(qa, indent=4, sort_keys=True))