import os
import re
from datetime import datetime

version = "0.0.27"
date = datetime.now().strftime("%Y-%m-%d")

html_files = ["index.html", "home.html", "manifest.html", "flightlog.html"]

new_html_changelog_entry = f"""                        <h4 style="margin-top:0; color:var(--accent-blue);">[{version}] - {date}</h4>
            <ul style="padding-left:20px; margin-bottom:15px; color:#ddd;">
                <li>Refactored the Mockup version and changelog UI to sit cleanly at the bottom of the left instructions panel.</li>
                <li>Made the changelog panel overlay available on all simulator pages (index, home, flightlog, manifest).</li>
                <li>Fixed CSS bugs to ensure the mockup version tag displays properly across all views in simulator mode.</li>
            </ul>
"""

for file in html_files:
    if os.path.exists(file):
        with open(file, "r") as f:
            content = f.read()
        
        # Update Mockup v0.0.26 to Mockup v0.0.27
        content = content.replace("Mockup v0.0.26", f"Mockup v{version}")
        
        # Update hardcoded changelog by prepending the new entry after the div padding line
        if '<div style="padding:20px; line-height:1.5; font-size: 0.95rem;">' in content:
            content = content.replace(
                '<div style="padding:20px; line-height:1.5; font-size: 0.95rem;">\n',
                f'<div style="padding:20px; line-height:1.5; font-size: 0.95rem;">\n{new_html_changelog_entry}'
            )
        elif '<div style="padding:20px; line-height:1.5; font-size: 0.95rem;">\n                        <h4' in content:
            pass # already handled if it matched above

        with open(file, "w") as f:
            f.write(content)

# Update CHANGELOG.md
with open("CHANGELOG.md", "r") as f:
    changelog = f.read()

new_md_entry = f"""## [{version}] - {date}
### Changed
- Refactored the Mockup version and changelog UI to sit cleanly at the bottom of the left instructions panel instead of floating randomly.
- Made the changelog panel overlay available on all simulator pages (index, home, flightlog, manifest).
- Fixed CSS scope bugs to ensure the mockup version tag and changelog display properly across all views in simulator mode, while still hiding seamlessly in native PWA mode.

"""

changelog = changelog.replace(
    "## [0.0.26]",
    new_md_entry + "## [0.0.26]"
)

with open("CHANGELOG.md", "w") as f:
    f.write(changelog)

print("Bumped version to", version)
