import os
import re
from datetime import datetime

version = "0.0.26"
date = datetime.now().strftime("%Y-%m-%d")

html_files = ["index.html", "home.html", "manifest.html", "flightlog.html"]

new_html_changelog_entry = f"""                        <h4 style="margin-top:0; color:var(--accent-blue);">[{version}] - {date}</h4>
            <ul style="padding-left:20px; margin-bottom:15px; color:#ddd;">
                <li>Applied global theme toggle logic across all pages, saving preferences to localStorage.</li>
                <li>Unified theme CSS variables for seamless light/dark/high-contrast mode switching.</li>
            </ul>
"""

for file in html_files:
    if os.path.exists(file):
        with open(file, "r") as f:
            content = f.read()
        
        # Update Mockup v0.0.25 to Mockup v0.0.26
        content = content.replace("Mockup v0.0.25", f"Mockup v{version}")
        
        # Update hardcoded changelog by prepending the new entry after the div padding line
        # Wait, the structure is:
        # <div style="padding:20px; line-height:1.5; font-size: 0.95rem;">
        #                 <h4 style="margin-top:0; color:var(--accent-blue);">[0.0.25] - 2026-06-18</h4>
        if '<div style="padding:20px; line-height:1.5; font-size: 0.95rem;">' in content:
            content = content.replace(
                '<div style="padding:20px; line-height:1.5; font-size: 0.95rem;">\n',
                f'<div style="padding:20px; line-height:1.5; font-size: 0.95rem;">\n{new_html_changelog_entry}'
            )

        with open(file, "w") as f:
            f.write(content)

# Update CHANGELOG.md
with open("CHANGELOG.md", "r") as f:
    changelog = f.read()

new_md_entry = f"""## [{version}] - {date}
### Added
- Applied global theme toggle logic across all pages.
- Saved user theme preferences to `localStorage` for cross-page persistence.
- Unified theme CSS variables for seamless light/dark/high-contrast mode switching across all layouts.

"""

changelog = changelog.replace(
    "## [0.0.25]",
    new_md_entry + "## [0.0.25]"
)

with open("CHANGELOG.md", "w") as f:
    f.write(changelog)
