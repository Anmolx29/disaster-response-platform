import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid } from 'recharts';
import axios from 'axios';

export default function IncidentTrendsChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/incidents")
      .then(res => {
        // Group by disaster_type
        const grouped = {};
        res.data.forEach(inc => {
          const type = inc.disaster_type || "Unknown";
          grouped[type] = (grouped[type] || 0) + 1;
        });
        setData(Object.keys(grouped).map(key => ({ type: key, count: grouped[key] })));
      });
  }, []);

  return (
    <div style={{ height: 340, width: "100%", margin: "38px auto", background: "#f8f9fc", borderRadius: 16, boxShadow: "0 0 12px #2263" }}>
      <h3 style={{ textAlign: "center", margin: 0, padding: 14, color: "#165CAE" }}>Incident Volume by Disaster Type</h3>
      <ResponsiveContainer width="95%" height={260}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="type" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#176cff" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
