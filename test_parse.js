const fs = require('fs');

function splitCSVLine(text) {
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
}

const csvText = fs.readFileSync('database/ecu_health_identifiers.csv', 'utf8');
const lines = csvText.split('\n');
const waypointsData = {};

for (let i = 1; i < lines.length; i++) {
    let line = lines[i].trim();
    if (!line) continue;
    
    const row = splitCSVLine(line);
    if (row.length >= 8) {
        let designation = row[0] || row[2];
        let title = row[1];
        let category = row[3];
        let latStr = row[6] ? row[6].replace(/'/g, '') : '';
        let lonStr = row[7] ? row[7].replace(/'/g, '') : '';
        let lat = parseFloat(latStr);
        let lon = parseFloat(lonStr);
        
        if (designation && !isNaN(lat) && !isNaN(lon)) {
            waypointsData[designation.toUpperCase()] = {
                id: designation.toUpperCase(),
                name: title,
                lat: lat,
                lon: lon
            };
        }
    }
}
console.log("Keys found:", Object.keys(waypointsData).length);
console.log("1NR1:", waypointsData['1NR1']);
console.log("KRWI:", waypointsData['KRWI']);
