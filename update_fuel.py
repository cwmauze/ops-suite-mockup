import re

with open('index.html', 'r') as f:
    html = f.read()

old_fuel_section = """                    <div class="form-row">
                        <div class="form-group">
                            <label>Supply Tank</label>
                            <div style="display:flex; align-items:center; gap:10px;">
                                <input type="number" id="supply-tank" value="33" inputmode="decimal" pattern="[0-9]*" style="text-align:right;" oninput="calculateFuelTime()"> <span style="font-weight:bold; color:var(--text-secondary)">GAL</span>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Main Tank</label>
                            <div style="display:flex; align-items:center; gap:10px;">
                                <input type="number" id="main-tank" value="160" inputmode="decimal" pattern="[0-9]*" style="text-align:right;" oninput="calculateFuelTime()"> <span style="font-weight:bold; color:var(--text-secondary)">GAL</span>
                            </div>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group" style="flex: 1.2;">
                            <label>Burn Rate</label>
                            <div style="display:flex; align-items:center; gap:10px;">
                                <input type="number" id="burn-rate" value="74" style="text-align:right;" oninput="calculateFuelTime()"> <span style="font-weight:bold; color:var(--text-secondary)">GPH</span>
                            </div>
                        </div>
                        <div class="form-group" style="flex: 1;">
                            <label>Fuel Time</label>
                            <input type="text" id="fuel-time" value="02:58" inputmode="decimal" style="text-align:center; font-weight:bold; color:var(--accent-blue);" oninput="handleOverride('fuel-time')">
                        </div>
                        <div class="form-group" style="flex: 0.8;">
                            <label>S.O.B.</label>
                            <input type="number" id="sob" value="0" inputmode="decimal" style="text-align:center; font-weight:bold; color:var(--accent-blue);" oninput="handleOverride('sob')">
                        </div>
                    </div>"""

new_fuel_section = """                    <div class="form-row" style="gap: 5px;">
                        <div class="form-group" style="flex: 1.2;">
                            <label style="font-size: 0.7rem; text-align: center;">Supply <span style="color:var(--text-secondary)">(GAL)</span></label>
                            <input type="number" id="supply-tank" value="33" inputmode="decimal" pattern="[0-9]*" style="text-align:center; padding: 6px;" oninput="calculateFuelTime()">
                        </div>
                        <div class="form-group" style="flex: 1.2;">
                            <label style="font-size: 0.7rem; text-align: center;">Main <span style="color:var(--text-secondary)">(GAL)</span></label>
                            <input type="number" id="main-tank" value="160" inputmode="decimal" pattern="[0-9]*" style="text-align:center; padding: 6px;" oninput="calculateFuelTime()">
                        </div>
                        <div class="form-group" style="flex: 1.2;">
                            <label style="font-size: 0.7rem; text-align: center;">Burn <span style="color:var(--text-secondary)">(GPH)</span></label>
                            <input type="number" id="burn-rate" value="74" inputmode="decimal" pattern="[0-9]*" style="text-align:center; padding: 6px;" oninput="calculateFuelTime()">
                        </div>
                        <div class="form-group" style="flex: 1.2;">
                            <label style="font-size: 0.7rem; text-align: center;">Time</label>
                            <input type="text" id="fuel-time" value="02:58" inputmode="decimal" style="text-align:center; font-weight:bold; color:var(--accent-blue); padding: 6px;" oninput="handleOverride('fuel-time')">
                        </div>
                        <div class="form-group" style="flex: 1;">
                            <label style="font-size: 0.7rem; text-align: center;">S.O.B.</label>
                            <input type="number" id="sob" value="0" inputmode="decimal" style="text-align:center; font-weight:bold; color:var(--accent-blue); padding: 6px;" oninput="handleOverride('sob')">
                        </div>
                    </div>"""

html = html.replace(old_fuel_section, new_fuel_section)

with open('index.html', 'w') as f:
    f.write(html)
print("Updated index.html")
