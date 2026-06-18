import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add formatSyncTime and initialization
init_block = """        // Initialize
        renderTabs();
        calculateRisk();"""

new_init_block = """        function formatSyncTime() {
            const now = new Date();
            return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }

        // Initialize
        renderTabs();
        calculateRisk();
        const initialSyncText = document.querySelector('.sync-text');
        if (initialSyncText) initialSyncText.innerHTML = `Last sync: ${formatSyncTime()}`;"""

html = html.replace(init_block, new_init_block)

# 2. Update triggerManualSync
old_sync_logic = """            setTimeout(() => {
                icon.style.animation = 'none';
                icon.innerHTML = '✔';
                icon.style.color = 'var(--accent-green)';
                text.innerHTML = 'Last sync: Just now';
                el.classList.remove('syncing');
            }, 10000);"""

new_sync_logic = """            setTimeout(() => {
                icon.style.animation = 'none';
                icon.innerHTML = '✔';
                icon.style.color = 'var(--accent-green)';
                text.innerHTML = `Last sync: ${formatSyncTime()}`;
                el.classList.remove('syncing');
            }, 10000);"""

html = html.replace(old_sync_logic, new_sync_logic)

with open('index.html', 'w') as f:
    f.write(html)
print("Updated sync logic")
