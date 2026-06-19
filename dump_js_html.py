import re

with open('flightlog.html', 'r') as f:
    text = f.read()

# Extract the entire JS block that handles theme and sync
# We know it starts at "const themes =" and ends after triggerManualSync
start = text.find("const themes = ['light'")
end = text.find("let currentRiskScore = 0;")
if end == -1: end = text.find("</script>", start)

js_block = text[start:end].strip()

# Extract sync-bar HTML
start_html = text.find('<div class="sync-bar">')
end_html = text.find('</div>', start_html) + 6
html_block = text[start_html:end_html].strip()

with open('extracted_js.txt', 'w') as f:
    f.write(js_block)

with open('extracted_html.txt', 'w') as f:
    f.write(html_block)

print("Dumped JS and HTML to text files.")
