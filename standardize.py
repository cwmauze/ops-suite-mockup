import re
import os

files = ['index.html', 'home.html', 'manifest.html', 'risk-items.html']

js_to_inject = """
        const themes = ['light', 'neutral', 'dark', 'hc-dark', 'hc-light'];
        function toggleTheme() {
            const html = document.documentElement;
            let current = html.getAttribute('data-theme') || 'light';
            let nextIndex = (themes.indexOf(current) + 1) % themes.length;
            html.setAttribute('data-theme', themes[nextIndex]);
        }

        function formatSyncTime() {
            const now = new Date();
            return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }

        function triggerManualSync(el) {
            if (el.classList.contains('syncing')) return;
            el.classList.add('syncing');
            const icon = el.querySelector('.sync-icon');
            const text = el.querySelector('.sync-text');
            icon.innerHTML = '↻';
            icon.style.animation = 'spin 1s linear infinite';
            icon.style.color = 'var(--accent-blue)';
            text.innerHTML = 'Syncing...';
            setTimeout(() => {
                icon.style.animation = 'none';
                icon.innerHTML = '✔';
                icon.style.color = 'var(--accent-green)';
                text.innerHTML = `Last sync: ${formatSyncTime()}`;
                el.classList.remove('syncing');
            }, 10000);
        }

        window.addEventListener('DOMContentLoaded', () => {
            const initialSyncText = document.querySelector('.sync-text');
            if (initialSyncText) initialSyncText.innerHTML = `Last sync: ${formatSyncTime()}`;
        });
"""

sync_bar_html = """
            <!-- Sync Bar -->
            <div class="sync-bar">
                <button class="theme-toggle" onclick="toggleTheme()" style="background:none; border: 1px solid var(--border-color); color: var(--text-primary); padding: 4px 8px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 1rem;">🌓</button>
                <div style="cursor: pointer; display: flex; align-items: center; gap: 4px;" onclick="triggerManualSync(this)">
                    <span class="sync-icon">✔</span> <span class="sync-text">Last sync: Just now</span>
                </div>
            </div>
"""

bottom_nav_html_base = """
            <!-- Bottom Navigation -->
            <nav class="bottom-nav">
                <div class="nav-item {home_active}" onclick="window.location.href='home.html'" style="cursor:pointer;">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
                    <span>Home</span>
                </div>
                <div class="nav-item {manifest_active}" onclick="window.location.href='manifest.html'" style="cursor:pointer;">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"></path></svg>
                    <span>Manifest</span>
                </div>
                <div class="nav-item">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"></path></svg>
                    <span>Weather</span>
                </div>
                <div class="nav-item">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M21 3H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H3V5h18v14zm-10-7h9v6h-9z"></path></svg>
                    <span>Company</span>
                </div>
                <div class="nav-item">
                    <svg class="nav-icon" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"></path></svg>
                    <span>Profile</span>
                </div>
            </nav>
"""

for file in files:
    if not os.path.exists(file): continue
    print(f"Processing {file}...")
    with open(file, 'r') as f:
        content = f.read()
        
    # Inject JS
    if "function toggleTheme()" not in content:
        # insert before </script>
        script_end = content.rfind('</script>')
        if script_end != -1:
            content = content[:script_end] + js_to_inject + content[script_end:]
            print("  - JS injected")
            
    # Inject Sync HTML
    if '<div class="sync-bar">' not in content:
        # insert right after <div class="device-screen">
        screen_start = content.find('<div class="device-screen">')
        if screen_start != -1:
            # find the end of the line containing <div class="device-screen">
            line_end = content.find('\n', screen_start)
            content = content[:line_end] + "\n" + sync_bar_html + content[line_end:]
            print("  - Sync HTML injected")
            
    # Inject Nav HTML
    if '<nav class="bottom-nav">' not in content and '<div class="bottom-nav">' not in content:
        # insert just before <!-- Simulated Home Indicator -->
        indicator_idx = content.find('<!-- Simulated Home Indicator -->')
        if indicator_idx == -1:
            indicator_idx = content.find('<div class="simulated-indicator">')
        if indicator_idx != -1:
            is_home = 'active' if file in ['home.html', 'index.html'] else ''
            is_manifest = 'active' if file in ['manifest.html', 'flightlog.html'] else ''
            nav = bottom_nav_html_base.replace('{home_active}', is_home).replace('{manifest_active}', is_manifest)
            content = content[:indicator_idx] + nav + "\n" + content[indicator_idx:]
            print("  - Nav HTML injected")
    elif '<nav class="bottom-nav">' in content or '<div class="bottom-nav">' in content:
        # If it already has it, we just update the active class manually
        print("  - Nav already exists, updating active classes")
        # remove existing active classes from nav-item
        content = re.sub(r'class="nav-item active"', 'class="nav-item"', content)
        # set the correct one
        if file in ['home.html', 'index.html']:
            content = content.replace('<span>Home</span>', '<span data-active="true">Home</span>')
            content = re.sub(r'<div class="nav-item"([^>]*)>\s*(<svg[^>]*>.*?</svg>)\s*<span data-active="true">Home</span>', r'<div class="nav-item active"\1>\n                    \2\n                    <span>Home</span>', content, flags=re.DOTALL)
        elif file in ['manifest.html', 'flightlog.html']:
            content = content.replace('<span>Manifest</span>', '<span data-active="true">Manifest</span>')
            content = re.sub(r'<div class="nav-item"([^>]*)>\s*(<svg[^>]*>.*?</svg>)\s*<span data-active="true">Manifest</span>', r'<div class="nav-item active"\1>\n                    \2\n                    <span>Manifest</span>', content, flags=re.DOTALL)
            
    # Make sure html tag has data-theme="light"
    if '<html lang="en">' in content:
        content = content.replace('<html lang="en">', '<html lang="en" data-theme="light">')
        
    with open(file, 'w') as f:
        f.write(content)

print("Standardization complete.")
