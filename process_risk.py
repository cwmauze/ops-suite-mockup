import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update risk-item HTML
# Find the start and end of the risk list
start_marker = '<div class="risk-list">'
end_marker = '</div>\n                    <div style="background-color: var(--surface-color)'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)

risk_list_html = html[start_idx:end_idx]

def replace_item(match):
    content = match.group(0)
    
    # Extract points
    pts_match = re.search(r'>\s*(-?\d+)\s*pts\s*<', content)
    if pts_match:
        pts = int(pts_match.group(1))
    else:
        pts = 0
        
    # Check if checkbox already exists
    if '<input type="checkbox"' not in content:
        # insert checkbox before the closing div
        content = content.replace('</div>\n                        </div>', '</div>\n                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="' + str(pts) + '" onchange="calculateRisk()">\n                        </div>')
    else:
        # replace existing checkbox
        content = re.sub(r'<input type="checkbox"[^>]*>', '<input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="' + str(pts) + '" onchange="calculateRisk()">', content)
    
    return content

# apply to all risk items
new_risk_list_html = re.sub(r'<div class="risk-item">[\s\S]*?</div>\n                        </div>', replace_item, risk_list_html)

# Now inject JS logic
js_logic = """
        let currentRiskScore = 0;
        let isRiskSigned = false;

        function calculateRisk() {
            let total = 0;
            document.querySelectorAll('.risk-checkbox').forEach(cb => {
                if (cb.checked) {
                    total += parseInt(cb.getAttribute('data-pts') || 0, 10);
                }
            });
            currentRiskScore = total;
            document.getElementById('risk-pill').innerText = total;
            updateRiskTile();
        }

        function toggleRiskSignature(checked) {
            isRiskSigned = checked;
            updateRiskTile();
        }

        function updateRiskTile() {
            const btn = document.getElementById('risk-btn');
            
            if (isRiskSigned) {
                btn.className = "tile green";
                btn.innerHTML = `Risk: ${currentRiskScore} ✓`;
                return;
            }
            
            btn.innerHTML = `Risk: ${currentRiskScore}`;
            
            if (currentRiskScore <= 15) {
                btn.className = "tile green";
            } else if (currentRiskScore <= 20) {
                btn.className = "tile orange";
            } else {
                btn.className = "tile red";
            }
        }
"""

html = html[:start_idx] + new_risk_list_html + html[end_idx:]

# Update the toggleRiskSignature function logic that we added earlier
old_func = """        function toggleRiskSignature(checked) {
            const btn = document.getElementById('risk-btn');
            if (checked) {
                btn.className = "tile green";
                btn.innerHTML = "Risk Pass";
            } else {
                btn.className = "tile orange";
                btn.innerHTML = "Risk Form";
            }
        }"""
html = html.replace(old_func, js_logic)

# Make sure risk-pill has an id
html = html.replace('<div class="risk-pill">0</div>', '<div class="risk-pill" id="risk-pill">0</div>')

# Initialize tile on load
html = html.replace('// Initialize state', '// Initialize state\n        calculateRisk();')

with open('index.html', 'w') as f:
    f.write(html)
print("Updated index.html")
