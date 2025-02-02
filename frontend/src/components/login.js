import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, Typography, Box, Container, Tab, Tabs, Alert } from '@mui/material';
import { login, register } from '../api';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (isLogin) {
        const response = await login(username, password);
        localStorage.setItem('token', response.data.access_token);
        onLogin();
        navigate('/dashboard');
      } else {
        await register(username, password);
        setIsLogin(true);
        setError('Registration successful. Please log in.');
      }
    } catch (error) {
      console.error(isLogin ? 'Login failed:' : 'Registration failed:', error);
      setError(error.response?.data?.message || 'An error occurred. Please try again.');
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h5">
          HaaS PoC
        </Typography>
        <Tabs value={isLogin ? 0 : 1} onChange={(_, newValue) => setIsLogin(newValue === 0)}>
          <Tab label="Login" />
          <Tab label="Register" />
        </Tabs>
        {error && <Alert severity="error" sx={{ mt: 2, width: '100%' }}>{error}</Alert>}
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            {isLogin ? 'Sign In' : 'Register'}
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default Login;