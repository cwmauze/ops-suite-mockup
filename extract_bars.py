import re

with open('flightlog.html', 'r') as f:
    text = f.read()

def extract_block(pattern_start, pattern_end):
    match = re.search(pattern_start + r'(.*?)' + pattern_end, text, re.DOTALL)
    if match: return match.group(0)
    return None

sync_bar_css = extract_block(r'\.sync-bar \{', r'\}\s*\n\s*\.global-header')
global_header_css = extract_block(r'\.global-header \{', r'\}\s*\n\s*\.header-content')
bottom_nav_css = extract_block(r'\.bottom-nav \{', r'\}\s*\n\s*\.modal-overlay')

sync_bar_html = extract_block(r'<div class="sync-bar">', r'</div>\s*\n\s*<!-- Global Header -->')
global_header_html = extract_block(r'<div class="global-header">', r'</div>\s*\n\s*<!-- Main Scrolling Content -->')
bottom_nav_html = extract_block(r'<div class="bottom-nav">', r'</div>\s*\n\s*</div>\s*\n\s*<div class="simulated-indicator">')

# Wait, `flightlog.html` has a back button in its global-header, which I shouldn't copy to home.html or index.html.
# Actually, the user's implementation plan says:
# "Ensure the .sync-bar ... CSS classes are identical"
# "Inject the <div class="sync-bar"> HTML directly under the .device-screen element."
# "Inject the <div class="bottom-nav"> HTML above the simulated inputs/keyboards."
# "Inject the toggleTheme() ... JS"
# "Inject the triggerManualSync() JS"

print(f"Sync Bar CSS found: {bool(sync_bar_css)}")
print(f"Global Header CSS found: {bool(global_header_css)}")
print(f"Bottom Nav CSS found: {bool(bottom_nav_css)}")

print(f"Sync Bar HTML found: {bool(sync_bar_html)}")
print(f"Global Header HTML found: {bool(global_header_html)}")
print(f"Bottom Nav HTML found: {bool(bottom_nav_html)}")
