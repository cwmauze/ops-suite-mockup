function toggleChangelog() {
    const panel = document.getElementById('changelog-panel');
    if(panel) {
        if(panel.style.display === 'none' || panel.style.display === '') {
            panel.style.display = 'flex';
        } else {
            panel.style.display = 'none';
        }
    }
}

async function loadChangelog() {
    try {
        const response = await fetch('CHANGELOG.md?v=' + new Date().getTime());
        if (!response.ok) {
            console.warn("Could not fetch CHANGELOG.md", response.status);
            return;
        }
        const text = await response.text();
        
        const container = document.getElementById('changelog-content');
        if (!container) return;
        
        let html = '';
        let inList = false;
        
        const lines = text.split('\n');
        for (let line of lines) {
            line = line.trim();
            if (line.startsWith('## [')) {
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                const versionHeader = line.substring(3); // "[0.1.8] - 2026-06-19"
                html += `<h4 style="margin-top:${html === '' ? '0' : '20px'}; color:var(--accent-blue);">${versionHeader}</h4>`;
            } else if (line.startsWith('### ')) {
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                const subHeader = line.substring(4);
                html += `<h5 style="margin-top:10px; margin-bottom:5px; color:#aaa;">${subHeader}</h5>`;
            } else if (line.startsWith('- ')) {
                if (!inList) {
                    html += '<ul style="padding-left:20px; margin-bottom:15px; color:#ddd;">';
                    inList = true;
                }
                // Escape < and > to prevent script tags from breaking HTML
                const content = line.substring(2).replace(/</g, "&lt;").replace(/>/g, "&gt;");
                html += `<li style="margin-bottom:4px;">${content}</li>`;
            }
        }
        if (inList) {
            html += '</ul>';
        }
        
        container.innerHTML = html;
        
    } catch (e) {
        console.error('Failed to load changelog:', e);
    }
}

window.addEventListener('DOMContentLoaded', loadChangelog);
