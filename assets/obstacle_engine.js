// obstacle_engine.js - Handles terrain and obstacle calculations for flight routes

let globalObstacles = [];
let globalTerrain = {};
let engineReady = false;

async function initObstacleEngine() {
    try {
        console.log("Loading obstacle and terrain databases...");
        const [obsRes, terrRes] = await Promise.all([
            fetch('database/obstacles.json'),
            fetch('database/terrain.json')
        ]);
        globalObstacles = await obsRes.json();
        globalTerrain = await terrRes.json();
        engineReady = true;
        console.log(`Obstacle engine ready. Loaded ${globalObstacles.length} obstacles and terrain grid.`);
        // Dispatch event to redraw map/route if it was waiting
        document.dispatchEvent(new CustomEvent('obstacleEngineReady'));
    } catch (e) {
        console.error("Failed to load obstacle/terrain databases", e);
    }
}

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
    // Flat earth approximation for local segment projection
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
    
    // 1. Calculate bounding box for the segment with radius buffer
    // 1 degree latitude ~ 60 NM. 1 degree longitude ~ 60 * cos(lat) NM.
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

    // 2. Search obstacles within bounding box, then precise distance
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
    
    // 3. Search terrain grid within bounding box, then precise distance
    // The keys in terrain.json are like "41.0_-82.0"
    // So we iterate lat from boxMinLat rounded to 0.1, to boxMaxLat rounded to 0.1
    const startLat = Math.floor(boxMinLat * 10) / 10;
    const endLat = Math.ceil(boxMaxLat * 10) / 10;
    const startLon = Math.floor(boxMinLon * 10) / 10;
    const endLon = Math.ceil(boxMaxLon * 10) / 10;
    
    for (let lat = startLat; lat <= endLat; lat += 0.1) {
        for (let lon = startLon; lon <= endLon; lon += 0.1) {
            const key = `${lat.toFixed(1)}_${lon.toFixed(1)}`;
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

// Generate the capsule polygon coordinates for Leaflet
function getCapsulePolygon(wp1, wp2, radiusNM = 4, points = 16) {
    const lat1 = wp1.lat, lon1 = wp1.lon;
    const lat2 = wp2.lat, lon2 = wp2.lon;
    
    // Calculate heading from wp1 to wp2
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const y = Math.sin(dLon) * Math.cos(lat2 * Math.PI / 180);
    const x = Math.cos(lat1 * Math.PI / 180) * Math.sin(lat2 * Math.PI / 180) -
            Math.sin(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.cos(dLon);
    let brng = Math.atan2(y, x); // radians
    
    const R = 3440.065; // Earth radius in NM
    const angularDist = radiusNM / R;
    
    const polygon = [];
    
    // Helper to get destination point
    function destPoint(lat, lon, brngRad, dRad) {
        const latRad = lat * Math.PI / 180;
        const lonRad = lon * Math.PI / 180;
        const destLat = Math.asin(Math.sin(latRad)*Math.cos(dRad) + Math.cos(latRad)*Math.sin(dRad)*Math.cos(brngRad));
        const destLon = lonRad + Math.atan2(Math.sin(brngRad)*Math.sin(dRad)*Math.cos(latRad), Math.cos(dRad)-Math.sin(latRad)*Math.sin(destLat));
        return [destLat * 180 / Math.PI, destLon * 180 / Math.PI];
    }
    
    // Semicircle around wp2 (end point)
    for (let i = 0; i <= points; i++) {
        const angle = brng - Math.PI/2 + (Math.PI * i / points);
        polygon.push(destPoint(lat2, lon2, angle, angularDist));
    }
    
    // Semicircle around wp1 (start point)
    for (let i = 0; i <= points; i++) {
        const angle = brng + Math.PI/2 + (Math.PI * i / points);
        polygon.push(destPoint(lat1, lon1, angle, angularDist));
    }
    
    return polygon;
}
