import os

html_files = ["index.html", "home.html", "manifest.html", "flightlog.html", "CHANGELOG.md"]

replacements = {
    "Mauze, Charles": "Stallone, Sylvester",
    "Charles Mauze": "Sylvester Stallone",
    "Mauze": "Stallone",
    "Leake": "Schwarzenegger",
    "Robert Leake": "Arnold Schwarzenegger",
    "Leake, Robert": "Schwarzenegger, Arnold"
}

for file in html_files:
    if os.path.exists(file):
        with open(file, "r") as f:
            content = f.read()
            
        original_content = content
        for k, v in replacements.items():
            content = content.replace(k, v)
            
        if content != original_content:
            with open(file, "w") as f:
                f.write(content)
            print(f"Updated {file}")
