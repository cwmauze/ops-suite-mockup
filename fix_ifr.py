import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update AppState.legs
old_appstate = """        const AppState = {
            legs: [
                { id: 1, origin: 'RWI', dest: 'NC91', active: true },
                { id: 2, origin: 'NC91', dest: 'RWI', active: false }
            ]
        };"""
new_appstate = """        const AppState = {
            legs: [
                { id: 1, origin: 'RWI', dest: 'NC91', isIfr: false, active: true },
                { id: 2, origin: 'NC91', dest: 'RWI', isIfr: false, active: false }
            ]
        };"""
html = html.replace(old_appstate, new_appstate)

# 2. Update addLeg()
old_addleg = "AppState.legs.push({ id: newId, origin: origin, dest: '???', active: false });"
new_addleg = "AppState.legs.push({ id: newId, origin: origin, dest: '???', isIfr: false, active: false });"
html = html.replace(old_addleg, new_addleg)

# 3. Update HTML for ifr-toggle
old_toggle = '<input type="checkbox" id="ifr-toggle">'
new_toggle = '<input type="checkbox" id="ifr-toggle" onchange="updateCurrentLeg()">'
html = html.replace(old_toggle, new_toggle)

# 4. Update updateFormFromState()
old_form = """        function updateFormFromState() {
            const activeLeg = AppState.legs.find(l => l.active);
            if(activeLeg) {
                // document.getElementById('current-leg-title').innerText = `Leg ${activeLeg.id}`;
                document.getElementById('leg-origin').value = activeLeg.origin;
                document.getElementById('leg-dest').value = activeLeg.dest;
            } else {
                // document.getElementById('current-leg-title').innerText = ``;
                document.getElementById('leg-origin').value = '';
                document.getElementById('leg-dest').value = '';
            }
        }"""
new_form = """        function updateFormFromState() {
            const activeLeg = AppState.legs.find(l => l.active);
            if(activeLeg) {
                document.getElementById('leg-origin').value = activeLeg.origin;
                document.getElementById('leg-dest').value = activeLeg.dest;
                const toggle = document.getElementById('ifr-toggle');
                if (toggle) toggle.checked = activeLeg.isIfr || false;
            } else {
                document.getElementById('leg-origin').value = '';
                document.getElementById('leg-dest').value = '';
                const toggle = document.getElementById('ifr-toggle');
                if (toggle) toggle.checked = false;
            }
        }"""
html = html.replace(old_form, new_form)

# 5. Update updateCurrentLeg()
old_curr = """        function updateCurrentLeg() {
            const activeLeg = AppState.legs.find(l => l.active);
            if(activeLeg) {
                activeLeg.origin = document.getElementById('leg-origin').value;
                activeLeg.dest = document.getElementById('leg-dest').value;
                
                // re-render just the tabs to show updated text
                renderTabs();
            }
        }"""
new_curr = """        function updateCurrentLeg() {
            const activeLeg = AppState.legs.find(l => l.active);
            if(activeLeg) {
                activeLeg.origin = document.getElementById('leg-origin').value;
                activeLeg.dest = document.getElementById('leg-dest').value;
                const toggle = document.getElementById('ifr-toggle');
                if (toggle) activeLeg.isIfr = toggle.checked;
                
                // re-render just the tabs to show updated text
                renderTabs();
            }
        }"""
html = html.replace(old_curr, new_curr)

with open('index.html', 'w') as f:
    f.write(html)
print("Updated IFR toggle")
