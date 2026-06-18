import re

with open('index.html', 'r') as f:
    html = f.read()

# Items to insert
new_items = """
                        <div style="background-color: var(--border-color); padding: 4px 12px; font-size:0.8rem; font-weight:bold; color:var(--text-secondary); text-transform:uppercase;">STATIC SCORE</div>
                        <div class="risk-item">
                            <div class="risk-text">1- Consecutive shifts > 7</div>
                            <div class="risk-pts">2 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="2" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">2- Consecutive night shifts > 4</div>
                            <div class="risk-pts">2 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="2" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">3- PIC < 1 YR or 100 flights at program</div>
                            <div class="risk-pts">2 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="2" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">4- Scene Flight w/ Medcrew Member(s) <6 mos @ Program</div>
                            <div class="risk-pts">2 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="2" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">5- PIC < 100 hours in type</div>
                            <div class="risk-pts">2 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="2" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">6- Last flight > 30 days</div>
                            <div class="risk-pts">2 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="2" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">7- Last Night and/or HNVGO flight > 30 days (Only applicable when conducting Night Flight)</div>
                            <div class="risk-pts">4 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="4" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">8- Last instrument approach > 30 days</div>
                            <div class="risk-pts">2 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="2" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">9- Relief Pilot new to local area and operating with an approved LBO Waiver</div>
                            <div class="risk-pts">3 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="3" onchange="calculateRisk()">
                        </div>
"""

# Find the start of the risk list
start_marker = '<div class="risk-list">'
start_idx = html.find(start_marker)

if start_idx != -1:
    # Find the start of item 10
    item10_idx = html.find('<div class="risk-item">\n                            <div class="risk-text">10-', start_idx)
    
    if item10_idx != -1:
        # replace everything from start of list to item 10 with new_items
        html = html[:start_idx + len(start_marker)] + "\n" + new_items + html[item10_idx:]

# Also update the tile text logic
# Initial text
html = html.replace('>Risk Form</button>', '>Risk Assessment</button>')

# dynamic text
old_js = """        function updateRiskTile() {
            const btn = document.getElementById('risk-btn');
            
            if (isRiskSigned) {
                btn.className = "tile green";
                btn.innerHTML = `Risk: ${currentRiskScore} ✓`;
                return;
            }
            
            btn.innerHTML = `Risk: ${currentRiskScore}`;"""

new_js = """        function updateRiskTile() {
            const btn = document.getElementById('risk-btn');
            btn.style.flexDirection = "column";
            btn.style.padding = "6px";
            
            let label = `<span style="font-size:0.6rem; text-transform:uppercase;">Risk Assmt</span>`;
            
            if (isRiskSigned) {
                btn.className = "tile green";
                btn.innerHTML = `${label}<span style="font-size:1rem; font-weight:bold; margin-top:2px;">${currentRiskScore} ✓</span>`;
                return;
            }
            
            btn.innerHTML = `${label}<span style="font-size:1rem; font-weight:bold; margin-top:2px;">${currentRiskScore} pts</span>`;"""

html = html.replace(old_js, new_js)

with open('index.html', 'w') as f:
    f.write(html)
print("Updated index.html")
