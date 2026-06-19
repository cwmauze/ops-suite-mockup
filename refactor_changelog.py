import re
import sys

def get_changelog_panel():
    with open('flightlog.html', 'r') as f:
        html = f.read()
    
    # Extract changelog panel
    start_idx = html.find('<!-- Changelog Side Panel -->')
    if start_idx == -1:
        start_idx = html.find('<div id="changelog-panel"')
        
    if start_idx == -1:
        return ""
        
    # Find the end of the div. 
    # It ends with '    </div>\n</body>' in flightlog.html
    end_idx = html.find('</body>', start_idx)
    panel = html[start_idx:end_idx].strip()
    return panel

def process_file(filename, panel_html):
    with open(filename, 'r') as f:
        html = f.read()

    # 1. Update .mockup-version CSS
    old_css = """        .mockup-version {
            position: fixed;
            bottom: 20px;
            right: 20px;
            color: #888;
            font-family: monospace;
            font-size: 1rem;
            z-index: 9999;
            cursor: pointer;
            padding: 5px 10px;
            background: rgba(0,0,0,0.5);
            border-radius: 6px;
        }
        .mockup-version:hover {
            color: #fff;
            background: rgba(0,0,0,0.8);
        }"""
        
    new_css = """        .mockup-version {
            margin-top: auto;
            color: #888;
            font-family: monospace;
            font-size: 1rem;
            cursor: pointer;
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 6px;
            text-align: center;
            border: 1px solid #444;
        }
        .mockup-version:hover {
            color: #fff;
            background: rgba(0,0,0,0.6);
        }"""

    if old_css in html:
        html = html.replace(old_css, new_css)

    # 2. Move .mockup-version html tag inside #desktop-instructions
    version_tag_regex = r'<div class="mockup-version" onclick="toggleChangelog\(\)">Mockup v0\.0\.\d+</div>\n\s*'
    match = re.search(r'<div class="mockup-version" onclick="toggleChangelog\(\)">(Mockup v0\.0\.\d+)</div>', html)
    version_text = "Mockup v0.0.26"
    if match:
        version_text = match.group(1)
        
    html = re.sub(version_tag_regex, '', html)

    desktop_inst_end = """            </ol>
        </div>
    </div>"""
    
    new_desktop_inst_end = f"""            </ol>
        </div>
        <div class="mockup-version" onclick="toggleChangelog()">{version_text}</div>
    </div>"""
    
    if desktop_inst_end in html:
        html = html.replace(desktop_inst_end, new_desktop_inst_end)

    # 3. Handle changelog panel
    # First remove existing panel if any
    start_idx = html.find('<!-- Changelog Side Panel -->')
    if start_idx == -1:
        start_idx = html.find('<div id="changelog-panel"')
        
    if start_idx != -1:
        end_idx = html.find('</body>', start_idx)
        if end_idx != -1:
            html = html[:start_idx] + html[end_idx:]
    
    # Now insert the panel right before </body>
    if panel_html:
        html = html.replace('</body>', f'\n{panel_html}\n</body>')

    with open(filename, 'w') as f:
        f.write(html)
    print(f"Processed {filename}")

panel_html = get_changelog_panel()

# Modify the styling of the panel to overlay the instructions panel
old_style = 'style="display:none; width: 400px; height: 100%; background:#222; color:#fff; flex-direction:column; font-family:-apple-system, BlinkMacSystemFont, sans-serif; border-left: 2px solid #444; overflow-y:auto; box-shadow: -5px 0 15px rgba(0,0,0,0.5); z-index: 10000; flex-shrink: 0;"'
new_style = 'style="display:none; position:absolute; left:0; top:0; bottom:0; width:350px; background:#222; color:#fff; flex-direction:column; font-family:-apple-system, BlinkMacSystemFont, sans-serif; border-right: 1px solid #444; overflow-y:auto; box-shadow: 5px 0 15px rgba(0,0,0,0.5); z-index: 10000;"'

if panel_html and old_style in panel_html:
    panel_html = panel_html.replace(old_style, new_style)

if panel_html:
    files = ['index.html', 'home.html', 'manifest.html', 'flightlog.html']
    for f in files:
        process_file(f, panel_html)
else:
    print("Could not extract panel_html")
