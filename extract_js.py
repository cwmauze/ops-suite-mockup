import re

with open('index.html', 'r') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)

with open('test.js', 'w') as f:
    for s in scripts:
        f.write(s)
        f.write('\n')

