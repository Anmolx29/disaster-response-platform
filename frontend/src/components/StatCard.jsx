import React from 'react';
import { Paper, Typography, Avatar } from '@mui/material';
import { motion } from 'framer-motion';

export default function StatCard({ label, value, icon, img, color }) {
  return (
    <motion.div
      whileHover={{ scale: 1.08, boxShadow: "0 8px 40px rgba(60,60,210,0.18)" }}
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Paper elevation={4} sx={{
        padding: 3, textAlign: "center", borderRadius: 3,
        background: `linear-gradient(145deg, ${color}20 0%, #fff 100%)`,
        boxShadow: "0 4px 24px 0 rgba(16, 40, 80, 0.08)",
        position: "relative"
      }}>
        <Avatar
          src={img}
          alt={label}
          sx={{
            mb: 1, mx: "auto", width: 72, height: 72,
            border: `4px solid ${color}70`
          }}
        >{icon}</Avatar>
        <Typography variant="h6" color="primary" sx={{color}}>
          {label}
        </Typography>
        <Typography variant="h3" sx={{ fontWeight: 900, mt: 0.5, color: "#232323" }}>
          {value}
        </Typography>
      </Paper>
    </motion.div>
  );
}
