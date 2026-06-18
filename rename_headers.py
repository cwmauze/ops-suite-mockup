with open('index.html', 'r') as f:
    html = f.read()

html = html.replace(
    '<label style="font-size: 0.7rem; text-align: center;">Supply <span style="color:var(--text-secondary)">(GAL)</span></label>',
    '<label style="font-size: 0.7rem; text-align: center;">Supply Tanks <span style="color:var(--text-secondary)">(GAL)</span></label>'
)

html = html.replace(
    '<label style="font-size: 0.7rem; text-align: center;">Main <span style="color:var(--text-secondary)">(GAL)</span></label>',
    '<label style="font-size: 0.7rem; text-align: center;">Main tanks <span style="color:var(--text-secondary)">(GAL)</span></label>'
)

html = html.replace(
    '<label style="font-size: 0.7rem; text-align: center;">Burn <span style="color:var(--text-secondary)">(GPH)</span></label>',
    '<label style="font-size: 0.7rem; text-align: center;">Burn Rate <span style="color:var(--text-secondary)">(GPH)</span></label>'
)

html = html.replace(
    '<label style="font-size: 0.7rem; text-align: center;">Time</label>',
    '<label style="font-size: 0.7rem; text-align: center;">Fuel time</label>'
)

with open('index.html', 'w') as f:
    f.write(html)
print("Updated headers")
