async function submitForm() {
    const home = document.getElementById("home").value.trim();
    const officesRaw = document.getElementById("offices").value.trim();

    if (!home || !officesRaw) {
        alert("Please enter both home and office locations.");
        return;
    }

    const office_locations = officesRaw.split("\n").map(line => line.trim()).filter(Boolean);

    const response = await fetch("http://127.0.0.1:8000/commute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ home_location: home, office_locations })
    });

    if (!response.ok) {
        const err = await response.json();
        alert(`Error: ${err.detail}`);
        return;
    }

    const results = await response.json();
    drawMap(home, results);
}

let map;

function drawMap(homeLabel, data) {
    const home = data.find(loc => loc.id === "home") || { lat: data[0].lat, lng: data[0].lng }; // fallback

    if (map) {
        map.remove();
    }

    map = L.map("map").setView([home.lat, home.lng], 13);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19
    }).addTo(map);

    const homeMarker = L.marker([home.lat, home.lng], { title: "Home" })
        .addTo(map)
        .bindPopup(`<b>Home:</b><br>${homeLabel}`)
        .openPopup();

    data.forEach(loc => {
        if (loc.id === "home") return;
        const marker = L.marker([loc.lat, loc.lng])
            .addTo(map)
            .bindPopup(`<b>${loc.id}</b><br>Travel time: ${loc.travel_time_minutes} min`);

        L.polyline([
            [home.lat, home.lng],
            [loc.lat, loc.lng]
        ], {
            color: "gray",
            weight: 2
        }).addTo(map);
    });
}