
        function scaleDevice() {
            const frame = document.querySelector('.device-frame');
            const container = document.getElementById('main-view') || document.body;
            if(frame) {
                if (document.body.classList.contains('native-mode')) {
                    frame.style.transform = 'none';
                    return;
                }
                // Total width = 744 + 40 padding = 784. Total height = 1133 + 40 padding = 1173
                const scale = Math.min(1, (container.clientWidth * 0.95) / 784, (container.clientHeight * 0.95) / 1173);
                frame.style.transform = `scale(${scale})`;
            }
        }
        window.addEventListener('resize', scaleDevice);
        window.addEventListener('DOMContentLoaded', () => {
            // Detect mobile/tablet devices, including iPadOS 13+ desktop mode, or PWA standalone mode
            const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
            const isMobile = /iPad|iPhone|iPod|Android/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
            if (isStandalone || isMobile) {
                document.body.classList.add('native-mode');
            }
            scaleDevice();
        });

        function toggleChangelog() {
            const panel = document.getElementById('changelog-panel');
            if (panel.style.display === 'none' || panel.style.display === '') {
                panel.style.display = 'flex';
            }
    

        const AppState = {
            legs: [
                { id: 1, origin: 'RWI', dest: 'NC91', active: true },
                { id: 2, origin: 'NC91', dest: 'RWI', active: false }
            ]
        };

        const DummyPersonnel = [
            { name: "Empty", weight: 0 },
            { name: "Arnold Schwarzenegger", weight: 105 },
            { name: "Sylvester Stallone", weight: 85 },
            { name: "Chuck Norris", weight: 77 },
            { name: "Dwayne Johnson", weight: 118 },
            { name: "Jason Statham", weight: 84 },
            { name: "Bruce Willis", weight: 82 },
            { name: "Tom Cruise", weight: 68 },
            { name: "Keanu Reeves", weight: 79 },
            { name: "Jean-Claude Van Damme", weight: 82 },
            { name: "Harrison Ford", weight: 80 },
            { name: "Marilyn Monroe", weight: 54 },
            { name: "Scarlett Johansson", weight: 57 },
            { name: "Margot Robbie", weight: 57 },
            { name: "Charlize Theron", weight: 61 },
            { name: "Angelina Jolie", weight: 54 },
            { name: "Megan Fox", weight: 52 },
            { name: "Salma Hayek", weight: 54 },
            { name: "Sofia Vergara", weight: 64 },
            { name: "Raquel Welch", weight: 55 },
            { name: "Pamela Anderson", weight: 60 }
        ];

        // Simulated Keyboard Logic
        // Convert datetime-sim inputs to real datetime-local on touch devices
        const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
        
        if (isTouchDevice || document.body.classList.contains('native-mode')) {
            // Disabled: We now use our custom Time Picker popover instead of native datetime-local
            // to ensure 24-hour compliance and a faster scrolling experience without a calendar popup.
        }
        
        document.addEventListener('focusin', (e) => {
            if (isTouchDevice || document.body.classList.contains('native-mode')) return;
            
            const target = e.target;
            const kb = document.getElementById('simulated-keyboard');
            const numpad = document.getElementById('simulated-numpad');

            if ((target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') && 
                !target.readOnly && 
                target.type !== 'checkbox' && 
                target.type !== 'radio' &&
                target.type !== 'range') {
                
                const inputMode = target.getAttribute('inputmode');
                const isNumeric = target.type === 'number' || inputMode === 'decimal' || inputMode === 'numeric';
                
                if (isNumeric) {
                    kb.classList.remove('visible');
                    numpad.classList.add('visible');
                } else {
                    numpad.classList.remove('visible');
                    kb.classList.add('visible');
                }
                
                const mainContent = document.getElementById('main-content');
                if (mainContent) {
                    mainContent.style.paddingBottom = isNumeric ? '350px' : '410px';
                    setTimeout(() => {
                        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 300);
                }
            }
        });

        document.addEventListener('focusout', (e) => {
            if (isTouchDevice || document.body.classList.contains('native-mode')) return;
            
            setTimeout(() => {
                const active = document.activeElement;
                if (!active || (active.tagName !== 'INPUT' && active.tagName !== 'TEXTAREA') || active.readOnly) {
                    if (isTouchDevice) return;
                    const kb = document.getElementById('simulated-keyboard');
                    const numpad = document.getElementById('simulated-numpad');
                    kb.classList.remove('visible');
                    numpad.classList.remove('visible');
                    
                    const mainContent = document.getElementById('main-content');
                    if (mainContent) {
                        mainContent.style.paddingBottom = '20px';
                    }
                }
            }, 50);
        });

        // Make simulated keys functional
        document.addEventListener('click', (e) => {
            if (isTouchDevice) return;
            
            const key = e.target.closest('.kb-key');
            if (!key) return;
            
            const active = document.activeElement;
            if (!active || (active.tagName !== 'INPUT' && active.tagName !== 'TEXTAREA') || active.readOnly) return;
            
            if (key.classList.contains('dismiss-btn')) {
                active.blur();
                return;
            }
            
            // Handle Backspace
            if (key.innerText === '⌫') {
                if (active.type === 'number' || active.type === 'time' || active.type === 'datetime-local') {
                    active.value = active.value.slice(0, -1);
                } else if (active.selectionStart !== undefined) {
                    const start = active.selectionStart;
                    const end = active.selectionEnd;
                    if (start === end && start > 0) {
                        active.value = active.value.slice(0, start - 1) + active.value.slice(start);
                        active.setSelectionRange(start - 1, start - 1);
                    } else if (start !== end) {
                        active.value = active.value.slice(0, start) + active.value.slice(end);
                        active.setSelectionRange(start, start);
                    }
                } else {
                    active.value = active.value.slice(0, -1);
                }
                active.dispatchEvent(new Event('input', { bubbles: true }));
                return;
            }
            
            // Ignore other special keys (Shift, Return, .?123)
            if (key.classList.contains('special') && key.innerText !== '.') {
                if (key.innerText.includes('Return')) active.blur();
                return; 
            }
            
            // Handle regular keys
            let char = key.classList.contains('spacebar') ? ' ' : key.innerText;
            
            // Handle input
            if (active.type === 'number' || active.type === 'time' || active.type === 'datetime-local') {
                // If it's a number and they hit '.', and it already has one, ignore
                if (active.type === 'number' && char === '.' && active.value.includes('.')) return;
                
                // Read current as string to handle appending properly
                let curVal = active.value.toString();
                active.value = curVal + char;
            } else if (active.selectionStart !== undefined) {
                const start = active.selectionStart;
                const end = active.selectionEnd;
                active.value = active.value.slice(0, start) + char + active.value.slice(end);
                active.setSelectionRange(start + char.length, start + char.length);
            } else {
                active.value += char;
            }
            
            active.dispatchEvent(new Event('input', { bubbles: true }));
        });

        let fuelTimeOverridden = false;
        let sobOverridden = false;

        function handleOverride(field) {
            const input = document.getElementById(field);
            if (!input) return;
            
            if (field === 'fuel-time') {
                fuelTimeOverridden = (input.value.trim() !== '');
                if (!fuelTimeOverridden) calculateFuelTime();
            } else if (field === 'sob') {
                sobOverridden = (input.value.trim() !== '');
                if (!sobOverridden) calculateSob();
            }
        }

        function calculateSob() {
            if (sobOverridden) return;
            let count = 0;
            document.querySelectorAll('.seat-occupant-input').forEach(input => {
                if (input.value.trim() !== '' && input.value.trim().toLowerCase() !== 'empty') {
                    count++;
                }
            });
            const sobInput = document.getElementById('sob');
            if (sobInput) sobInput.value = count;
        }

        function calculateFuelTime() {
            if (fuelTimeOverridden) return;
            const supply = parseFloat(document.getElementById('supply-tank').value) || 0;
            const main = parseFloat(document.getElementById('main-tank').value) || 0;
            const burn = parseFloat(document.getElementById('burn-rate').value) || 0;
            
            if (burn > 0) {
                const totalGal = supply + main;
                const hoursDecimal = totalGal / burn;
                const hours = Math.floor(hoursDecimal);
                const minutes = Math.floor((hoursDecimal - hours) * 60);
                
                const padH = hours.toString().padStart(2, '0');
                const padM = minutes.toString().padStart(2, '0');
                document.getElementById('fuel-time').value = `${padH}:${padM}`;
            } else {
                document.getElementById('fuel-time').value = '--:--';
            }
        }
        
        // Initialize fields on load
        setTimeout(() => {
            calculateFuelTime();
            calculateSob();
        }, 100);

        function setNow(inputId) {
            const now = new Date();
            const year = now.getUTCFullYear();
            const month = String(now.getUTCMonth() + 1).padStart(2, '0');
            const day = String(now.getUTCDate()).padStart(2, '0');
            const hours = String(now.getUTCHours()).padStart(2, '0');
            const minutes = String(now.getUTCMinutes()).padStart(2, '0');
            
            const input = document.getElementById(inputId);
            if(input) {
                if (input.type === 'datetime-local') {
                    input.value = `${year}-${month}-${day}T${hours}:${minutes}`;
                } else {
                    input.value = `${year}-${month}-${day} ${hours}:${minutes}`;
                }
            }
        }

        function showPersonnel(seatId) {
            filterPersonnel(seatId);
        }

        let dispatchNumber = "";
        function promptDispatch() {
            const num = prompt("Enter Dispatch Number:", dispatchNumber);
            if (num !== null) {
                dispatchNumber = num.trim();
                const btn = document.getElementById('dispatch-btn');
                if (dispatchNumber === "") {
                    btn.className = "tile red";
                    btn.innerHTML = "Dispatch #";
                } else {
                    btn.className = "tile green";
                    btn.style.flexDirection = "column";
                    btn.innerHTML = `<span style="font-size:0.7rem; text-transform:uppercase;">Dispatch #</span><span style="font-size:1rem; font-weight:bold; margin-top:2px;">${dispatchNumber}</span>`;
                }
            }
        }

        function clearSeat(seatId, event) {
            if (event) {
                event.stopPropagation();
            }
            const input = document.getElementById(`occ-${seatId}`);
            const wt = document.getElementById(`wt-${seatId}`);
            if(input) input.value = '';
            if(wt) wt.value = '0';
            const dropdown = document.getElementById(`dropdown-${seatId}`);
            if(dropdown) dropdown.style.display = 'none';
        }

        function filterPersonnel(seatId) {
            calculateSob(); // Trigger SOB recount
            const input = document.getElementById(`occ-${seatId}`);
            const dropdown = document.getElementById(`dropdown-${seatId}`);
            if (!input || !dropdown) return;
            const query = input.value.toLowerCase();
            
            for(let i=1; i<=6; i++) {
                if(i !== seatId) {
                    const other = document.getElementById(`dropdown-${i}`);
                    if(other) other.style.display = 'none';
                }
            }
            
            dropdown.innerHTML = '';
            
            let matches = DummyPersonnel;
            if (query.trim() !== '') {
                matches = DummyPersonnel.filter(p => p.name.toLowerCase().includes(query));
            }

            if (matches.length > 0) {
                matches.forEach(p => {
                    const item = document.createElement('div');
                    item.className = 'autocomplete-item';
                    item.innerHTML = `<span>${p.name}</span><span style="color:var(--text-secondary);">${p.weight} KG</span>`;
                    item.onmousedown = (e) => {
                        e.preventDefault(); 
                        input.value = p.name;
                        const wt = document.getElementById(`wt-${seatId}`);
                        if (wt) wt.value = p.weight;
                        dropdown.style.display = 'none';
                        calculateSob(); // Trigger SOB recount
                    };
                    dropdown.appendChild(item);
                });
                dropdown.style.display = 'block';
            } else {
                dropdown.style.display = 'none';
            }
        }

        document.addEventListener('focusout', (e) => {
            if (e.target.classList.contains('seat-occupant-input')) {
                const seatId = parseInt(e.target.id.split('-')[1]);
                const dropdown = document.getElementById(`dropdown-${seatId}`);
                setTimeout(() => { if (dropdown) dropdown.style.display = 'none'; }, 150);
            }
        });

        const themes = ['light', 'neutral', 'dark', 'hc-dark', 'hc-light'];
        function toggleTheme() {
            const html = document.documentElement;
            let current = html.getAttribute('data-theme') || 'light';
            let nextIndex = (themes.indexOf(current) + 1) % themes.length;
            html.setAttribute('data-theme', themes[nextIndex]);
        }

        function renderTabs() {
            const tabsContainer = document.getElementById('leg-tabs-container');
            tabsContainer.innerHTML = '';
            AppState.legs.forEach(leg => {
                const btn = document.createElement('button');
                btn.className = `leg-tab ${leg.active ? 'active' : ''}`;
                btn.innerHTML = `
                    <span style="color:${leg.active ? 'var(--accent-green)' : 'var(--text-secondary)'}">●</span> 
                    Leg ${leg.id}: ${leg.origin} ➔ ${leg.dest}
                    <span class="close-btn" onclick="removeLeg(${leg.id}, event)">×</span>
                `;
                btn.onclick = () => activateLeg(leg.id);
                tabsContainer.appendChild(btn);
            });
            
            updateFormFromState();
        }

        function handleSaveAddLeg() {
            const verifiedToggle = document.getElementById('manifest-verified-toggle');
            if (!verifiedToggle || !verifiedToggle.checked) {
                alert("Warning: You must verify the manifest for the current leg before saving and adding a new leg.");
                return;
            }
            addLeg();
            if (verifiedToggle) {
                verifiedToggle.checked = false;
            }
        }

        function addLeg() {
            const newId = AppState.legs.length ? Math.max(...AppState.legs.map(l=>l.id)) + 1 : 1;
            const origin = AppState.legs.length ? AppState.legs[AppState.legs.length-1].dest : '???';
            AppState.legs.push({ id: newId, origin: origin, dest: '???', active: false });
            activateLeg(newId);
        }

        function removeLeg(id, event) {
            event.stopPropagation();
            AppState.legs = AppState.legs.filter(l => l.id !== id);
            if (AppState.legs.length > 0 && !AppState.legs.some(l => l.active)) {
                AppState.legs[0].active = true;
            }
            renderTabs();
        }

        function activateLeg(id) {
            AppState.legs.forEach(l => l.active = (l.id === id));
            renderTabs();
        }
        
        function updateFormFromState() {
            const activeLeg = AppState.legs.find(l => l.active);
            if(activeLeg) {
                // document.getElementById('current-leg-title').innerText = `Leg ${activeLeg.id}`;
                document.getElementById('leg-origin').value = activeLeg.origin;
                document.getElementById('leg-dest').value = activeLeg.dest;
            } else {
                // document.getElementById('current-leg-title').innerText = ``;
                document.getElementById('leg-origin').value = '';
                document.getElementById('leg-dest').value = '';
            }
        }
        
        function updateCurrentLeg() {
            const activeLeg = AppState.legs.find(l => l.active);
            if(activeLeg) {
                activeLeg.origin = document.getElementById('leg-origin').value;
                activeLeg.dest = document.getElementById('leg-dest').value;
                
                // re-render just the tabs to show updated text
                renderTabs();
            }
        }

        function openModal(id) {
            document.getElementById(id).classList.add('active');
        }

        function closeModal(id) {
            document.getElementById(id).classList.remove('active');
        }

        function validateAndClose() {
            const night = parseFloat(document.getElementById('val-night').value) || 0;
            const nvg = parseFloat(document.getElementById('val-nvg').value) || 0;
            const hnvgo = parseInt(document.getElementById('val-hnvgo').value) || 0;
            const inst = parseFloat(document.getElementById('val-inst').value) || 0;
            const hood = parseFloat(document.getElementById('val-hood').value) || 0;
            const app = parseInt(document.getElementById('val-app').value) || 0;
            const isIfr = document.getElementById('ifr-toggle') ? document.getElementById('ifr-toggle').checked : false;

            let error = "";

            if (nvg > night) {
                error = "NVG time cannot exceed Night time.";
            } else if (hnvgo > 0 && nvg <= 0) {
                error = "HNVGO logged but NVG time is 0.";
            } else if (nvg > 0 && night <= 0) {
                error = "NVG time logged but Night time is 0.";
            } else if (app > 0 && (inst + hood) <= 0) {
                error = "Approaches logged without Instrument/Hood time.";
            } else if (inst > 0 && !isIfr) {
                error = "Instrument time logged but IFR Flight is NOT toggled.";
            }

            const errorBanner = document.getElementById('close-error-banner');
            if (error) {
                errorBanner.innerText = error;
                errorBanner.style.display = "flex";
            } else {
                errorBanner.style.display = "none";
                alert("Flight leg closed successfully!");
                closeModal('close-modal');
            }
        }

        // Initialize
        renderTabs();

        // --- SYNC INTERACTION ---
        function triggerManualSync(el) {
            if (el.classList.contains('syncing')) return;
            el.classList.add('syncing');
            
            const icon = el.querySelector('.sync-icon');
            const text = el.querySelector('.sync-text');
            
            // Change icon to a spinner
            icon.innerHTML = '↻';
            icon.style.animation = 'spin 1s linear infinite';
            icon.style.color = 'var(--accent-blue)';
            text.innerHTML = 'Syncing...';
            
            setTimeout(() => {
                icon.style.animation = 'none';
                icon.innerHTML = '✔';
                icon.style.color = 'var(--accent-green)';
                text.innerHTML = 'Last sync: Just now';
                el.classList.remove('syncing');
            }, 10000);
        }
    

        let currentRiskScore = 0;
        let isRiskSigned = false;

        function calculateRisk() {
            let total = 0;
            document.querySelectorAll('.risk-checkbox').forEach(cb => {
                if (cb.checked) {
                    total += parseInt(cb.getAttribute('data-pts') || 0, 10);
                }
            });
            currentRiskScore = total;
            document.getElementById('risk-pill').innerText = total;
            updateRiskTile();
        }

        function toggleRiskSignature(checked) {
            isRiskSigned = checked;
            updateRiskTile();
        }

        function updateRiskTile() {
            const btn = document.getElementById('risk-btn');
            btn.style.flexDirection = "column";
            btn.style.padding = "6px";
            
            let label = `<span style="font-size:0.6rem; text-transform:uppercase;">Risk Assmt</span>`;
            
            if (isRiskSigned) {
                btn.className = "tile green";
                btn.innerHTML = `${label}<span style="font-size:1rem; font-weight:bold; margin-top:2px;">${currentRiskScore} ✓</span>`;
                return;
            }
            
            btn.innerHTML = `${label}<span style="font-size:1rem; font-weight:bold; margin-top:2px;">${currentRiskScore} pts</span>`;
            
            if (currentRiskScore <= 15) {
                btn.className = "tile green";
            } else if (currentRiskScore <= 20) {
                btn.className = "tile orange";
            } else {
                btn.className = "tile red";
            }
        }

        
    
