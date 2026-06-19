var fs = Object(); // Mock
var data = [
  {"id": "RWI", "name": "ROCKY MOUNT", "lat": 35.85, "lon": -77.89, "type": "APT"}
];

var waypointsData = {};

data.forEach(function(item) {
    if (item.id && item.lat !== undefined && item.lon !== undefined) {
        var wp = {
            id: item.id.toUpperCase(),
            name: item.name || 'Airport',
            category: 'FAA Airport',
            lat: parseFloat(item.lat),
            lon: parseFloat(item.lon)
        };
        
        waypointsData[item.id.toUpperCase()] = wp;
        
        if (item.id.length === 3 && /^[A-Z]{3}$/i.test(item.id)) {
            // Object spread is not supported in JXA, but it's supported in Chrome.
            waypointsData['K' + item.id.toUpperCase()] = Object.assign({}, wp, {id: 'K' + item.id.toUpperCase()});
        }
    }
});

console.log(JSON.stringify(waypointsData));
