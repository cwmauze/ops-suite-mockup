import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Insert CSS before </style>
css = """
        .time-picker-popover {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #d1d5db;
            z-index: 10000;
            display: none;
            flex-direction: column;
            border-top: 1px solid var(--border-color);
            padding-bottom: env(safe-area-inset-bottom);
        }
        
        [data-theme="dark"] .time-picker-popover, [data-theme="hc-dark"] .time-picker-popover {
            background-color: #333;
        }

        .picker-header {
            display: flex;
            justify-content: space-between;
            padding: 10px 15px;
            background-color: #f3f4f6;
            border-bottom: 1px solid var(--border-color);
        }

        [data-theme="dark"] .picker-header, [data-theme="hc-dark"] .picker-header {
            background-color: #222;
        }

        .picker-btn {
            background: none;
            border: none;
            color: #007aff;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
        }

        .picker-body {
            display: flex;
            height: 200px;
            position: relative;
            background: white;
            overflow: hidden;
        }

        [data-theme="dark"] .picker-body, [data-theme="hc-dark"] .picker-body {
            background: #000;
            color: white;
        }

        .picker-highlight {
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            height: 40px;
            margin-top: -20px;
            background-color: rgba(0, 122, 255, 0.1);
            border-top: 1px solid rgba(0, 122, 255, 0.3);
            border-bottom: 1px solid rgba(0, 122, 255, 0.3);
            pointer-events: none;
        }

        .picker-column {
            flex: 1;
            overflow-y: scroll;
            scroll-snap-type: y mandatory;
            scrollbar-width: none;
            -ms-overflow-style: none;
            padding: 80px 0;
        }
        
        .picker-column::-webkit-scrollbar {
            display: none;
        }

        .picker-item {
            height: 40px;
            line-height: 40px;
            text-align: center;
            font-size: 1.4rem;
            scroll-snap-align: center;
            font-family: monospace;
            cursor: pointer;
        }
        
        .picker-label {
            position: absolute;
            top: 50%;
            margin-top: -10px;
            font-size: 0.9rem;
            font-weight: bold;
            color: var(--text-primary);
            pointer-events: none;
        }
"""
html = html.replace('</style>', css + '\n    </style>')

# 2. Insert HTML popover before <div id="simulated-keyboard"
popover_html = """
        <!-- Simulated Time Picker -->
        <div id="simulated-time-picker" class="time-picker-popover" onmousedown="event.preventDefault()">
            <div class="picker-header">
                <button class="picker-btn" style="color:var(--accent-red);" onclick="closeTimePicker()">Cancel</button>
                <div style="font-weight:bold; font-size:1.1rem; line-height:1.5;">Time</div>
                <button class="picker-btn" onclick="applyTimePicker()">Done</button>
            </div>
            <div class="picker-body">
                <div class="picker-highlight"></div>
                <div class="picker-label" style="left: 30%;">hrs</div>
                <div class="picker-label" style="left: 80%;">min</div>
                <div id="picker-col-hours" class="picker-column" onscroll="snapPicker('hours')">
                    <!-- populated by js -->
                </div>
                <div id="picker-col-minutes" class="picker-column" onscroll="snapPicker('minutes')">
                    <!-- populated by js -->
                </div>
            </div>
        </div>
"""
html = html.replace('<div id="simulated-keyboard"', popover_html + '\n        <div id="simulated-keyboard"')

# 3. Add JS Logic for time picker
js_logic = """
        // Time Picker Logic
        let activeTimeInput = null;
        let pickerScrollTimeout = null;

        function initTimePicker() {
            const hCol = document.getElementById('picker-col-hours');
            const mCol = document.getElementById('picker-col-minutes');
            
            for (let i = 0; i < 24; i++) {
                let div = document.createElement('div');
                div.className = 'picker-item';
                div.innerText = i.toString().padStart(2, '0');
                div.onclick = () => scrollToPickerItem(hCol, i);
                hCol.appendChild(div);
            }
            
            for (let i = 0; i < 60; i++) {
                let div = document.createElement('div');
                div.className = 'picker-item';
                div.innerText = i.toString().padStart(2, '0');
                div.onclick = () => scrollToPickerItem(mCol, i);
                mCol.appendChild(div);
            }
        }
        initTimePicker();

        function scrollToPickerItem(col, index) {
            col.scrollTo({ top: index * 40, behavior: 'smooth' });
        }

        function openTimePicker(input) {
            activeTimeInput = input;
            document.getElementById('simulated-keyboard').style.display = 'none';
            document.getElementById('simulated-numpad').style.display = 'none';
            document.getElementById('simulated-time-picker').style.display = 'flex';
            
            // Parse existing time
            let val = input.value || '';
            let h = 0, m = 0;
            
            // Extract HH:MM if it contains it
            const timeMatch = val.match(/([0-9]{2}):([0-9]{2})/);
            if (timeMatch) {
                h = parseInt(timeMatch[1], 10);
                m = parseInt(timeMatch[2], 10);
            } else {
                // If now date
                const now = new Date();
                h = now.getUTCHours();
                m = now.getUTCMinutes();
            }
            
            const hCol = document.getElementById('picker-col-hours');
            const mCol = document.getElementById('picker-col-minutes');
            
            // Wait for display:flex to render
            setTimeout(() => {
                hCol.scrollTo({ top: h * 40, behavior: 'instant' });
                mCol.scrollTo({ top: m * 40, behavior: 'instant' });
            }, 10);
        }

        function closeTimePicker() {
            document.getElementById('simulated-time-picker').style.display = 'none';
            if (activeTimeInput) activeTimeInput.blur();
            activeTimeInput = null;
        }

        function applyTimePicker() {
            if (!activeTimeInput) return;
            
            const hCol = document.getElementById('picker-col-hours');
            const mCol = document.getElementById('picker-col-minutes');
            
            const h = Math.round(hCol.scrollTop / 40);
            const m = Math.round(mCol.scrollTop / 40);
            
            const hStr = h.toString().padStart(2, '0');
            const mStr = m.toString().padStart(2, '0');
            
            let val = activeTimeInput.value || '';
            const timeMatch = val.match(/([0-9]{2}):([0-9]{2})/);
            
            if (timeMatch) {
                val = val.replace(/[0-9]{2}:[0-9]{2}/, `${hStr}:${mStr}`);
            } else {
                // If it was empty, prepend today's date
                const now = new Date();
                const year = now.getUTCFullYear();
                const month = String(now.getUTCMonth() + 1).padStart(2, '0');
                const day = String(now.getUTCDate()).padStart(2, '0');
                val = `${year}-${month}-${day} ${hStr}:${mStr}`;
            }
            
            activeTimeInput.value = val;
            activeTimeInput.dispatchEvent(new Event('input', { bubbles: true }));
            closeTimePicker();
        }

        function snapPicker(type) {
            // Optional: add tactile feedback or update UI while scrolling
        }
"""
html = html.replace('// Simulate keyboard on touch/focus', js_logic + '\n        // Simulate keyboard on touch/focus')

# 4. Modify the focus listener to show time picker for `.datetime-sim`
old_focus = """        document.addEventListener('focusin', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                const type = e.target.type;
                const inputmode = e.target.inputMode;
                const isNumeric = type === 'number' || inputmode === 'decimal' || inputmode === 'numeric';
                
                if (isNumeric) {
                    document.getElementById('simulated-keyboard').style.display = 'none';
                    document.getElementById('simulated-numpad').style.display = 'flex';
                } else {
                    document.getElementById('simulated-numpad').style.display = 'none';
                    document.getElementById('simulated-keyboard').style.display = 'flex';
                }
            }
        });"""

new_focus = """        document.addEventListener('focusin', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                document.getElementById('simulated-keyboard').style.display = 'none';
                document.getElementById('simulated-numpad').style.display = 'none';
                document.getElementById('simulated-time-picker').style.display = 'none';
                
                if (e.target.classList.contains('datetime-sim')) {
                    openTimePicker(e.target);
                    return;
                }
                
                const type = e.target.type;
                const inputmode = e.target.inputMode;
                const isNumeric = type === 'number' || inputmode === 'decimal' || inputmode === 'numeric';
                
                if (isNumeric) {
                    document.getElementById('simulated-numpad').style.display = 'flex';
                } else {
                    document.getElementById('simulated-keyboard').style.display = 'flex';
                }
            }
        });"""

html = html.replace(old_focus, new_focus)

with open('index.html', 'w') as f:
    f.write(html)
print("Updated index.html")
