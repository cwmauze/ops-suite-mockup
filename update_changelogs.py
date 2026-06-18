import re

with open('CHANGELOG.md', 'r') as f:
    changelog_md = f.read()

new_md_entry = """## [0.0.24] - 2026-06-18
### Added
- Created a custom 24-hour iOS-style Time Picker with scroll-snapping rollers to streamline minute-by-minute adjustments, bypassing the clunky native iOS `datetime-local` picker.
- Implemented dynamic Risk Assessment logic containing all 46 risk items. The dashboard tile automatically calculates the score, updates the pill, and changes color (Green/Orange/Red) based on the current threshold.
- Added a "Sign to Approve" toggle in the Risk Assessment modal. When activated, it forces the dashboard tile to green and appends a "✓" symbol.
- Refactored the Fuel section to fit Supply Tanks, Main tanks, Burn Rate, Fuel time, and S.O.B. into a single, compact horizontal row.
- Bound the "IFR leg" toggle to the underlying `AppState` engine so it tracks securely on a per-leg basis, defaulting to OFF for newly created legs.
- Implemented a tiered UI decluttering system for Leg tabs to automatically compress text length and prevent horizontal scrolling as more legs are added.
- Added dynamic local timestamps to the "Last sync" status so it reflects the exact time of page load and updates upon manual sync completion.

### Changed
- Renamed the dashboard "Risk Form" tile to "Risk Assessment".
- Moved the Leg deletion action from an inline "x" on the tabs to a dedicated, red-outlined `Delete Leg` button at the bottom of the screen with a confirmation prompt to prevent accidental fat-finger deletions.

"""

# Insert right after the header
changelog_md = changelog_md.replace("## [0.0.23]", new_md_entry + "## [0.0.23]")

# Also clean up line 1 of CHANGELOG.md if it got corrupted:
if changelog_md.startswith("Let's# Changelog"):
    changelog_md = changelog_md.replace("Let's# Changelog", "# Changelog")

with open('CHANGELOG.md', 'w') as f:
    f.write(changelog_md)


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

html = html.replace('<h4 style="margin-top:0; color:var(--accent-blue);">[0.0.23]', html_entry + '            <h4 style="color:var(--accent-blue);">[0.0.23]')

with open('index.html', 'w') as f:
    f.write(html)

print("Updated changelogs")
