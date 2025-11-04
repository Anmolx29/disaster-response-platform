import React, { useEffect, useState } from 'react';
import { Box, AppBar, Toolbar, Typography, Grid, Button, Card } from '@mui/material';
import { motion } from 'framer-motion';
import axios from 'axios';
import StatCard from '../components/StatCard';
import IncidentTable from '../components/IncidentTable';
import IncidentsMap from '../components/IncidentsMap';
import IncidentTrendsChart from "../components/IncidentTrendsChart";
import PredictionPanel from "../components/PredictionPanel";

const heroImg = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80";

// Animated overlay icons
const overlayIcons = {
  flood: "🌊", fire: "🔥", ambulance: "🚑", alert: "🚨"
};

// Disaster types you want cards for - add/remove types as needed!
const DISASTER_TYPES = [
  { type: "flood", label: "Flood", icon: "🌊", color: "#76d1f2", img: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=60" },
  { type: "earthquake", label: "Earthquake", icon: "🌎", color: "#bca5f2", img: "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=60" },
  { type: "cloudburst", label: "Cloudburst", icon: "🌧️", color: "#bbdefb", img: "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=60" },
  { type: "avalanche", label: "Avalanche", icon: "🏔️", color: "#d7f3f7", img: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=400&q=60" },
];

export default function Dashboard() {
  const [incidentCounts, setIncidentCounts] = useState({});
  const [resourceCount, setResourceCount] = useState("-");
  const [alertCount, setAlertCount] = useState("-");
  const [timestamp, setTimestamp] = useState(() => (new Date()).toLocaleTimeString());

  useEffect(() => {
    setInterval(() => setTimestamp((new Date()).toLocaleTimeString()), 1000);

    axios.get('http://localhost:8000/incidents')
      .then(res => {
        // Count incidents by disaster_type
        const counts = {};
        res.data.forEach(inc => {
          const key = (inc.disaster_type || "unknown").toLowerCase();
          counts[key] = (counts[key] || 0) + 1;
        });
        setIncidentCounts(counts);
      })
      .catch(() => setIncidentCounts({}));

    axios.get('http://localhost:8000/resources')
      .then(res => setResourceCount(res.data.length))
      .catch(() => setResourceCount("N/A"));

    setAlertCount(Math.floor(Math.random() * 20) + 10);
  }, []);

  return (
    <Box sx={{
      minHeight: "100vh",
      background: "linear-gradient(120deg, #1e3c72 0%, #2a5298 100%)",
      pb: 4,
      color: "#f5f5f5"
    }}>
      <AppBar
        position="sticky"
        sx={{
          background: "rgba(25,34,67,0.90)",
          boxShadow: "0 8px 36px 0 rgba(30,60,120,0.24)"
        }}>
        <Toolbar>
          <Typography variant="h5" sx={{ flexGrow: 1, fontWeight: 900, letterSpacing: 2 }}>
            Disaster Response Command Center
          </Typography>
          <Typography variant="body1" sx={{ opacity: 0.8, fontWeight: 600 }}>{timestamp}</Typography>
        </Toolbar>
      </AppBar>

      {/* Hero Section */}
      <Box sx={{
        mt: 4,
        mx: "auto",
        maxWidth: "85vw",
        borderRadius: 5,
        overflow: "hidden",
        position: "relative",
        boxShadow: "0 8px 36px #2229"
      }}>
        <img src={heroImg} alt="Disaster Response" style={{
          width: "100%",
          height: "280px",
          objectFit: "cover",
          filter: "brightness(0.58) blur(1px)"
        }} />
        <Typography variant="h3"
          sx={{ position: "absolute", top: 35, left: 48, color: "#fff", fontWeight: 900, textShadow: "0 6px 24px #0008" }}>
          Real-time Emergency Dashboard
        </Typography>
        {/* Animated Icon Overlays */}
        <Box sx={{ position: "absolute", left: 40, bottom: 28, display: "flex", gap: 2 }}>
          {Object.entries(overlayIcons).map(([key, icon], i) => (
            <motion.div
              key={key}
              animate={{ y: [0, -16, 0] }}
              transition={{ repeat: Infinity, duration: 1.5 + i * 0.2 }}
              style={{ fontSize: 38, marginRight: 20, textShadow: "0 1px 8px #222a" }}
            >
              {icon}
            </motion.div>
          ))}
        </Box>
        <Typography variant="h6"
          sx={{ position: "absolute", bottom: 18, right: 32, color: "#e3e3e3", fontWeight: 500, background: "#1848addd", borderRadius: 2, px: 3, py: 1 }}>
          AI Powered • Secure • Multi-Agency
        </Typography>
      </Box>

      {/* Stat Cards—one per disaster type + resources + alerts */}
      <Grid container spacing={4} sx={{ maxWidth: "1300px", mx: "auto", mt: 4 }}>
        {DISASTER_TYPES.map(dt => (
          <Grid item xs={12} md={3} key={dt.type}>
            <StatCard
              label={dt.label + " Incidents"}
              value={incidentCounts[dt.type] || 0}
              icon={dt.icon}
              img={dt.img}
              color={dt.color}
            />
          </Grid>
        ))}
        <Grid item xs={12} md={3}>
          <StatCard
            label="Resources"
            value={resourceCount}
            icon="🚑"
            img="https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?auto=format&fit=crop&w=400&q=60"
            color="#e7a331"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            label="Alerts Sent"
            value={alertCount}
            icon="🚨"
            img="https://images.unsplash.com/photo-1506784992012-a3566c4888a1?auto=format&fit=crop&w=400&q=60"
            color="#ff6e7b"
          />
        </Grid>
      </Grid>

      <IncidentTable />
      <IncidentTrendsChart />
      <IncidentsMap />
      <PredictionPanel />

      {/* Main Action Buttons */}
      <Box sx={{ textAlign: "center", mt: 6 }}>
        <motion.div
          whileHover={{ scale: 1.08 }}
          transition={{ type: "spring", stiffness: 220, damping: 17 }}
        >
          <Button variant="contained" size="large" sx={{
            mx: 2, py: 1.4, px: 5, fontWeight: 700, letterSpacing: 1,
            background: "linear-gradient(95deg,#21d4fd 0%,#b721ff 100%)",
            boxShadow: "0 2px 20px #6590ff44"
          }}>Run AI Prediction</Button>
          <Button variant="contained" size="large" color="info" sx={{
            mx: 2, py: 1.4, px: 5, fontWeight: 700, letterSpacing: 1,
            background: "linear-gradient(82deg,#fad961 0%,#f76b1c 100%)",
            boxShadow: "0 2px 20px #fa6f1c29"
          }}>Optimize Resources</Button>
          <Button variant="outlined" size="large" color="error" sx={{
            mx: 2, py: 1.4, px: 5, fontWeight: 700, letterSpacing: 1,
            borderWidth: 3,
            borderColor: "#fff",
            color: "#fff",
            boxShadow: "0 2px 20px #ff476e44"
          }}>Send Alert</Button>
        </motion.div>
      </Box>

      <Box sx={{ maxWidth: 900, mt: 6, mx: "auto" }}>
        <Card sx={{
          px: 5, py: 4, borderRadius: 6,
          background: "rgba(245, 251, 255, 0.24)",
          boxShadow: "0 8px 48px #1e2d4b22",
          backdropFilter: "blur(18px)"
        }}>
          <Typography variant="h5" sx={{ fontWeight: 700, color: "#18316f", letterSpacing: 1, mb: 1 }}>
            Platform Capabilities
          </Typography>
          <Typography sx={{ color: "#425b98" }}>
            Real-time analytics, AI-powered disaster prediction, resource optimization, and multi-channel emergency alerting—all on one secure dashboard, designed for rapid decision-making and cross-agency coordination.
          </Typography>
        </Card>
      </Box>
    </Box>
  );
}
