import re
import sys

def fix_css(filename):
    with open(filename, 'r') as f:
        html = f.read()

    # We want to change:
    #         .mockup-version {
    #             display: none !important;
    #         }
    # To:
    #         body.native-mode .mockup-version {
    #             display: none !important;
    #         }
    
    # Let's use regex
    target = r'\.mockup-version\s*{\s*display:\s*none\s*!important;\s*}'
    replacement = r'body.native-mode .mockup-version {\n            display: none !important;\n        }'
    
    new_html = re.sub(target, replacement, html)
    
    if new_html != html:
        with open(filename, 'w') as f:
            f.write(new_html)
        print(f"Fixed {filename}")
    else:
        print(f"No match in {filename}")

files = ['index.html', 'home.html', 'manifest.html', 'flightlog.html']
for f in files:
    fix_css(f)
