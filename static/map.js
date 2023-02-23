var map = L.map('map').setView([57, -4.5], 8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var pathArray = window.location.pathname.split('/');
if (pathArray.length > 1) {
    var user1 = pathArray[0];
    var user2 = pathArray[1];
}

function makeIcon(colour) {
    var icon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-' + colour + '.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [12, 20],
        iconAnchor: [6, 20],
        popupAnchor: [1, -15],
        shadowSize: [20, 20]
    });
    return icon;
}

const icons = {
    "both": makeIcon("blue"),
    "only1": makeIcon("green"),
    "only2": makeIcon("yellow"),
    "neither": makeIcon("red")
};

async function addMarkers() {
    let url = window.location + ".json"
    let mountains = await (await fetch(url)).json();
    mountains.forEach(row => {
        var icon = icons[row[3]];
        var marker = L.marker(row[1], {icon: icon}).addTo(map)
        marker.bindPopup(row[0]);
    });
}
addMarkers();