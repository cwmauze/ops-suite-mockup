import re

with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('        // Initialize\n        renderTabs();', '        // Initialize\n        renderTabs();\n        calculateRisk();')

with open('index.html', 'w') as f:
    f.write(html)
print("Updated index.html init")
