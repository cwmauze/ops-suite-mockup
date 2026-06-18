import re

with open('index.html', 'r') as f:
    html = f.read()

new_items = """
                        <div class="risk-item">
                            <div class="risk-text">38- Use of a pre-designated LZ at a scene</div>
                            <div class="risk-pts">-1 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="-1" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">39- Add extra fuel stop</div>
                            <div class="risk-pts">-1 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="-1" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">40- Change route to avoid hazardous terrain or weather</div>
                            <div class="risk-pts">-1 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="-1" onchange="calculateRisk()">
                        </div>
                        
                        <div style="background-color: var(--border-color); padding: 4px 12px; font-size:0.8rem; font-weight:bold; color:var(--text-secondary); text-transform:uppercase; margin-top: 15px;">TURNDOWN</div>
                        <div class="risk-item">
                            <div class="risk-text">41- Weather Conditions are Unacceptable</div>
                            <div class="risk-pts">35 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="35" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">42- Medical Crew Declined Flight Request</div>
                            <div class="risk-pts">35 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="35" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">43- Insufficient Duty Time available</div>
                            <div class="risk-pts">35 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="35" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">44- Aircraft Range Inadequate</div>
                            <div class="risk-pts">35 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="35" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">45- Aircraft Performance or Equipment Inadequate</div>
                            <div class="risk-pts">35 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="35" onchange="calculateRisk()">
                        </div>
                        <div class="risk-item">
                            <div class="risk-text">46- Other (explain briefly in comments)</div>
                            <div class="risk-pts">35 pts</div>
                            <input type="checkbox" class="risk-checkbox" style="width:24px; height:24px;" data-pts="35" onchange="calculateRisk()">
                        </div>
"""

# Insert these at the end of the risk-list
list_end_idx = html.find('</div>\n                    <div style="background-color: var(--surface-color)')
if list_end_idx != -1:
    html = html[:list_end_idx] + new_items + html[list_end_idx:]

with open('index.html', 'w') as f:
    f.write(html)
print("Updated index.html")
