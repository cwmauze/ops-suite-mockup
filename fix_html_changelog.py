import re

with open('index.html', 'r') as f:
    html = f.read()

html_entry = """            <h4 style="margin-top:0; color:var(--accent-blue);">[0.0.24] - 2026-06-18</h4>
            <ul style="padding-left:20px; margin-bottom:15px; color:#ddd;">
                <li>Created a custom 24-hour iOS-style Time Picker with scroll-snapping rollers.</li>
                <li>Implemented dynamic Risk Assessment scoring (1-46 items) with responsive dashboard tile colors (Green/Orange/Red).</li>
                <li>Added a "Sign to Approve" toggle in the Risk modal that forces the tile green.</li>
                <li>Refactored Fuel section to a single compact horizontal row.</li>
                <li>Bound IFR leg toggle to per-leg state engine.</li>
                <li>Implemented tiered decluttering for Leg tabs to prevent horizontal scrolling.</li>
                <li>Added dynamic timestamps to "Last sync" status.</li>
                <li>Moved Leg deletion to a dedicated bottom button with confirmation prompt.</li>
            </ul>
"""

# Replace 0.0.23 with the new entry + the old 0.0.23 (removing margin-top:0 from the old one if it had it, but keeping it simple)
target = '<h4 style="color:var(--accent-blue);">[0.0.23] - 2026-06-18</h4>'
html = html.replace(target, html_entry + '            ' + target)

# Also update the mockup version text at the top
html = html.replace('Mockup v0.0.23', 'Mockup v0.0.24')

with open('index.html', 'w') as f:
    f.write(html)

print("Updated HTML changelog")
