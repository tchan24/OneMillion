import React, { useState } from 'react';
import { TextField, Button, Typography, Box } from '@mui/material';
import { login, register } from '../api';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log('Attempting to', isLogin ? 'login' : 'register');
      console.log('Username:', username);
      console.log('Password:', password);
      
      const response = isLogin
        ? await login(username, password)
        : await register(username, password);
      
      console.log('Response:', response);
      
      localStorage.setItem('token', response.data.access_token);
      onLogin();
    } catch (error) {
      console.error('Authentication error:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
      }
      alert('Authentication failed. Please check the console for more details.');
    }
  };

  return (
    <Box
      sx={{
        marginTop: 8,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <Typography component="h1" variant="h5">
        {isLogin ? 'Sign In' : 'Register'}
      </Typography>
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
        <Button
          fullWidth
          onClick={() => setIsLogin(!isLogin)}
        >
          {isLogin ? 'Need to register?' : 'Already have an account?'}
        </Button>
      </Box>
    </Box>
  );
};

export default Login;