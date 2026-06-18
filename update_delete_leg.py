import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove the close-btn from renderTabs
old_tab = """                    ${labelText}
                    <span class="close-btn" onclick="removeLeg(${leg.id}, event)">×</span>
                `;"""
new_tab = """                    ${labelText}
                `;"""
html = html.replace(old_tab, new_tab)

# 2. Add Delete Leg button
old_footer = """            <!-- Fixed Action Buttons Footer -->
            <div style="flex-shrink: 0; width: 100%; box-sizing: border-box; background-color: var(--surface-color); padding: 8px 12px; border-top: 1px solid var(--border-color); z-index: 40; display: flex; align-items: center; gap: 10px;">
                <button class="btn btn-primary">Save</button>
                <button class="btn btn-primary" onclick="handleSaveAddLeg()">Save/Add Leg</button>
                <button class="btn btn-danger" onclick="openModal('close-modal')">Close Flt</button>
                <div class="verify-wrapper" style="margin-left: auto;">"""

new_footer = """            <!-- Fixed Action Buttons Footer -->
            <div style="flex-shrink: 0; width: 100%; box-sizing: border-box; background-color: var(--surface-color); padding: 8px 12px; border-top: 1px solid var(--border-color); z-index: 40; display: flex; align-items: center; gap: 8px; overflow-x: auto;">
                <button class="btn btn-primary" style="padding: 6px 10px; font-size: 0.8rem;">Save</button>
                <button class="btn btn-primary" onclick="handleSaveAddLeg()" style="padding: 6px 10px; font-size: 0.8rem;">Save/Add Leg</button>
                <button class="btn btn-outline" onclick="deleteCurrentLeg()" style="color:var(--accent-red); border-color:var(--accent-red); padding: 6px 10px; font-size: 0.8rem;">Delete Leg</button>
                <button class="btn btn-danger" onclick="openModal('close-modal')" style="padding: 6px 10px; font-size: 0.8rem;">Close Flt</button>
                <div class="verify-wrapper" style="margin-left: auto; flex-shrink: 0;">"""
html = html.replace(old_footer, new_footer)

# 3. Add deleteCurrentLeg function
js_to_insert = """        function deleteCurrentLeg() {
            const activeLeg = AppState.legs.find(l => l.active);
            if (activeLeg) {
                if (confirm(`Are you sure you want to delete Leg ${activeLeg.id} (${activeLeg.origin} ➔ ${activeLeg.dest})?`)) {
                    removeLeg(activeLeg.id, {stopPropagation: () => {}});
                }
            }
        }
"""
# insert before handleSaveAddLeg()
html = html.replace('        function handleSaveAddLeg() {', js_to_insert + '        function handleSaveAddLeg() {')

with open('index.html', 'w') as f:
    f.write(html)
print("Updated delete leg")
