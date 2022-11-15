import requests

params = {
    "text": "31 is a repdigit in base 5 (111), and base 2 (11111).",
    "number": 31,
    "found": True,
    "type": "math"
}
f = open("dataset_24476_3 (2).txt")
g = open("result.txt", "w")
for line in f:
    number = int(line)
    res = requests.get(f'http://numbersapi.com/{number}/math?json=True', params = params)
    data = res.json()
    if data["found"]:
        g.write("Interesting")
    else:
        g.write("Boring")
    g.write("\n")
f.close()
g.close()
