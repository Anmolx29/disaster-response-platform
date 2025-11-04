import React, { useState } from 'react';
import { Box, Button, TextField, Typography, Paper, Alert } from '@mui/material';
import axios from 'axios';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const form = new FormData();
      form.append('username', username);
      form.append('password', password);
      const resp = await axios.post('http://localhost:8000/token', form, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      localStorage.setItem('token', resp.data.access_token);
      if (onLogin) onLogin(resp.data.access_token);
    } catch (e) {
      setError("Login failed - please check your credentials.");
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Paper elevation={6} sx={{ p: 4, minWidth: 340 }}>
        <Typography variant="h5" sx={{ mb: 2, fontWeight: 700 }}>Login</Typography>
        {error && <Alert severity="error">{error}</Alert>}
        <form onSubmit={handleLogin}>
          <TextField
            fullWidth label="Username" value={username} onChange={e => setUsername(e.target.value)} sx={{ mb: 2 }} required
          />
          <TextField
            fullWidth type="password" label="Password" value={password} onChange={e => setPassword(e.target.value)} sx={{ mb: 2 }} required
          />
          <Button fullWidth type="submit" variant="contained">Login</Button>
        </form>
      </Paper>
    </Box>
  );
}
