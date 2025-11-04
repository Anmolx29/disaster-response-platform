import React, { useEffect, useState } from 'react';
import { Paper, Table, TableHead, TableBody, TableRow, TableCell, Typography, Chip } from '@mui/material';
import { motion, AnimatePresence } from "framer-motion";
import axios from 'axios';

export default function IncidentTable() {
  const [incidents, setIncidents] = useState([]);

  useEffect(() => {
    fetchIncidents();
    const id = setInterval(fetchIncidents, 9000); // refresh every 9s
    return () => clearInterval(id);
  }, []);

  function fetchIncidents() {
    axios.get('http://localhost:8000/incidents')
      .then(res => setIncidents(Array.isArray(res.data) ? res.data.slice(-6).reverse() : []))
      .catch(() => setIncidents([]));
  }

  return (
    <Paper
      elevation={5}
      sx={{ p: 3, borderRadius: 4, mt: 4, background: "rgba(240,247,255,0.97)" }}
    >
      <Typography variant="h6" sx={{ mb: 2, fontWeight: 700, color: "#1848ad" }}>
        Recent Active Disaster Incidents (Live)
      </Typography>
      {incidents.length === 0 ? (
        <Typography color="warning.main">No incidents yet!</Typography>
      ) : (
        <Table>
          <TableHead>
            <TableRow sx={{ bgcolor: "#eaf4fa" }}>
              <TableCell><b>Type</b></TableCell>
              <TableCell><b>Location</b></TableCell>
              <TableCell align="center"><b>Status</b></TableCell>
              <TableCell><b>Reported</b></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <AnimatePresence>
              {incidents.map((row, i) => (
                <motion.tr
                  key={row._id || i}
                  initial={{ opacity: 0, x: 60 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -60 }}
                  transition={{ duration: 0.6, delay: i * 0.08 }}
                  style={{ background: i % 2 ? "#f5fafd" : "#eaf9ff" }}
                >
                  <TableCell>
                    <Chip label={row.type || "Unknown"} color={row.type === "Flood" ? "primary" : "warning"} sx={{ fontWeight: 700 }} />
                  </TableCell>
                  <TableCell>
                    {row.location || "?"}
                  </TableCell>
                  <TableCell align="center">
                    <Chip label={row.status || "Active"} color={row.status === "Resolved" ? "success" : "error"} />
                  </TableCell>
                  <TableCell>
                    {row.time || new Date().toLocaleString()}
                  </TableCell>
                </motion.tr>
              ))}
            </AnimatePresence>
          </TableBody>
        </Table>
      )}
    </Paper>
  );
}
