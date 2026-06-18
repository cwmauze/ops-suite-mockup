import re

with open('index.html', 'r') as f:
    html = f.read()

with open('risk-items.html', 'r') as f:
    items = f.read()

start_marker = '<div class="risk-list">'
end_marker = '</div>\n                </div>\n                <div class="modal-footer">'

start_idx = html.find(start_marker)
if start_idx != -1:
    end_idx = html.find(end_marker, start_idx)
    if end_idx != -1:
        new_list = '<div class="risk-list">\n' + items + '\n                    </div>\n'
        
        sign_block = '''                    <div style="background-color: var(--surface-color); padding: 15px; margin-top: 15px; border-radius: 8px; border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                        <span style="font-weight:bold; font-size:1.1rem;">Sign to Approve</span>
                        <label class="switch">
                            <input type="checkbox" id="risk-sign-toggle" onchange="toggleRiskSignature(this.checked)">
                            <span class="slider"></span>
                        </label>
                    </div>
'''
        
        new_html = html[:start_idx] + new_list + sign_block + html[end_idx + len('</div>\n'):]
        
        func = '''
        function toggleRiskSignature(checked) {
            const btn = document.getElementById('risk-btn');
            if (checked) {
                btn.className = "tile green";
                btn.innerHTML = "Risk Pass";
            } else {
                btn.className = "tile orange";
                btn.innerHTML = "Risk Form";
            }
        }
        '''
        new_html = new_html.replace('</script>', func + '\n    </script>')
        
        with open('index.html', 'w') as f:
            f.write(new_html)
        print("Updated index.html")
    else:
        print("End marker not found")
else:
    print("Start marker not found")
