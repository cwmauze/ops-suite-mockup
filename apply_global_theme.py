import os
import re

files = ['home.html', 'index.html', 'manifest.html', 'flightlog.html']

theme_css = """
        /* Universal Theme overrides */
        [data-theme="light"] {
            --bg-color: #f0f2f5;
            --surface-color: #ffffff;
            --surface-color-light: #f8f9fa;
            --text-primary: #111111;
            --text-secondary: #666666;
            --border-color: #dddddd;
            --input-bg: #ffffff;
            --toggle-off: #cccccc;
            --bg-body: #f1f2f5;
            --bg-card: #ffffff;
            --text-main: #181c20;
            --text-muted: #5e646e;
        }

        [data-theme="neutral"] {
            --bg-color: #2b2b2b;
            --surface-color: #3b3b3b;
            --surface-color-light: #4b4b4b;
            --text-primary: #f0f0f0;
            --text-secondary: #c0c0c0;
            --border-color: #555555;
            --input-bg: #444444;
            --toggle-off: #666666;
            --bg-body: #2b2b2b;
            --bg-card: #3b3b3b;
            --text-main: #f0f0f0;
            --text-muted: #c0c0c0;
        }

        [data-theme="dark"] {
            --bg-color: #000000;
            --surface-color: #111111;
            --surface-color-light: #222222;
            --text-primary: #ffffff;
            --text-secondary: #aaaaaa;
            --border-color: #333333;
            --input-bg: #1a1a1a;
            --toggle-off: #444444;
            --bg-body: #000000;
            --bg-card: #111111;
            --text-main: #ffffff;
            --text-muted: #aaaaaa;
        }

        [data-theme="hc-dark"] {
            --bg-color: #000000;
            --surface-color: #000000;
            --surface-color-light: #000000;
            --text-primary: #ffffff;
            --text-secondary: #dddddd;
            --accent-blue: #55aaff;
            --accent-orange: #ffaa55;
            --accent-green: #55ff55;
            --accent-red: #ff5555;
            --border-color: #ffffff;
            --input-bg: #000000;
            --toggle-off: #ffffff;
            --bg-body: #000000;
            --bg-card: #000000;
            --text-main: #ffffff;
            --text-muted: #dddddd;
        }

        [data-theme="hc-light"] {
            --bg-color: #ffffff;
            --surface-color: #ffffff;
            --surface-color-light: #ffffff;
            --text-primary: #000000;
            --text-secondary: #000000;
            --accent-blue: #0000ee;
            --accent-orange: #cc5500;
            --accent-green: #008800;
            --accent-red: #cc0000;
            --border-color: #000000;
            --input-bg: #ffffff;
            --toggle-off: #000000;
            --bg-body: #ffffff;
            --bg-card: #ffffff;
            --text-main: #000000;
            --text-muted: #000000;
        }
"""

js_code = """
        const themes = ['light', 'neutral', 'dark', 'hc-dark', 'hc-light'];
        function toggleTheme() {
            const html = document.documentElement;
            let current = html.getAttribute('data-theme') || 'light';
            let nextIndex = (themes.indexOf(current) + 1) % themes.length;
            let nextTheme = themes[nextIndex];
            html.setAttribute('data-theme', nextTheme);
            localStorage.setItem('ops_suite_theme', nextTheme);
        }

        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('ops_suite_theme');
            if (savedTheme) {
                document.documentElement.setAttribute('data-theme', savedTheme);
            }
        });
"""

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # 1. Replace the toggleTheme JS function
    # Find the function toggleTheme block
    # It might be: const themes = [...]; \n function toggleTheme() { ... }
    # Let's just find and replace the whole thing or inject.
    content = re.sub(
        r'const themes = \[\'light\', \'neutral\', \'dark\', \'hc-dark\', \'hc-light\'\];\s*function toggleTheme\(\) \{[\s\S]*?\}',
        js_code.strip(),
        content
    )

    # 2. Inject CSS if not present
    # Remove existing data-theme blocks in flightlog.html to replace them with universal ones
    content = re.sub(r'\[data-theme="light"\] \{[\s\S]*?\}\s*\[data-theme="neutral"\] \{[\s\S]*?\}\s*\[data-theme="hc-dark"\] \{[\s\S]*?\}\s*\[data-theme="hc-light"\] \{[\s\S]*?\}', '', content)
    
    # Also clean up any other stray single data-theme block in case others had them
    content = re.sub(r'\[data-theme="light"\] \{[\s\S]*?\}', '', content)
    
    # Inject our universal theme_css right after :root { ... }
    # Wait, some files might not have :root. But they all do.
    content = re.sub(r'(:root \{[\s\S]*?\})', r'\1' + '\n' + theme_css, content)

    # Note: index.html has an extra copy of `function toggleTheme()` near the top. Let's clean up duplicate script blocks if necessary, but the regex above might replace all of them.
    
    with open(file, 'w') as f:
        f.write(content)

    print(f"Updated {file}")
