import re

with open('index.html', 'r') as f:
    html = f.read()

# We want to remove the variables and functions that were mistakenly injected into the head
# The head script block starts around line 12: <script>
# and ends around line 93: </script>
# We can find the first </script> and strip out everything after toggleChangelog

# Find the toggleChangelog function end
toggle_end_idx = html.find('        function toggleChangelog() {')
if toggle_end_idx != -1:
    end_of_toggle = html.find('        }', toggle_end_idx) + 9
    
    first_script_close = html.find('</script>', end_of_toggle)
    
    if first_script_close != -1:
        # Reconstruct the first script block correctly
        html = html[:end_of_toggle] + '\n    </script>' + html[first_script_close + 9:]

with open('index.html', 'w') as f:
    f.write(html)
print("Cleaned head script block")
