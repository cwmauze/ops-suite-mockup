// Ops Suite - Fake Flight Request Simulator
// Global object to manage simulator state and actions
window.FlightSimulator = {
    waypointsData: {}, // Map of designation -> {lat, lon, name, category}
    activeRoute: [], // Array of waypoint objects

    init: async function() {
        try {
            this.loadActiveRoute();
            this.injectUI();
            await this.loadWaypoints();
            this.bindEvents();
            this.dispatchUpdate();
        } catch (e) {
            console.error("FlightSimulator initialization failed:", e);
        }
    },
    loadScript: function(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    },

    loadWaypoints: async function() {
        try {
            await this.loadScript('database/airports_data.js');
            if (window.FAA_AIRPORTS) {
                this.parseFAA(window.FAA_AIRPORTS);
            }
        } catch (err) {
            console.error("Simulator could not load FAA data script:", err);
        }

        try {
            await this.loadScript('database/hospitals_data.js');
            if (window.ECU_HOSPITALS) {
                this.parseCSV(window.ECU_HOSPITALS);
            }
        } catch (err) {
            console.error("Simulator could not load CSV data script:", err);
        }
    },

    parseFAA: function(data) {
        data.forEach(item => {
            if (item.id && item.lat !== undefined && item.lon !== undefined) {
                let wp = {
                    id: item.id.toUpperCase(),
                    name: item.name || 'Airport',
                    category: 'FAA Airport',
                    lat: parseFloat(item.lat),
                    lon: parseFloat(item.lon)
                };
                
                this.waypointsData[item.id.toUpperCase()] = wp;
                
                // Add ICAO K-prefix alias for 3-letter contiguous US airports
                if (item.id.length === 3 && /^[A-Z]{3}$/i.test(item.id)) {
                    this.waypointsData['K' + item.id.toUpperCase()] = {
                        ...wp,
                        id: 'K' + item.id.toUpperCase()
                    };
                }
            }
        });
    },

    parseCSV: function(csvText) {
        const lines = csvText.split('\n');
        // Skip header
        for (let i = 1; i < lines.length; i++) {
            let line = lines[i].trim();
            if (!line) continue;
            
            // Basic CSV parsing handling quotes
            const row = this.splitCSVLine(line);
            if (row.length >= 8) {
                let designation = row[0] || row[2];
                let title = row[1];
                let category = row[3];
                // lat_DD is index 6, lon_DD is index 7
                let lat = parseFloat(row[6].replace(/'/g, ''));
                let lon = parseFloat(row[7].replace(/'/g, ''));
                
                if (designation && !isNaN(lat) && !isNaN(lon)) {
                    this.waypointsData[designation.toUpperCase()] = {
                        id: designation.toUpperCase(),
                        name: title,
                        category: category,
                        lat: lat,
                        lon: lon
                    };
                }
            }
        }
    },

    splitCSVLine: function(text) {
        let ret = [];
        let cur = '';
        let inQuote = false;
        for (let i = 0; i < text.length; i++) {
            let c = text[i];
            if (c === '"') {
                inQuote = !inQuote;
            } else if (c === ',' && !inQuote) {
                ret.push(cur);
                cur = '';
            } else {
                cur += c;
            }
        }
        ret.push(cur);
        return ret;
    },

    loadActiveRoute: function() {
        try {
            const stored = localStorage.getItem('ops_suite_sim_route');
            if (stored) {
                this.activeRoute = JSON.parse(stored);
            } else {
                this.activeRoute = [];
            }
        } catch (e) {
            this.activeRoute = [];
        }
        
        // Ensure ETAs and distance are recalculated consistently with current code logic
        if (this.activeRoute.length > 0) {
            this.recalculateRouteMath();
        }
    },

    saveActiveRoute: function() {
        try {
            localStorage.setItem('ops_suite_sim_route', JSON.stringify(this.activeRoute));
        } catch (e) {
            console.warn("Could not save to localStorage. Security context may prevent this.");
        }
        this.dispatchUpdate();
    },

    clearRoute: function() {
        this.activeRoute = [];
        this.saveActiveRoute();
    },

    recalculateRouteMath: function() {
        let totalDistance = 0;
        let cumulativeTime = 0; // minutes
        
        for (let i = 0; i < this.activeRoute.length; i++) {
            let wp = this.activeRoute[i];
            if (i === 0) {
                wp.legDistance = 0;
                wp.heading = 0;
                wp.legTime = 0;
                wp.etaOffset = 0; // relative to start
            } else {
                let prev = this.activeRoute[i-1];
                let dist = this.calcDistance(prev.lat, prev.lon, wp.lat, wp.lon);
                let hdg = this.calcHeading(prev.lat, prev.lon, wp.lat, wp.lon);
                
                wp.legDistance = dist;
                wp.heading = hdg;
                // Assuming ~120 knots speed -> 2 nm per minute
                let time = Math.round(dist / 2);
                
                // Add ground delay at previous if it's not the first leg
                if (i > 1) {
                    let prevDelay = prev.delay !== undefined ? parseInt(prev.delay, 10) : 30;
                    if (isNaN(prevDelay)) prevDelay = 0;
                    cumulativeTime += prevDelay; 
                    wp.groundTimePrev = prevDelay;
                } else {
                    wp.groundTimePrev = 0;
                }
                
                cumulativeTime += time;
                wp.legTime = time;
                wp.etaOffset = cumulativeTime;
                totalDistance += dist;
            }
        }
        
        this.saveActiveRoute();
        this.renderRouteList();
    },

    addWaypointToRoute: function(token) {
        token = token.toUpperCase();
        if (this.waypointsData[token]) {
            this.activeRoute.push({...this.waypointsData[token]});
        } else {
            let coords = this.parseCoordinates(token);
            if (coords) {
                // Decimal coordinate format compatible with ForeFlight route strings
                let coordId = `${coords.lat.toFixed(5)},${coords.lon.toFixed(5)}`;
                this.activeRoute.push({
                    id: coordId,
                    name: 'SCENE',
                    lat: coords.lat,
                    lon: coords.lon
                });
            } else {
                // Unknown waypoint fallback
                this.activeRoute.push({
                    id: token,
                    name: 'Unknown Waypoint',
                    lat: 35.8563 + (Math.random() * 0.1 - 0.05),
                    lon: -77.8918 + (Math.random() * 0.1 - 0.05)
                });
            }
        }
        this.recalculateRouteMath();
    },

    parseCoordinates: function(input) {
        let str = input.trim().toUpperCase();
        
        // Replace commas and slashes with spaces to normalize
        let clean = str.replace(/[,/]/g, ' ').replace(/\s+/g, ' ').trim();
        
        // 1. Try pure decimal: "35.8563 -77.8918"
        const decimalRegex = /^(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)$/;
        let m = clean.match(decimalRegex);
        if (m) {
            let lat = parseFloat(m[1]);
            let lon = parseFloat(m[2]);
            if (lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180) {
                return {lat, lon};
            }
        }

        // 2. Try format with N/S and E/W identifiers
        const nsRegex = /^([\d\.\s]+[NS])\s*([\d\.\s]+[EW])$/;
        m = clean.match(nsRegex);
        if (m) {
            let latStr = m[1];
            let lonStr = m[2];
            let lat = this.parseCoordPart(latStr, true);
            let lon = this.parseCoordPart(lonStr, false);
            if (lat !== null && lon !== null && lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180) {
                return {lat, lon};
            }
        }
        
        return null;
    },

    parseCoordPart: function(part, isLat) {
        let dir = part.slice(-1);
        let numStr = part.slice(0, -1).trim();
        let sign = (dir === 'S' || dir === 'W') ? -1 : 1;
        
        let parts = numStr.split(' ').filter(p => p.length > 0);
        if (parts.length === 1) {
            let n = parts[0];
            if (n.includes('.')) {
                let val = parseFloat(n);
                if ((isLat && val > 90) || (!isLat && val > 180)) {
                    // Treat as DDMM.MM or DDDMM.MM
                    let idx = n.indexOf('.');
                    let mmStr = n.substring(idx - 2);
                    let ddStr = n.substring(0, idx - 2);
                    if (!ddStr) ddStr = '0';
                    return sign * (parseInt(ddStr, 10) + parseFloat(mmStr)/60.0);
                } else {
                    return sign * val;
                }
            }
        } else if (parts.length === 2) {
            // DD MM.MM
            return sign * (parseInt(parts[0], 10) + parseFloat(parts[1])/60.0);
        }
        return null;
    },

    removeWaypointFromRoute: function(index) {
        if (index >= 0 && index < this.activeRoute.length) {
            this.activeRoute.splice(index, 1);
            this.recalculateRouteMath();
        }
    },

    dispatchUpdate: function() {
        const event = new CustomEvent('flightRequestUpdated', {
            detail: { route: this.activeRoute }
        });
        document.dispatchEvent(event);
    },

    injectUI: function() {
        // Inject styles
        const style = document.createElement('style');
        style.textContent = `
            #flight-request-simulator {
                display: flex !important;
                width: 450px;
                flex-shrink: 0;
                min-width: 450px;
                max-width: 450px;
                background-color: #222;
                color: #ddd;
                padding: 40px 30px;
                box-sizing: border-box;
                flex-direction: column;
                gap: 15px;
                border-left: 1px solid #444;
                overflow-y: auto;
                z-index: 999999;
            }
            @media (max-width: 1100px) {
                #flight-request-simulator {
                    display: none !important;
                }
                #flight-request-simulator.mobile-visible {
                    display: flex !important;
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 9999999;
                    background-color: rgba(34,34,34, 0.95);
                    padding-top: calc(env(safe-area-inset-top) + 20px);
                    padding-bottom: calc(env(safe-area-inset-bottom) + 80px);
                }
                #flight-request-simulator .sim-mobile-close {
                    display: block !important;
                }
            }
            body.native-mode #flight-request-simulator {
                display: none !important;
            }
            body.native-mode #flight-request-simulator.mobile-visible {
                display: flex !important;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 9999999;
                background-color: rgba(34,34,34, 0.95);
                padding-top: calc(env(safe-area-inset-top) + 20px);
                padding-bottom: calc(env(safe-area-inset-bottom) + 80px);
            }
            body.native-mode #flight-request-simulator .sim-mobile-close {
                display: block !important;
            }
            #flight-request-simulator .sim-mobile-close {
                display: none;
            }
            #flight-request-simulator h2 { color: #fff; font-size: 1.5rem; margin-bottom: 5px; margin-top: 0; }
            #flight-request-simulator label { font-size: 0.9rem; font-weight: bold; color: #aaa; margin-bottom: 4px; display: block; }
            #flight-request-simulator input[type="text"] {
                width: 100%;
                padding: 10px;
                background: #111;
                border: 1px solid #444;
                color: white;
                border-radius: 6px;
                font-size: 1rem;
                margin-bottom: 10px;
            }
            #flight-request-simulator .btn-sim {
                background: #1b68e3;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 1rem;
                cursor: pointer;
                text-align: center;
                transition: opacity 0.2s;
                margin-bottom: 10px;
            }
            #flight-request-simulator .btn-sim:active { opacity: 0.8; }
            #flight-request-simulator .btn-clear {
                background: transparent;
                border: 1px solid #ea4335;
                color: #ea4335;
            }
            #flight-request-simulator .sim-note {
                font-size: 0.85rem;
                color: #888;
                line-height: 1.4;
            }
            .autocomplete-list {
                background: #111;
                border: 1px solid #444;
                border-radius: 6px;
                max-height: 150px;
                overflow-y: auto;
                margin-top: -10px;
                margin-bottom: 10px;
            }
            #flight-request-simulator .autocomplete-item {
                padding: 8px 10px;
                border-bottom: 1px solid #333;
                cursor: pointer;
                font-size: 0.9rem;
                color: #fff !important;
            }
            #flight-request-simulator .autocomplete-item:hover { background: #333; }
            .sim-route-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: #111;
                border: 1px solid #444;
                padding: 8px 12px;
                border-radius: 6px;
                margin-bottom: 5px;
            }
            .sim-route-row .id { font-weight: bold; color: #1b68e3; width: 50px; }
            .sim-route-row .name { font-size: 0.85rem; color: #888; flex: 1; margin-left: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .sim-route-row .remove-btn { cursor: pointer; color: #ea4335; font-weight: bold; padding: 0 5px; }
        `;
        document.head.appendChild(style);

        // Inject HTML
        const simDiv = document.createElement('div');
        simDiv.id = 'flight-request-simulator';
        simDiv.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                <h2>Comm Center Simulator</h2>
                <button onclick="window.FlightSimulator.toggleMobile()" class="sim-mobile-close" style="background: none; border: none; color: white; font-size: 2rem; cursor: pointer;">&times;</button>
            </div>
            <p class="sim-note">Add or remove waypoints to dynamically update the active flight request.</p>
            
            <div id="sim-route-list" style="margin-bottom: 15px;">
                <!-- Rows will be injected here -->
            </div>
            
            <div>
                <label>Add Waypoint</label>
                <input type="text" id="sim-waypoints-input" placeholder="Search identifier..." autocomplete="off">
                <div id="sim-autocomplete" class="autocomplete-list" style="display:none;"></div>
            </div>
            
            <button id="sim-btn-send" class="btn-sim" style="background:#34a853;">Create Flight Request</button>
            <button id="sim-btn-clear" class="btn-sim btn-clear">Clear Active Request</button>
            
            <div class="sim-note" style="margin-top: 20px;">
                <strong>Sample Identifiers:</strong><br>
                03NR - Johnston Health<br>
                NC91 - ECU Health Medical Center<br>
                35.85,-77.89 or 3551.38N/07753.51W - SCENE
            </div>
        `;
        document.body.appendChild(simDiv);
        this.renderRouteList();
    },

    renderRouteList: function() {
        const listDiv = document.getElementById('sim-route-list');
        if (!listDiv) return;
        
        if (this.activeRoute.length === 0) {
            listDiv.innerHTML = '<div class="sim-note" style="text-align:center; padding: 10px; background: #111; border-radius: 6px; border: 1px dashed #444;">No active waypoints</div>';
            return;
        }
        
        listDiv.innerHTML = this.activeRoute.map((wp, i) => {
            let info = '';
            if (i > 0) {
                info = `<div style="font-size:0.75rem; color:#888; margin-top: 4px;">${wp.heading}&deg; | ${wp.legDistance} nm | ${wp.legTime} min</div>`;
                if (i < this.activeRoute.length - 1) {
                    let d = wp.delay !== undefined ? wp.delay : 30;
                    info += `<div style="font-size:0.75rem; margin-top: 4px; display:flex; align-items:center; gap:5px;">Ground Time (min): <input type="number" class="sim-delay-input" data-index="${i}" value="${d}" min="0" style="width: 45px; background: #222; border: 1px solid #444; color: white; border-radius: 4px; padding: 2px 4px; font-size: 0.75rem;"></div>`;
                }
            } else {
                info = `<div style="font-size:0.75rem; color:#888; margin-top: 4px;">Origin</div>`;
            }
            let displayId = wp.name === 'SCENE' ? 'SCENE' : wp.id;
            let displayName = wp.name === 'SCENE' ? wp.id : (wp.name || 'Unknown');
            return `
            <div class="sim-route-row" draggable="true" data-index="${i}" style="cursor: grab;">
                <div style="pointer-events: none; flex: 1; overflow: hidden;">
                    <div style="display:flex; align-items:baseline; gap:10px;">
                        <span class="id">${displayId}</span>
                        <span class="name" title="${displayName}">${displayName}</span>
                    </div>
                    ${info}
                </div>
                <div class="remove-btn" data-index="${i}">✕</div>
            </div>
            `;
        }).join('');
    },

    toggleMobile: function() {
        const simDiv = document.getElementById('flight-request-simulator');
        if (simDiv) {
            simDiv.classList.toggle('mobile-visible');
        }
    },

    bindEvents: function() {
        const input = document.getElementById('sim-waypoints-input');
        const clearBtn = document.getElementById('sim-btn-clear');
        const autocomplete = document.getElementById('sim-autocomplete');
        const listDiv = document.getElementById('sim-route-list');

        listDiv.addEventListener('change', (e) => {
            if (e.target.classList.contains('sim-delay-input')) {
                const idx = parseInt(e.target.getAttribute('data-index'), 10);
                const val = parseInt(e.target.value, 10);
                if (!isNaN(val) && this.activeRoute[idx]) {
                    this.activeRoute[idx].delay = val;
                    this.recalculateRouteMath();
                }
            }
        });

        listDiv.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-btn')) {
                const index = parseInt(e.target.getAttribute('data-index'), 10);
                this.removeWaypointFromRoute(index);
            }
        });

        // Drag and Drop Logic
        let dragStartIndex = null;

        listDiv.addEventListener('dragstart', (e) => {
            const row = e.target.closest('.sim-route-row');
            if (row) {
                dragStartIndex = parseInt(row.getAttribute('data-index'), 10);
                e.dataTransfer.setData('text/plain', dragStartIndex);
                row.style.opacity = '0.5';
                e.dataTransfer.effectAllowed = 'move';
            }
        });

        listDiv.addEventListener('dragover', (e) => {
            e.preventDefault(); // Necessary to allow dropping
            const row = e.target.closest('.sim-route-row');
            if (row) {
                row.style.borderColor = '#1b68e3';
            }
        });

        listDiv.addEventListener('dragleave', (e) => {
            const row = e.target.closest('.sim-route-row');
            if (row) {
                row.style.borderColor = '#444';
            }
        });

        listDiv.addEventListener('drop', (e) => {
            e.preventDefault();
            const row = e.target.closest('.sim-route-row');
            if (row && dragStartIndex !== null) {
                const dragEndIndex = parseInt(row.getAttribute('data-index'), 10);
                if (dragStartIndex !== dragEndIndex) {
                    const item = this.activeRoute.splice(dragStartIndex, 1)[0];
                    this.activeRoute.splice(dragEndIndex, 0, item);
                    this.saveActiveRoute();
                    this.dispatchUpdate();
                }
            }
            this.renderRouteList();
        });

        listDiv.addEventListener('dragend', () => {
            this.renderRouteList();
        });

        const sendBtn = document.getElementById('sim-btn-send');
        if (sendBtn) {
            sendBtn.addEventListener('click', () => {
                localStorage.setItem('ops_suite_flight_sent', 'true');
                localStorage.setItem('ops_suite_flight_time', new Date().toISOString());
                this.dispatchUpdate();
            });
        }

        clearBtn.addEventListener('click', () => {
            localStorage.setItem('ops_suite_flight_sent', 'false');
            localStorage.removeItem('ops_suite_flight_time');
            this.clearRoute();
            this.renderRouteList();
            this.dispatchUpdate();
        });
        
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const val = input.value.trim();
                if (val.length > 0) {
                    this.addWaypointToRoute(val);
                    input.value = '';
                    autocomplete.style.display = 'none';
                }
            }
        });
        
        // Basic Autocomplete
        input.addEventListener('input', (e) => {
            const val = e.target.value.trim().toUpperCase();
            
            if (val.length >= 2) {
                const matches = Object.values(this.waypointsData)
                    .filter(w => w.id.includes(val) || (w.name && w.name.toUpperCase().includes(val)))
                    .slice(0, 5);
                    
                if (matches.length > 0) {
                    autocomplete.innerHTML = matches.map(m => 
                        `<div class="autocomplete-item" data-id="${m.id}"><strong>${m.id}</strong> - ${m.name}</div>`
                    ).join('');
                    autocomplete.style.display = 'block';
                } else {
                    autocomplete.style.display = 'none';
                }
            } else {
                autocomplete.style.display = 'none';
            }
        });

        autocomplete.addEventListener('click', (e) => {
            const item = e.target.closest('.autocomplete-item');
            if (item) {
                const id = item.getAttribute('data-id');
                this.addWaypointToRoute(id);
                input.value = '';
                autocomplete.style.display = 'none';
                input.focus();
            }
        });
        
        document.addEventListener('click', (e) => {
            if (!autocomplete.contains(e.target) && e.target !== input) {
                autocomplete.style.display = 'none';
            }
        });
    },

    // --- Math Helpers ---
    calcDistance: function(lat1, lon1, lat2, lon2) {
        // Haversine formula for nautical miles
        const R = 3440.065; // Earth radius in nm
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = 
            Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
            Math.sin(dLon/2) * Math.sin(dLon/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return Math.round((R * c) * 10) / 10;
    },

    calcHeading: function(lat1, lon1, lat2, lon2) {
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const y = Math.sin(dLon) * Math.cos(lat2 * Math.PI / 180);
        const x = Math.cos(lat1 * Math.PI / 180) * Math.sin(lat2 * Math.PI / 180) -
                Math.sin(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.cos(dLon);
        let brng = Math.atan2(y, x) * 180 / Math.PI;
        return Math.round((brng + 360) % 360);
    }
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (window.FlightSimulator) window.FlightSimulator.init();
    });
} else {
    if (window.FlightSimulator) window.FlightSimulator.init();
}
