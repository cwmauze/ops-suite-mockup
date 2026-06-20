<script>



        const dutyInRisksData = [
            { id: "dir-1", text: "I do \"NOT\" feel Rested and Fit for Duty.", pts: 4 },
            { id: "dir-2", text: "It has \"NOT\" been at least 10 hours since I last consumed alcohol.", pts: 4 },
            { id: "dir-3", text: "I am experiencing the residual effects of alcohol consumption or medication.", pts: 4 },
            { id: "dir-4", text: "Fever of 100.4 F (38 C) or higher", pts: 4 },
            { id: "dir-5", text: "Feel Feverish or have Chills", pts: 2 },
            { id: "dir-6", text: "Cough (Dry or Unproductive)", pts: 2 },
            { id: "dir-7", text: "Shortness of Breath or Difficulty Breathing", pts: 2 },
            { id: "dir-8", text: "Sore Throat", pts: 1 },
            { id: "dir-9", text: "Runny Nose (Nasal Congestion)", pts: 1 },
            { id: "dir-10", text: "Body Fatigue (Tiredness)", pts: 1 },
            { id: "dir-11", text: "Body Aches and Pains", pts: 1 },
            { id: "dir-12", text: "Headache", pts: 1 },
            { id: "dir-13", text: 'Nausea or Vomiting "Within the last 24 hours"', pts: 1 },
            { id: "dir-14", text: 'Diarrhea "Within the last 24 hours"', pts: 1 }
        ];

        function openDutyInRiskModal() {
            const modal = document.getElementById('duty-in-risk-modal');
            const list = document.getElementById('duty-in-risk-list');
            
            // Generate list if empty
            if (list.innerHTML.trim() === '') {
                dutyInRisksData.forEach((risk, index) => {
                    const isLast = index === dutyInRisksData.length - 1;
                    const borderStyle = isLast ? '' : 'border-bottom: 1px solid var(--border-color);';
                    list.innerHTML += `
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 16px 0; ${borderStyle}">
                            <div style="font-size: 14px; color: var(--text-main); flex: 1; padding-right: 16px; line-height: 1.4;">${risk.text}</div>
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <span style="font-size: 14px; color: var(--text-muted);">${risk.pts} pts</span>
                                <input type="checkbox" id="${risk.id}" style="width: 20px; height: 20px; border: 1px solid var(--border-color); border-radius: 4px;">
                            </div>
                        </div>
                    `;
                });
            }

            // Load saved state
            const savedState = JSON.parse(localStorage.getItem('ops_suite_duty_in_risks')) || {};
            dutyInRisksData.forEach(risk => {
                const cb = document.getElementById(risk.id);
                if (cb) cb.checked = !!savedState[risk.id];
            });
            document.getElementById('duty-in-pilot-comments').value = savedState.comments || '';
            document.getElementById('duty-in-sign-toggle').checked = !!savedState.signed;

            modal.style.display = 'flex';
        }

        function closeDutyInRiskModal() {
            document.getElementById('duty-in-risk-modal').style.display = 'none';
        }

        function saveDutyInRiskModal() {
            const state = { comments: document.getElementById('duty-in-pilot-comments').value, signed: document.getElementById('duty-in-sign-toggle').checked };
            dutyInRisksData.forEach(risk => {
                const cb = document.getElementById(risk.id);
                if (cb) state[risk.id] = cb.checked;
            });
            localStorage.setItem('ops_suite_duty_in_risks', JSON.stringify(state));
            closeDutyInRiskModal();
        }


        // Map Implementation
        let leafletMap = null;

        async function initMap() {
            leafletMap = L.map('leaflet-map', { 
                zoomControl: false, 
                attributionControl: false 
            });
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(leafletMap);

            updateFlightRequestView();
        }

        function updateFlightRequestView() {
            if (window.FlightSimulator && window.FlightSimulator.activeRoute) {
                const route = window.FlightSimulator.activeRoute;
                
                // Update Route List
                const routeList = document.getElementById('flight-request-route-list');
                if (routeList) {
                    if (route.length === 0) {
                        routeList.innerHTML = '<div style="padding: 10px; color: var(--text-muted); text-align: center;">No active route.</div>';
                    } else {
                        routeList.innerHTML = route.map((wp, index) => {
                            let statsHtml = '';
                            if (index > 0) {
                                statsHtml = `<span>${wp.legDistance} nm</span> <span>${wp.heading}&deg;</span>`;
                            }
                            
                            // Mock ETA just for display
                            const etaOffset = wp.etaOffset || 0;
                            const d = new Date();
                            d.setMinutes(d.getMinutes() + etaOffset);
                            const etaStr = d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                            
                            return `
                            <div class="route-row">
                                <div class="waypoint-info">
                                    <span class="waypoint-id">${wp.id}</span>
                                    <span class="waypoint-stats">${statsHtml}</span>
                                </div>
                                <span class="waypoint-eta">ETA: ${etaStr}</span>
                            </div>`;
                        }).join('');
                    }
                }

                // Update Map
                if (leafletMap && route.length > 0) {
                    // Clear previous layers
                    leafletMap.eachLayer((layer) => {
                        if (layer instanceof L.Marker || layer instanceof L.Polyline) {
                            leafletMap.removeLayer(layer);
                        }
                    });

                    const waypoints = [];
                    route.forEach((wp, index) => {
                        const latLng = [wp.lat, wp.lon];
                        waypoints.push(latLng);

                        let colorClass = 'var(--accent-green)';
                        if (index === 1) colorClass = 'var(--accent-orange)';
                        if (index === 2) colorClass = 'var(--accent-red)';

                        const markerHtml = `<div style="background-color: ${colorClass}; color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">${index + 1}</div>`;
                        const customIcon = L.divIcon({
                            html: markerHtml,
                            className: 'custom-div-icon',
                            iconSize: [24, 24],
                            iconAnchor: [12, 12]
                        });

                        L.marker(latLng, {icon: customIcon}).addTo(leafletMap);
                    });

                    const routeLine = L.polyline(waypoints, {
                        color: '#FF00FF',
                        weight: 3,
                        opacity: 0.8,
                        dashArray: null
                    }).addTo(leafletMap);

                    leafletMap.fitBounds(routeLine.getBounds(), {padding: [30, 30]});
                }
                
                const dateSpan = document.getElementById('req-date-text');
                const storedTime = localStorage.getItem('ops_suite_flight_time');
                if (dateSpan && storedTime) {
                    const d = new Date(storedTime);
                    const mm = String(d.getMonth() + 1).padStart(2, '0');
                    const dd = String(d.getDate()).padStart(2, '0');
                    const yyyy = d.getFullYear();
                    const hh = String(d.getHours()).padStart(2, '0');
                    const min = String(d.getMinutes()).padStart(2, '0');
                    dateSpan.innerHTML = `${mm}/${dd}/${yyyy}, ${hh}:${min}`;
                }
            }
        }

        document.addEventListener('flightRequestUpdated', () => {
            updateFlightRequestView();
        });

        function openInForeFlight() {
            if (window.FlightSimulator && window.FlightSimulator.activeRoute) {
                const route = window.FlightSimulator.activeRoute;
                if (route.length > 0) {
                    const waypointIds = route.map(wp => wp.id).join('+');
                    const url = `foreflightmobile://maps/search?q=${waypointIds}`;
                    window.location.href = url;
                } else {
                    alert('No active route to open in ForeFlight.');
                }
            }
        }

        // Initialize everything
        window.onload = () => {
            initMap();
        };

        const themes = ['light', 'neutral', 'mid', 'dark', 'hc-dark', 'hc-light'];
        function toggleTheme() {
            const html = document.documentElement;
            let current = html.getAttribute('data-theme') || 'mid';
            let nextIndex = (themes.indexOf(current) + 1) % themes.length;
            let nextTheme = themes[nextIndex];
            html.setAttribute('data-theme', nextTheme);
            localStorage.setItem('ops_suite_theme', nextTheme);
        }

        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('ops_suite_theme');
            if (savedTheme) {
                document.documentElement.setAttribute('data-theme', savedTheme);
            }
            
            const initialSyncText = document.querySelector('.sync-text');
            if (initialSyncText) {
                initialSyncText.innerHTML = `Last sync: ${formatSyncTime()}`;
            }

            loadSystemIdentifiedRisks();
        });

        function loadSystemIdentifiedRisks() {
            const container = document.getElementById('system-identified-risks-container');
            const list = document.getElementById('system-identified-risks-list');
            if (!container || !list) return;

            const defaultRisks = [
                { text: '2- Consecutive night shifts > 4', pts: 2 },
                { text: '3- PIC < 1 YR or 100 flights at program', pts: 2 },
                { text: '6- Last flight > 30 days', pts: 2 },
                { text: '7- Last Night and/or HNVGO flight > 30 days (Only applicable when conducting Night Flight)', pts: 4 }
            ];

            try {
                let savedRisks = JSON.parse(localStorage.getItem('ops_suite_active_risks'));
                
                // If localStorage is empty or null, use defaults
                if (!savedRisks || savedRisks.length === 0) {
                    savedRisks = defaultRisks;
                    localStorage.setItem('ops_suite_active_risks', JSON.stringify(defaultRisks));
                }

                if (savedRisks.length > 0) {
                    list.innerHTML = '';
                    let totalPts = 0;
                    savedRisks.forEach(risk => {
                        totalPts += risk.pts;
                        list.innerHTML += `
                            <div style="background-color: rgba(249, 171, 0, 0.1); border-left: 4px solid var(--accent-orange); padding: 12px; border-radius: 0 8px 8px 0; display: flex; align-items: center; justify-content: space-between; border-top: 1px solid var(--border-color); border-right: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color);">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent-orange)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
                                    <span style="font-size: 14px; font-weight: 600; color: var(--text-main); line-height: 1.3;">${risk.text}</span>
                                </div>
                                <span style="font-size: 14px; font-weight: bold; color: var(--accent-orange); white-space: nowrap; margin-left: 8px;">${risk.pts} pts</span>
                            </div>
                        `;
                    });
                    container.style.display = 'flex';
                } else {
                    container.style.display = 'none';
                }
            } catch (e) {
                console.error("Error loading system risks", e);
            }
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

        const dutyInRisksData = [
            { id: "dir-1", text: "I do \"NOT\" feel Rested and Fit for Duty.", pts: 4 },
            { id: "dir-2", text: "It has \"NOT\" been at least 10 hours since I last consumed alcohol.", pts: 4 },
            { id: "dir-3", text: "I am experiencing the residual effects of alcohol consumption or medication.", pts: 4 },
            { id: "dir-4", text: "Fever of 100.4 F (38 C) or higher", pts: 4 },
            { id: "dir-5", text: "Feel Feverish or have Chills", pts: 2 },
            { id: "dir-6", text: "Cough (Dry or Unproductive)", pts: 2 },
            { id: "dir-7", text: "Shortness of Breath or Difficulty Breathing", pts: 2 },
            { id: "dir-8", text: "Sore Throat", pts: 1 },
            { id: "dir-9", text: "Runny Nose (Nasal Congestion)", pts: 1 },
            { id: "dir-10", text: "Body Fatigue (Tiredness)", pts: 1 },
            { id: "dir-11", text: "Body Aches and Pains", pts: 1 },
            { id: "dir-12", text: "Headache", pts: 1 },
            { id: "dir-13", text: 'Nausea or Vomiting "Within the last 24 hours"', pts: 1 },
            { id: "dir-14", text: 'Diarrhea "Within the last 24 hours"', pts: 1 }
        ];

        function openDutyInRiskModal() {
            const modal = document.getElementById('duty-in-risk-modal');
            const list = document.getElementById('duty-in-risk-list');
            
            if (list.innerHTML.trim() === '') {
                dutyInRisksData.forEach((risk, index) => {
                    const isLast = index === dutyInRisksData.length - 1;
                    const borderStyle = isLast ? '' : 'border-bottom: 1px solid var(--border-color);';
                    list.innerHTML += `
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 16px 0; ${borderStyle}">
                            <div style="font-size: 14px; color: var(--text-main); flex: 1; padding-right: 16px; line-height: 1.4;">${risk.text}</div>
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <span style="font-size: 14px; color: var(--text-muted);">${risk.pts} pts</span>
                                <input type="checkbox" id="${risk.id}" style="width: 20px; height: 20px; border: 1px solid var(--border-color); border-radius: 4px;">
                            </div>
                        </div>
                    `;
                });
            }

            const savedState = JSON.parse(localStorage.getItem('ops_suite_duty_in_risks')) || {};
            dutyInRisksData.forEach(risk => {
                const cb = document.getElementById(risk.id);
                if (cb) cb.checked = !!savedState[risk.id];
            });
            document.getElementById('duty-in-pilot-comments').value = savedState.comments || '';
            document.getElementById('duty-in-sign-toggle').checked = !!savedState.signed;

            modal.style.display = 'flex';
        }

        function closeDutyInRiskModal() {
            document.getElementById('duty-in-risk-modal').style.display = 'none';
        }

        function saveDutyInRiskModal() {
            const state = { comments: document.getElementById('duty-in-pilot-comments').value, signed: document.getElementById('duty-in-sign-toggle').checked };
            dutyInRisksData.forEach(risk => {
                const cb = document.getElementById(risk.id);
                if (cb) state[risk.id] = cb.checked;
            });
            localStorage.setItem('ops_suite_duty_in_risks', JSON.stringify(state));
            closeDutyInRiskModal();
        }
    </script>