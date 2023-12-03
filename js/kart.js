// Lager kart og merke/ikon
var map = L.map('map');
// Ikonet til fartøyets posisjo
var boat = L.icon({
    iconUrl: './bilder/ikoner/boat.svg',
    iconSize:     [40, 40], // Størrelsen på ikonet
    iconAnchor:   [20, 20], // Hvor ankeret til ikonet er i forhold til størrelsen
});
// Henter ut koordinater fra lokal fil og sentrerer kartet rund posisjonen til fartøyet
fetch('./data_inn/live_pos/ais.txt') 
.then(response => response.text())
.then(data => {
    //Henter lengdegrad, breddegrad og heading og lagrer dette til hver sin variabel
    const coordinates = JSON.parse(data);
    var bredde = coordinates.latitude;
    var lengde = coordinates.longitude;
    var heading = coordinates.trueHeading;

    map.setView([bredde, lengde], 10); // Setter senter på kart til nåværende posisjon, med zoom-nivå lik 10
    let m = L.marker([bredde, lengde], {icon: boat}).addTo(map); // Legger til båt-ikon på nåværende posisjon
    m.setRotationAngle(heading); //Setter retning på ikonet etter virkelig heading
})
// Dersom det ikke går an å hente ut koordinater fra fil
.catch(error => {
    console.error('Error loading coordinates from the text file:', error);
    map.setView([60.343, 5.229]); // Dersom ingen posisjon finnes, setter posisjon til Haakonsvern
});

//Koordinater til polygonet som dekker Fedje VTS
var latlngs = [
    [60.09627, 4.94949],
    [60.16582, 4.93125],
    [60.15676, 5.00322],
    [60.1717, 5.10935],
    [60.20352, 5.16586],
    [60.67556, 4.79263],
    [60.67574, 4.43304],
    [60.94736, 4.29949],
    [60.94606, 4.95263],
    [60.79956, 5.1872],
    [60.77311, 5.1609],
    [60.83461, 4.8074],
    [60.7856, 4.79804],
    [60.39615, 5.26359],
    [60.29256, 5.19905],
    [60.19823, 5.249],
    [60.16611, 5.18791],
    [60.13584, 5.04036]
];
//Markerer Fedje VTS i kartet
var poly1 = L.polygon(latlngs, {color: '#be252399'}).addTo(map);

// Dersom man trykker et sted i kartet
var marker;
map.on('click', function(e) {
    var latlng = e.latlng;
    //Sender koordinatene til Node-red for bearbeiding ol.
    sendCoordinatesToNodeRed(latlng);

    // Fjerner tidligere merke i kartet, dersom det eksisterer
    if (marker) {
        map.removeLayer(marker);
    }

    // Lager merke i kart der man trykker
    marker = L.marker(latlng).addTo(map);
});

// Funksjon for å sende koordinater til Node-red
function sendCoordinatesToNodeRed(latlng) {
    var url = 'http://127.0.0.1:1880/coordinates'; // Adresse til Node-red
    var data = new URLSearchParams();
    data.append('latitude', latlng.lat);
    data.append('longitude', latlng.lng);

    fetch(url, {
        method: 'POST',
        body: data,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    // Respons i konsoll
    .then(response => {
        if (response.ok) {
            console.log('Coordinates sent to Node-RED successfully.');
        } else {
            console.error('Error sending coordinates to Node-RED.');
        }
    })
    .catch(error => {
        console.error('Network error:', error);
    });
}