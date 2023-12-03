//Denne funksjonen henter linken som hvert ikon i en grid skal linkes mot, og sender brukeren til det dokumentet
let sideButtons = document.querySelectorAll('.grid > div');
sideButtons.forEach(side =>{
    side.addEventListener('click', () =>{
        let lenke = side.getAttribute('side-lenke');
        window.open(lenke,'_self');
    })
})

//Når hjemknappen trykkes sendes brukeren til index
function hjemfunksjon(){
    window.open('index.html','_self');
}

//Create a link som senere linker til CSS dokumentet vi ønsker
const link = document.createElement('link');
link.rel = 'stylesheet';
document.getElementsByTagName('HEAD')[0].appendChild(link);

//Variabler som definerer nivået på lysstyrken til datamaskinen
var light = 100;
var grey = 65;
var dark = 0;
// Funksjonen kjøres kun når siden lastes inn
// Dersom det er første gang nettsiden åpnes har ingen av variablene blitt satt til true eller false. Da settes standard utseende til DarkMode
// Dersom siden tidligere er blitt lastet inn og lastes inn vil samme palett brukes igjen
// Her settes også hvilke kartlag som skal brukes
checkStatus()
function checkStatus(){
    if (sessionStorage.getItem('lightMode')==="true" && sessionStorage.getItem('greyMode')==="false" && sessionStorage.getItem('darkMode')==="false"){
        link.href = './css/light.css';   
        sendSliderToNodeRed(light);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
        }).addTo(map);

        // Maritimt kart med div detaljer
        L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
            maxZoom: 18,
        }).addTo(map);                
    }
    else if (sessionStorage.getItem('greyMode')==="true" && sessionStorage.getItem('lightMode')==="false" && sessionStorage.getItem('darkMode')==="false"){
        link.href = './css/grey.css';
        sendSliderToNodeRed(grey);
        L.tileLayer.provider('Stadia.AlidadeSmoothDark', {
            maxZoom: 18,
        }).addTo(map);

        // Maritimt kart med div detaljer
        L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
            maxZoom: 18,
        }).addTo(map);
    }
    else
    {
        link.href = './css/dark.css';
        sendSliderToNodeRed(dark);
        var Jawg_Matrix = L.tileLayer('https://{s}.tile.jawg.io/jawg-matrix/{z}/{x}/{y}{r}.png?access-token={accessToken}', {
            maxZoom: 18,
            accessToken: 'vxhrbt43N6yCkA3lhevguGdv4uUEDSLTPNVEcmWj6Z6txdKVKmiSrg0PUxxD4HIO'
        }).addTo(map);

        // Maritimt kart med div detaljer
        L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
            maxZoom: 18,
        }).addTo(map);
    }
}

// Hver gang man endre fargepalett kjøres denne funksjonen
// Her settes variabler som checkStatus bruker for å beholde fargepalett når siden lastes inn på nytt
// Funksjonen endrer også kartlaget som skal brukes
function changeStatus(tall){ 
    if (tall===0){     
        sessionStorage.setItem('lightMode', "true"); 
        sessionStorage.setItem('greyMode', "false");
        sessionStorage.setItem('darkMode', 'false');    
        link.href = './css/light.css';
        sendSliderToNodeRed(light);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
        }).addTo(map);

        // Maritimt kart med div detaljer
        L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
            maxZoom: 18,
        }).addTo(map);
    } 
    else if(tall===1){
        sessionStorage.setItem('lightMode', "false"); 
        sessionStorage.setItem('greyMode', "true"); 
        sessionStorage.setItem('darkMode', 'false');
        link.href = './css/grey.css';
        sendSliderToNodeRed(grey);

        L.tileLayer.provider('Stadia.AlidadeSmoothDark', {
            maxZoom: 18,
        }).addTo(map);

        // Maritimt kart med div detaljer
        L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
            maxZoom: 18,
        }).addTo(map);
    }
    else{
        sessionStorage.setItem('lightMode', "false");
        sessionStorage.setItem('greyMode', "false");
        sessionStorage.setItem('darkMode', 'true');
        link.href = './css/dark.css';
        sendSliderToNodeRed(dark);

        var Jawg_Matrix = L.tileLayer('https://{s}.tile.jawg.io/jawg-matrix/{z}/{x}/{y}{r}.png?access-token={accessToken}', {
            maxZoom: 18,
            accessToken: 'vxhrbt43N6yCkA3lhevguGdv4uUEDSLTPNVEcmWj6Z6txdKVKmiSrg0PUxxD4HIO'
        }).addTo(map);

        L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
            maxZoom: 18,
        }).addTo(map);
    }
}

// Dersom man trykker i kartet vil denne funksjonen vise en ny meny
function menyFunction() {
    document.getElementById('kart-meny').style.display = 'block';
}

// Denne funksjonen sender lysverdien valgt av fargepaletten til Node-RED
function sendSliderToNodeRed(verdi) {
    var urll = 'http://127.0.0.1:1880/slider'; // Adressen Node-RED kjører på
    var dataa = new URLSearchParams();
    dataa.append('range', verdi);

    fetch(urll, {
        method: 'POST',
        body: dataa,
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