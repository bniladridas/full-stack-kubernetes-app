import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Grid, 
  Paper, 
  Divider, 
  Box, 
  Chip, 
  LinearProgress,
  Alert
} from '@mui/material';
import { 
  Dashboard as DashboardIcon, 
  Storage as StorageIcon, 
  Memory as MemoryIcon, 
  Computer as ComputerIcon, 
  Security as SecurityIcon 
} from '@mui/icons-material';

import { AppMetadata } from '../types/MetaInterfaces';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const MetadataDashboard: React.FC = () => {
  const [metadata, setMetadata] = useState<AppMetadata | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { token } = useAuth();

  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        if (!token) {
          throw new Error('No authentication token found');
        }

        console.log('Fetching metadata with token:', token.substring(0, 10) + '...');

        const response = await axios.get('/api/auth/metadata', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        console.log('Metadata response:', response.data);
        
        setMetadata(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Metadata fetch error:', error);
        
        if (axios.isAxiosError(error)) {
          const axiosError = error as any;
          if (axiosError.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            setError(`Server Error: ${axiosError.response.status} - ${axiosError.response.data}`);
          } else if (axiosError.request) {
            // The request was made but no response was received
            setError('No response received from server');
          } else {
            // Something happened in setting up the request that triggered an Error
            setError(`Request Setup Error: ${axiosError.message}`);
          }
        } else {
          setError(`Unexpected Error: ${(error as Error).message}`);
        }
        
        setLoading(false);
      }
    };

    fetchMetadata();
  }, [token]);

  if (loading) {
    return <LinearProgress />;
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">
          {error}
        </Alert>
      </Container>
    );
  }

  if (!metadata) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="warning">
          Unable to load metadata. Please try again later.
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* User Information Card */}
        <Grid item xs={12} md={4}>
          <Paper 
            elevation={3} 
            sx={{ 
              p: 3, 
              display: 'flex', 
              flexDirection: 'column',
              height: 300
            }}
          >
            <Typography variant="h6" gutterBottom>
              <DashboardIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              User Profile
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Box>
              <Typography>Username: {metadata.user?.username || 'N/A'}</Typography>
              <Typography>Email: {metadata.user?.email || 'N/A'}</Typography>
              <Chip 
                label={metadata.user?.is_superuser ? 'Admin' : 'User'} 
                color={metadata.user?.is_superuser ? 'primary' : 'default'}
                sx={{ mt: 2 }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* System Diagnostics Card */}
        <Grid item xs={12} md={8}>
          <Paper 
            elevation={3} 
            sx={{ 
              p: 3, 
              display: 'flex', 
              flexDirection: 'column',
              height: 300
            }}
          >
            <Typography variant="h6" gutterBottom>
              <ComputerIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              System Diagnostics
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography>
                  <MemoryIcon sx={{ mr: 1, verticalAlign: 'middle', fontSize: 'small' }} />
                  Memory Usage: {metadata.health?.system_diagnostics.memory.percent_used?.toFixed(2) || 'N/A'}%
                </Typography>
                <Typography>
                  <StorageIcon sx={{ mr: 1, verticalAlign: 'middle', fontSize: 'small' }} />
                  Available Memory: {metadata.health?.system_diagnostics.memory.available ? 
                    (metadata.health.system_diagnostics.memory.available / 1024).toFixed(2) : 'N/A'} GB
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography>
                  <SecurityIcon sx={{ mr: 1, verticalAlign: 'middle', fontSize: 'small' }} />
                  Python Version: {metadata.health?.system_diagnostics.python_version || 'N/A'}
                </Typography>
                <Typography>
                  OS: {metadata.health?.system_diagnostics.os.system || 'N/A'} {metadata.health?.system_diagnostics.os.release || ''}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Application Metadata Card */}
        <Grid item xs={12}>
          <Paper 
            elevation={3} 
            sx={{ 
              p: 3, 
              display: 'flex', 
              flexDirection: 'column' 
            }}
          >
            <Typography variant="h6" gutterBottom>
              Application Details
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography>
                  Name: {metadata.application?.name || 'N/A'}
                </Typography>
                <Typography>
                  Version: {metadata.application?.version || 'N/A'}
                </Typography>
                <Typography>
                  Environment: {metadata.application?.environment || 'N/A'}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography>
                  Build Timestamp: {metadata.application?.build_timestamp ? 
                    new Date(metadata.application.build_timestamp).toLocaleString() : 'N/A'}
                </Typography>
                <Typography>
                  Dependencies: {metadata.application?.dependencies?.join(', ') || 'N/A'}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default MetadataDashboard;
