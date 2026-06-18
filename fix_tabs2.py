with open('index.html', 'r') as f:
    html = f.read()

old_code = """                let labelText = `Leg ${leg.id}: ${leg.origin} ➔ ${leg.dest}`;
                if (AppState.legs.length >= 3) {
                    labelText = `${leg.origin} ➔ ${leg.dest}`;
                }"""

new_code = """                let labelText = `Leg ${leg.id}: ${leg.origin} ➔ ${leg.dest}`;
                if (AppState.legs.length === 3) {
                    labelText = `${leg.id}: ${leg.origin} ➔ ${leg.dest}`;
                } else if (AppState.legs.length > 3) {
                    labelText = `${leg.origin} ➔ ${leg.dest}`;
                }"""

html = html.replace(old_code, new_code)

with open('index.html', 'w') as f:
    f.write(html)
print("Updated tabs again")
