import re
import os

def extract_balanced(text, start_str):
    start_idx = text.find(start_str)
    if start_idx == -1: return None
    
    count = 0
    in_str = False
    str_char = ''
    
    # Simple balanced tag extractor for <div>...</div>
    i = start_idx
    while i < len(text):
        if text[i:i+4] == '<div':
            count += 1
            i += 4
        elif text[i:i+6] == '</div':
            count -= 1
            i += 6
            if count == 0:
                # Find the closing >
                end_idx = text.find('>', i)
                return text[start_idx:end_idx+1]
        else:
            i += 1
    return None

def extract_css(text, class_name):
    # Extracts everything from .class_name { to the closing }
    # This is a bit tricky with nested {}, but CSS usually isn't nested unless using media queries
    pattern = r'(\.' + class_name + r'\s*\{[\s\S]*?\n\s*\})'
    match = re.search(pattern, text)
    if match: return match.group(1)
    return None

with open('flightlog.html', 'r') as f:
    ref = f.read()

# Extract HTML blocks
sync_bar_html = extract_balanced(ref, '<div class="sync-bar">')
global_header_html = extract_balanced(ref, '<div class="global-header">')
bottom_nav_html = extract_balanced(ref, '<div class="bottom-nav">')

# Extract CSS blocks
sync_css = []
for cls in ['sync-bar', 'sync-icon', 'sync-text', 'syncing']:
    matches = re.findall(r'(\.' + cls + r'\s*\{[\s\S]*?\n\s*\})', ref)
    sync_css.extend(matches)
    
nav_css = []
for cls in ['bottom-nav', 'nav-item', 'nav-icon', 'active']:
    matches = re.findall(r'(\.' + cls + r'\s*\{[\s\S]*?\n\s*\})', ref)
    nav_css.extend(matches)
    
# Extract JS
theme_js = re.search(r'(function toggleTheme\(\) \{[\s\S]*?body\.setAttribute\(\'data-theme\', newTheme\);\n        \})', ref).group(1)
sync_funcs_js = re.search(r'(function formatSyncTime\(\) \{[\s\S]*?el\.classList\.remove\(\'syncing\'\);\n            \}, 1500\);\n        \})', ref).group(1)
sync_init_js = re.search(r'(const initialSyncText = document\.querySelector\(\'\.sync-text\'\);\n        if \(initialSyncText\) initialSyncText\.innerHTML = `Last sync: \$\{formatSyncTime\(\)\}`;)', ref).group(1)

print("Extracted HTML:")
print(f"Sync: {len(sync_bar_html) if sync_bar_html else 0}")
print(f"Header: {len(global_header_html) if global_header_html else 0}")
print(f"Nav: {len(bottom_nav_html) if bottom_nav_html else 0}")
