import re
import requests
import sys

a = input()
b = input()
res0 = requests.get(a)
res = re.findall(r"(https?://[^\s]+.html)", res0.text)
res2 = []
for c in res:
    res0 = requests.get(c)
    res3 = re.findall(r"(https?://[^\s]+.html)", res0.text)
    for d in res3:
        if d not in res2:
            res2.extend([d])
if b in res2:
    print("Yes")
else:
    print("No")
