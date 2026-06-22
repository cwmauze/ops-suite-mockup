const fs = require('fs');

const globalObstacles = JSON.parse(fs.readFileSync('database/obstacles.json', 'utf8'));
const globalTerrain = JSON.parse(fs.readFileSync('database/terrain.json', 'utf8'));
const engineReady = true;

function haversineNM(lat1, lon1, lat2, lon2) {
    const R = 3440.065; 
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

function pointToSegmentDistanceNM(px, py, ax, ay, bx, by) {
    const cosLat = Math.cos((ay * Math.PI) / 180);
    const dx = (bx - ax) * cosLat;
    const dy = by - ay;
    const l2 = dx*dx + dy*dy;
    
    if (l2 === 0) return haversineNM(ay, ax, py, px);
    
    const px_proj = (px - ax) * cosLat;
    const py_proj = py - ay;
    
    let t = ((px_proj * dx) + (py_proj * dy)) / l2;
    t = Math.max(0, Math.min(1, t));
    
    const projX = ax + t * (bx - ax);
    const projY = ay + t * (by - ay);
    
    return haversineNM(py, px, projY, projX);
}

function calculateLegPeakElevation(wp1, wp2, radiusNM = 4) {
    if (!engineReady) return null;
    
    let maxElev = 0;
    let peakLat = null;
    let peakLon = null;
    const ax = wp1.lon, ay = wp1.lat;
    const bx = wp2.lon, by = wp2.lat;
    
    const maxLat = Math.max(ay, by);
    const minLat = Math.min(ay, by);
    const maxLon = Math.max(ax, bx);
    const minLon = Math.min(ax, bx);
    
    const latBuffer = (radiusNM + 1) / 60.0;
    const lonBuffer = (radiusNM + 1) / (60.0 * Math.cos(minLat * Math.PI / 180));
    
    const boxMinLat = minLat - latBuffer;
    const boxMaxLat = maxLat + latBuffer;
    const boxMinLon = minLon - lonBuffer;
    const boxMaxLon = maxLon + lonBuffer;

    for (const obs of globalObstacles) {
        if (obs.lat >= boxMinLat && obs.lat <= boxMaxLat && obs.lon >= boxMinLon && obs.lon <= boxMaxLon) {
            const dist = pointToSegmentDistanceNM(obs.lon, obs.lat, ax, ay, bx, by);
            if (dist <= radiusNM) {
                if (obs.msl > maxElev) {
                    maxElev = obs.msl;
                    peakLat = obs.lat;
                    peakLon = obs.lon;
                }
            }
        }
    }
    
    const startLat = Math.floor(boxMinLat * 10) / 10;
    const endLat = Math.ceil(boxMaxLat * 10) / 10;
    const startLon = Math.floor(boxMinLon * 10) / 10;
    const endLon = Math.ceil(boxMaxLon * 10) / 10;
    
    for (let lat = startLat; lat <= endLat; lat += 0.1) {
        for (let lon = startLon; lon <= endLon; lon += 0.1) {
            const key = \`\${lat.toFixed(1)}_\${lon.toFixed(1)}\`;
            const terrData = globalTerrain[key];
            if (terrData) {
                const elev = terrData[0];
                const tLat = terrData[1];
                const tLon = terrData[2];
                const dist = pointToSegmentDistanceNM(tLon, tLat, ax, ay, bx, by);
                if (dist <= radiusNM) {
                    if (elev > maxElev) {
                        maxElev = elev;
                        peakLat = tLat;
                        peakLon = tLon;
                    }
                }
            }
        }
    }
    
    if (maxElev > 0) return { elevation: maxElev, lat: peakLat, lon: peakLon };
    return null;
}

const wp1 = {'lat': 35.539, 'lon': -78.389}; // JNX
const wp2 = {'lat': 35.214, 'lon': -80.943}; // CLT
const wp3 = {'lat': 35.436, 'lon': -82.541}; // AVL

console.log('JNX-CLT:', calculateLegPeakElevation(wp1, wp2, 25));
console.log('CLT-AVL:', calculateLegPeakElevation(wp2, wp3, 25));

