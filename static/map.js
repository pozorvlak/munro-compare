var map = L.map('map').setView([57, -4], 8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

mountains.forEach(row => {
    L.marker(row[1]).addTo(map)
});