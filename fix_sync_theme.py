import re
import os

files = ['home.html', 'index.html', 'manifest.html', 'flightlog.html', 'risk-items.html']

for file in files:
    if not os.path.exists(file): continue
    
    with open(file, 'r') as f:
        content = f.read()
        
    print(f"\nChecking {file}:")
    has_theme = "function toggleTheme" in content
    has_sync = "function triggerManualSync" in content
    has_sync_init = "initialSyncText.innerHTML" in content
    print(f"Has theme: {has_theme}, Has sync: {has_sync}, Has sync init: {has_sync_init}")
