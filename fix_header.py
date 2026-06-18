import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace HTML
old_html = """                    <div style="display: flex; flex-direction: column; gap: 4px; justify-content: center; min-width: 120px;">
                        <div class="aircraft-title">Aircraft: N850BU</div>
                        <div class="manifest-number">Manifest: 3664365</div>
                        <div class="team-badge" style="font-size: 0.85rem; color: var(--accent-blue); font-weight: bold; cursor: pointer; text-transform: uppercase;">👥 RWI Medical Team</div>
                    </div>"""
new_html = """                    <div style="display: flex; flex-direction: column; gap: 4px; justify-content: center; min-width: 120px;">
                        <div class="manifest-title" style="font-size: 1.2rem; font-weight: 700;">Manifest: 3664365</div>
                        <div class="aircraft-number" style="font-size: 0.95rem; color: var(--text-secondary); font-weight: bold;">N850BU</div>
                        <div class="team-badge" style="font-size: 0.85rem; color: var(--accent-blue); font-weight: bold; cursor: pointer; text-transform: uppercase;">👥 RWI Medical Team</div>
                    </div>"""

html = html.replace(old_html, new_html)

with open('index.html', 'w') as f:
    f.write(html)

print("Updated header")
