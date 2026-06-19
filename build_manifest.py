import re

def main():
    # Read the current manifest.html
    # wait, manifest.html is currently identical to flightlog.html
    # We should grab home.html since it is cleaner and doesn't have the back button in the header
    # and has the proper "New Manifest" button (though we will replace the content anyway)
    # Actually, we can just use manifest.html, but let's make sure the .app-icon is just the logo
    
    with open('home.html', 'r') as f:
        content = f.read()

    # Step 1: Inject CSS
    css = """
        /* Manifest List Styles */
        .manifest-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        .manifest-title-group {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .manifest-title {
            font-size: 24px;
            font-weight: 800;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .manifest-badge {
            background-color: #e5e7eb;
            color: #4b5563;
            font-size: 14px;
            font-weight: 700;
            padding: 2px 10px;
            border-radius: 12px;
        }
        .manifest-card {
            background-color: white;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid var(--border-color);
            margin-bottom: 16px;
            display: flex;
            overflow: hidden;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            transition: transform 0.1s ease-in-out, box-shadow 0.1s ease-in-out;
        }
        [data-theme="dark"] .manifest-card { background-color: var(--bg-card); }
        [data-theme="hc-dark"] .manifest-card { background-color: var(--bg-card); }
        .manifest-card:active {
            transform: scale(0.98);
        }
        .manifest-card-left {
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .manifest-plane-icon {
            width: 56px;
            height: 56px;
            background-color: #e6f6eb;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--accent-green);
        }
        .manifest-plane-icon svg {
            width: 28px;
            height: 28px;
            fill: currentColor;
        }
        .manifest-card-body {
            flex: 1;
            padding: 20px 0;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .manifest-card-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-right: 20px;
        }
        .manifest-id {
            font-size: 18px;
            font-weight: 800;
            color: var(--text-main);
        }
        .manifest-status {
            background-color: #e6f6eb;
            color: var(--accent-green);
            font-size: 12px;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
            letter-spacing: 0.5px;
        }
        .manifest-status::before {
            content: '';
            display: block;
            width: 6px;
            height: 6px;
            background-color: var(--accent-green);
            border-radius: 50%;
        }
        .manifest-route-row {
            background-color: #f0f7ff;
            padding: 8px 12px;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-right: 20px;
        }
        [data-theme="dark"] .manifest-route-row { background-color: rgba(59,130,246,0.15); }
        [data-theme="hc-dark"] .manifest-route-row { background-color: rgba(59,130,246,0.15); }
        .manifest-route {
            color: var(--accent-blue);
            font-weight: 700;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .manifest-legs {
            background-color: var(--accent-blue);
            color: white;
            font-size: 12px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 12px;
        }
        .manifest-details-row {
            display: flex;
            gap: 16px;
            color: var(--text-muted);
            font-size: 13px;
            font-weight: 600;
            align-items: center;
        }
        .manifest-detail-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .manifest-card-right {
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #9ca3af;
        }
        .manifest-card-right svg {
            width: 24px;
            height: 24px;
        }
"""
    if '/* Manifest List Styles */' not in content:
        content = content.replace('</style>', css + '\n    </style>')

    # Step 2: Replace content-container with our new HTML
    new_html = """
                <div class="manifest-header">
                    <div class="manifest-title-group">
                        <div class="manifest-title">
                            <svg style="width:24px;height:24px;fill:currentColor" viewBox="0 0 24 24"><path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20M10,19L12,15H9V10H15V15H12L10,19Z"/></svg>
                            Manifests
                        </div>
                        <div class="manifest-badge">3</div>
                    </div>
                    <button class="btn-action blue" style="width: 160px; margin-bottom: 0;">
                        <svg viewBox="0 0 24 24"><path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/></svg> New Manifest
                    </button>
                </div>

                <!-- Card 1 -->
                <a href="flightlog.html" class="manifest-card">
                    <div class="manifest-card-left">
                        <div class="manifest-plane-icon">
                            <svg viewBox="0 0 24 24"><path d="M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z"/></svg>
                        </div>
                    </div>
                    <div class="manifest-card-body">
                        <div class="manifest-card-top">
                            <div class="manifest-id">#3664375</div>
                            <div class="manifest-status">OPEN</div>
                        </div>
                        <div class="manifest-route-row">
                            <div class="manifest-route">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M12,2L4.5,20.29L5.21,21L12,18L18.79,21L19.5,20.29L12,2Z"/></svg>
                                RWI &rarr; ?
                            </div>
                            <div class="manifest-legs">2 legs</div>
                        </div>
                        <div class="manifest-details-row">
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M19,4H18V2H16V4H8V2H6V4H5C3.89,4 3,4.9 3,6V20A2,2 0 0,0 5,22H19A2,2 0 0,0 21,20V6A2,2 0 0,0 19,4M19,20H5V10H19V20M19,8H5V6H19V8Z"/></svg>
                                06/18/2026
                            </div>
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z"/></svg>
                                14:54
                            </div>
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z"/></svg>
                                N850BU
                            </div>
                        </div>
                        <div class="manifest-details-row" style="margin-top:-4px;">
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/></svg>
                                Mauze, Charles
                            </div>
                        </div>
                    </div>
                    <div class="manifest-card-right">
                        <svg viewBox="0 0 24 24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" fill="currentColor"/></svg>
                    </div>
                </a>

                <!-- Card 2 -->
                <a href="flightlog.html" class="manifest-card">
                    <div class="manifest-card-left">
                        <div class="manifest-plane-icon">
                            <svg viewBox="0 0 24 24"><path d="M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z"/></svg>
                        </div>
                    </div>
                    <div class="manifest-card-body">
                        <div class="manifest-card-top">
                            <div class="manifest-id">#3664374</div>
                            <div class="manifest-status">OPEN</div>
                        </div>
                        <div class="manifest-route-row">
                            <div class="manifest-route">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M12,2L4.5,20.29L5.21,21L12,18L18.79,21L19.5,20.29L12,2Z"/></svg>
                                1NR1 &rarr; 1NR1
                            </div>
                            <div class="manifest-legs">2 legs</div>
                        </div>
                        <div class="manifest-details-row">
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M19,4H18V2H16V4H8V2H6V4H5C3.89,4 3,4.9 3,6V20A2,2 0 0,0 5,22H19A2,2 0 0,0 21,20V6A2,2 0 0,0 19,4M19,20H5V10H19V20M19,8H5V6H19V8Z"/></svg>
                                06/18/2026
                            </div>
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z"/></svg>
                                10:26
                            </div>
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z"/></svg>
                                N850BU
                            </div>
                        </div>
                        <div class="manifest-details-row" style="margin-top:-4px;">
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/></svg>
                                Mauze, Charles
                            </div>
                        </div>
                    </div>
                    <div class="manifest-card-right">
                        <svg viewBox="0 0 24 24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" fill="currentColor"/></svg>
                    </div>
                </a>

                <!-- Card 3 -->
                <a href="flightlog.html" class="manifest-card">
                    <div class="manifest-card-left">
                        <div class="manifest-plane-icon">
                            <svg viewBox="0 0 24 24"><path d="M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z"/></svg>
                        </div>
                    </div>
                    <div class="manifest-card-body">
                        <div class="manifest-card-top">
                            <div class="manifest-id">#3664365</div>
                            <div class="manifest-status">OPEN</div>
                        </div>
                        <div class="manifest-route-row">
                            <div class="manifest-route">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M12,2L4.5,20.29L5.21,21L12,18L18.79,21L19.5,20.29L12,2Z"/></svg>
                                RWI &rarr; ?
                            </div>
                            <div class="manifest-legs">2 legs</div>
                        </div>
                        <div class="manifest-details-row">
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M19,4H18V2H16V4H8V2H6V4H5C3.89,4 3,4.9 3,6V20A2,2 0 0,0 5,22H19A2,2 0 0,0 21,20V6A2,2 0 0,0 19,4M19,20H5V10H19V20M19,8H5V6H19V8Z"/></svg>
                                06/16/2026
                            </div>
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z"/></svg>
                                19:11
                            </div>
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z"/></svg>
                                N850BU
                            </div>
                        </div>
                        <div class="manifest-details-row" style="margin-top:-4px;">
                            <div class="manifest-detail-item">
                                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24"><path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/></svg>
                                Mauze, Charles
                            </div>
                        </div>
                    </div>
                    <div class="manifest-card-right">
                        <svg viewBox="0 0 24 24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" fill="currentColor"/></svg>
                    </div>
                </a>
"""

    start_idx = content.find('<div class="content-container">')
    end_idx = content.find('</div> <!-- End Content Container -->')
    
    if start_idx != -1 and end_idx != -1:
        content = content[:start_idx + len('<div class="content-container">')] + "\\n" + new_html + "\\n            " + content[end_idx:]

    # Change active tab in bottom nav
    # The active tab should be Manifest!
    content = content.replace('<div class="nav-item active" onclick="window.location.href=\\\'home.html\\\'"', '<div class="nav-item " onclick="window.location.href=\\\'home.html\\\'"')
    content = content.replace('<div class="nav-item " onclick="window.location.href=\\\'manifest.html\\\'"', '<div class="nav-item active" onclick="window.location.href=\\\'manifest.html\\\'"')

    with open('manifest.html', 'w') as f:
        f.write(content)

if __name__ == '__main__':
    main()
