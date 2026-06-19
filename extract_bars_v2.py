import re
import os

def extract_balanced(text, start_str):
    start_idx = text.find(start_str)
    if start_idx == -1: return None
    
    count = 0
    i = start_idx
    while i < len(text):
        if text[i:i+4] == '<div':
            count += 1
            i += 4
        elif text[i:i+6] == '</div':
            count -= 1
            i += 6
            if count == 0:
                end_idx = text.find('>', i)
                if end_idx == -1: end_idx = i
                return text[start_idx:end_idx+1]
        else:
            i += 1
    return None

def extract_nav_balanced(text, start_str):
    start_idx = text.find(start_str)
    if start_idx == -1: return None
    count = 0
    i = start_idx
    while i < len(text):
        if text[i:i+4] == '<nav': count += 1; i += 4
        elif text[i:i+5] == '</nav':
            count -= 1; i += 5
            if count == 0:
                end_idx = text.find('>', i)
                return text[start_idx:end_idx+1] if end_idx != -1 else text[start_idx:i+1]
        else: i += 1
    return None

with open('flightlog.html', 'r') as f:
    ref = f.read()

# CSS
sync_css = re.search(r'(\.sync-bar\s*\{[\s\S]*?)(?=\n\s*\.global-header)', ref).group(1)
header_css = re.search(r'(\.global-header\s*\{[\s\S]*?)(?=\n\s*\.header-content)', ref).group(1)
nav_css = re.search(r'(\.bottom-nav\s*\{[\s\S]*?)(?=\n\s*\.modal-overlay)', ref).group(1)

# HTML
sync_html = extract_balanced(ref, '<div class="sync-bar">')
header_html = extract_balanced(ref, '<div class="global-header">')
nav_html = extract_balanced(ref, '<div class="bottom-nav">')
if not nav_html: nav_html = extract_nav_balanced(ref, '<nav class="bottom-nav">')
if not nav_html: nav_html = extract_balanced(ref, '<div class="bottom-nav">')

# JS
theme_js = re.search(r'(const themes = \[\'light\', \'neutral\', \'dark\', \'hc-dark\', \'hc-light\'\];\n\s*function toggleTheme\(\) \{[\s\S]*?html\.setAttribute\(\'data-theme\', themes\[nextIndex\]\);\n\s*\})', ref).group(1)
sync_funcs_js = re.search(r'(function formatSyncTime\(\) \{[\s\S]*?el\.classList\.remove\(\'syncing\'\);\n\s*\}, 10000\);\n\s*\})', ref).group(1)
sync_init_js = re.search(r'(const initialSyncText = document\.querySelector\(\'\.sync-text\'\);\n\s*if \(initialSyncText\) initialSyncText\.innerHTML = `Last sync: \$\{formatSyncTime\(\)\}`;)', ref).group(1)

print("Extraction successful.")
