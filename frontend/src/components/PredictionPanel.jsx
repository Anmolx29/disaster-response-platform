import React, { useState } from 'react';
import { Paper, Typography, Button, MenuItem, Select, TextField, Box, Alert } from '@mui/material';
import axios from 'axios';

const disasterFields = {
  flood: [
    { name: "rainfall", label: "Rainfall (mm)", type: "number" },
    { name: "river_level", label: "River Level (m)", type: "number" },
    { name: "soil_moisture", label: "Soil Moisture (%)", type: "number" },
    { name: "temperature", label: "Temperature (°C)", type: "number" },
    { name: "humidity", label: "Humidity (%)", type: "number" },
  ],
  earthquake: [
    { name: "magnitude", label: "Magnitude", type: "number" },
    { name: "depth", label: "Depth (km)", type: "number" },
    { name: "distance_from_fault", label: "Distance from Fault (km)", type: "number" },
    { name: "peak_ground_accel", label: "Peak Ground Accel (g)", type: "number" },
  ],
  cloudburst: [
    { name: "rainfall_rate", label: "Rainfall Rate (mm/hr)", type: "number" },
    { name: "duration", label: "Duration (min)", type: "number" },
    { name: "cloud_water_content", label: "Cloud Water Content (g/m³)", type: "number" },
    { name: "temp_diff", label: "Temperature Difference (°C)", type: "number" },
  ],
  avalanche: [
    { name: "snow_depth", label: "Snow Depth (cm)", type: "number" },
    { name: "slope_angle", label: "Slope Angle (deg)", type: "number" },
    { name: "temperature", label: "Temperature (°C)", type: "number" },
    { name: "wind_speed", label: "Wind Speed (km/h)", type: "number" },
  ],
};

export default function PredictionPanel() {
  const [disasterType, setDisasterType] = useState("flood");
  const [params, setParams] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const fields = disasterFields[disasterType];

  function handleChange(e) {
    setParams({ ...params, [e.target.name]: parseFloat(e.target.value) });
  }

  function handlePredict() {
    setPrediction(null);
    setError(null);
    axios.post(`http://localhost:8000/predict/${disasterType}`, params)
      .then(res => setPrediction(res.data))
      .catch(err => setError("Could not predict. Check parameters and server!"));
  }

  return (
    <Paper elevation={5} sx={{
      p: 4, maxWidth: 500, mx: "auto", mt: 4, borderRadius: 4, background: "#e8f4ff"
    }}>
      <Typography variant="h5" sx={{ fontWeight: 700, color: "#1356a8" }}>
        AI Disaster Prediction Simulator
      </Typography>
      <Box sx={{ mt: 2 }}>
        <Select
          value={disasterType}
          onChange={e => setDisasterType(e.target.value)}
          sx={{ mb: 2, width: "100%" }}>
          <MenuItem value="flood">Flood</MenuItem>
          <MenuItem value="earthquake">Earthquake</MenuItem>
          <MenuItem value="cloudburst">Cloudburst</MenuItem>
          <MenuItem value="avalanche">Avalanche</MenuItem>
        </Select>
        {fields.map(f => (
          <TextField
            key={f.name}
            name={f.name}
            label={f.label}
            type={f.type}
            onChange={handleChange}
            sx={{ mb: 2, width: "100%" }}
            required
          />
        ))}
        <Button variant="contained" color="primary" onClick={handlePredict} sx={{ mb: 2, width: "100%" }}>
          Predict Risk
        </Button>
        {error && <Alert severity="error">{error}</Alert>}
        {prediction && (
          <Paper elevation={2} sx={{ mt: 2, p: 2, background: "#fffbee", borderRadius: 2 }}>
            <Typography variant="h6" sx={{ color: "#de7500", fontWeight: 700 }}>Prediction Result:</Typography>
            <pre style={{ fontSize: 15, margin: 0 }}>{JSON.stringify(prediction, null, 2)}</pre>
          </Paper>
        )}
      </Box>
    </Paper>
  );
}
