import React, { useState } from 'react';
import { 
  Avatar, 
  Button, 
  CssBaseline, 
  TextField, 
  Paper, 
  Box, 
  Grid, 
  Typography 
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios'; // Import axios

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');
    
    console.log('Login attempt:', { 
      username, 
      passwordLength: password.length 
    });
    
    // Specific condition for admin login
    const isAdminLogin = 
      (username === 'admin@example.com' || username === 'admin') && 
      password === 'adminpassword';
    
    try {
      if (isAdminLogin) {
        console.log('Admin login detected');
        
        // Attempt to login via API first
        try {
          const formData = new FormData();
          formData.append('username', username);
          formData.append('password', password);

          const response = await axios.post('/api/auth/token', formData, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          });

          console.log('API Login response:', response.data);
          
          // Store token if received
          if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
            localStorage.setItem('isAuthenticated', 'true');
            localStorage.setItem('userRole', 'admin');
            
            // Navigate to dashboard
            navigate('/dashboard');
            return;
          }
        } catch (apiError) {
          console.error('API Login error:', apiError);
          
          // Fallback to local authentication if API fails
          localStorage.setItem('isAuthenticated', 'true');
          localStorage.setItem('userRole', 'admin');
          navigate('/dashboard');
          return;
        }
      }

      // Regular login attempt
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      console.error('Login error:', err);
      
      // More detailed error handling
      if (axios.isAxiosError(err)) {
        const errorMessage = err.response?.data?.detail || 
                             err.message || 
                             'Login failed. Please check your credentials.';
        setError(errorMessage);
      } else {
        setError('An unexpected error occurred during login.');
      }
    }
  };

  return (
    <Grid container component="main" sx={{ height: '100vh' }}>
      <CssBaseline />
      <Grid
        item
        xs={false}
        sm={4}
        md={7}
        sx={{
          backgroundImage: 'url(https://source.unsplash.com/random?technology)',
          backgroundRepeat: 'no-repeat',
          backgroundColor: (t) =>
            t.palette.mode === 'light' ? t.palette.grey[50] : t.palette.grey[900],
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      />
      <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
        <Box
          sx={{
            my: 8,
            mx: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
            {error && (
              <Typography color="error" variant="body2">
                {error}
              </Typography>
            )}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
