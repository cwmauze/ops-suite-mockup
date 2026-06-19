import re
import os

files = ['home.html', 'manifest.html']

correct_nav_html_base = """
            <!-- Bottom Navigation -->
            <div class="bottom-nav">
                <div class="nav-item {home_active}" onclick="window.location.href='home.html'" style="cursor:pointer;">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
                    <span>Home</span>
                </div>
                <div class="nav-item" style="cursor:pointer;">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path></svg>
                    <span>Map</span>
                </div>
                <div class="nav-item {manifest_active}" onclick="window.location.href='manifest.html'" style="cursor:pointer;">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    <span>Manifest</span>
                </div>
                <div class="nav-item">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                    <span>Library</span>
                </div>
                <div class="nav-item">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
                    <span>Chat</span>
                </div>
            </div>
"""

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # Step 1: Remove the old nav
    # The old nav could be <nav class="bottom-nav"> ... </nav>
    # We will find it and remove it
    old_nav_start = content.find('<!-- Bottom Navigation -->')
    if old_nav_start != -1:
        old_nav_end = content.find('</nav>', old_nav_start)
        if old_nav_end != -1:
            content = content[:old_nav_start] + content[old_nav_end+6:]
            
    # Also in case there's a div bottom-nav we need to remove
    old_nav_start_div = content.find('<!-- Bottom Navigation -->')
    if old_nav_start_div != -1:
        old_nav_end_div = content.find('</div>\n    </div>\n    </div>\n\n    <!-- Leaflet JS -->', old_nav_start_div)
        if old_nav_end_div != -1:
            pass # Actually string replacement is easier via regex if it varies

    # Let's just use regex to cleanly rip out the old nav block regardless of what it is
    content = re.sub(r'<!-- Bottom Navigation -->[\s\S]*?(?:</nav>|</div>(?=\s*</div>\s*<!-- Leaflet JS -->|</div>\s*</div>\s*<!-- Leaflet JS -->))', '', content)
    
    # Let's clean up any lingering </nav> just in case
    content = content.replace('</nav>', '')

    # Step 2: Inject the correct nav right before `</div> <!-- End Device Screen -->`
    # Let's find `</div> <!-- End Device Screen -->`
    device_screen_end = content.find('</div> <!-- End Device Screen -->')
    if device_screen_end != -1:
        is_home = 'active' if file == 'home.html' else ''
        is_manifest = 'active' if file == 'manifest.html' else ''
        nav_html = correct_nav_html_base.replace('{home_active}', is_home).replace('{manifest_active}', is_manifest)
        
        content = content[:device_screen_end] + nav_html + "\n        " + content[device_screen_end:]
        
    with open(file, 'w') as f:
        f.write(content)

print("Navigation fixed in home.html and manifest.html")
