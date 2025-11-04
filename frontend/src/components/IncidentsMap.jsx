import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import L from 'leaflet';

// Icons for different disaster types!
const iconMapping = {
  flood: "https://cdn-icons-png.flaticon.com/512/252/252035.png",
  earthquake: "https://cdn-icons-png.flaticon.com/512/1506/1506778.png",
  cloudburst: "https://cdn-icons-png.flaticon.com/512/481/481874.png",
  avalanche: "https://cdn-icons-png.flaticon.com/512/1779/1779940.png",
  default: "https://cdn-icons-png.flaticon.com/512/10086/10086903.png",
};

function getIncidentIcon(type) {
  return new L.Icon({
    iconUrl: iconMapping[type?.toLowerCase()] || iconMapping.default,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
  });
}

export default function IncidentsMap() {
  const [incidents, setIncidents] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/incidents")
      .then(res => setIncidents(res.data))
      .catch(() => setIncidents([]));
  }, []);

  let center = [20.6, 78.96];
  if (incidents.length) {
    let lats = incidents.map(i => i.latitude), lngs = incidents.map(i => i.longitude);
    center = [lats.reduce((a, b) => a + b, 0)/lats.length, lngs.reduce((a, b) => a + b, 0)/lngs.length];
  }

  return (
    <div style={{ height: "400px", width: "100%", margin: "32px auto", borderRadius: 16, overflow: "hidden" }}>
      <MapContainer center={center} zoom={5.5} scrollWheelZoom={true} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
        {incidents.map(incident => (
          <Marker
            key={incident.id || incident._id}
            position={[
              incident.latitude || 20.6,
              incident.longitude || 78.96
            ]}
            icon={getIncidentIcon(incident.disaster_type)}
          >
            <Popup>
              <b>{incident.title || incident.disaster_type}</b><br />
              {incident.description}<br />
              <span style={{ color: "#246" }}>
                Disaster: {incident.disaster_type} <br />
                Severity: {incident.severity || "-"}
              </span>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
