import React, { useState, useEffect } from 'react';
import { getResources, checkoutResources, checkinResources, getProjectResources, getProjects } from '../api';
import { Container, Typography, TextField, Button, List, ListItem, ListItemText, Box, Paper, Alert, Select, MenuItem } from '@mui/material';
import Navbar from './navbar';

const ResourceManagement = ({ onLogout }) => {
  const [resources, setResources] = useState([]);
  const [checkoutData, setCheckoutData] = useState({ hw_set: '', quantity: 0, project_id: '' });
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState('');
  const [projectResources, setProjectResources] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchResources();
    fetchProjects();
  }, []);

  useEffect(() => {
    if (selectedProject) {
      fetchProjectResources(selectedProject);
    }
  }, [selectedProject]);

  const fetchResources = async () => {
    try {
      const response = await getResources();
      setResources(response.data);
    } catch (error) {
      setError('Error fetching resources');
    }
  };

  const fetchProjects = async () => {
    try {
      const response = await getProjects();
      setProjects(response.data);
    } catch (error) {
      setError('Error fetching projects');
    }
  };

  const fetchProjectResources = async (projectId) => {
    try {
      const response = await getProjectResources(projectId);
      setProjectResources(response.data);
    } catch (error) {
      setError('Error fetching project resources');
    }
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    try {
      await checkoutResources(checkoutData.hw_set, checkoutData.quantity, selectedProject);
      setCheckoutData({ hw_set: '', quantity: 0 });
      fetchResources();
      fetchProjectResources(selectedProject);
      showAlert('Resources checked out successfully', 'success');
    } catch (error) {
      console.error('Error checking out resource:', error);
      showAlert(error.response?.data?.message || 'Error checking out resource. Insufficient quantity may be available.', 'error');
    }
  };

  const handleCheckin = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      await checkinResources(checkoutData.hw_set, checkoutData.quantity, selectedProject);
      setCheckoutData({ hw_set: '', quantity: 0 });
      fetchResources();
      fetchProjectResources(selectedProject);
      setSuccess('Resources checked in successfully');
    } catch (error) {
      setError(error.response?.data?.message || 'Error checking in resources');
    }
  };

  return (
    <>
      <Navbar onLogout={onLogout} />
      <Container maxWidth="md" sx={{ mt: 4 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
        <Typography variant="h4" component="h1" gutterBottom>
          Resource Management
        </Typography>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" component="h2" gutterBottom>
            Available Resources
          </Typography>
          <List>
            {resources.map(resource => (
              <ListItem key={resource.id}>
                <ListItemText 
                  primary={resource.name} 
                  secondary={`Available: ${resource.available}/${resource.capacity}`} 
                />
              </ListItem>
            ))}
          </List>
        </Paper>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" component="h2" gutterBottom>
            Checkout/Check-in Resources
          </Typography>
          <Box component="form" onSubmit={handleCheckout} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Select
              value={selectedProject}
              onChange={(e) => setSelectedProject(e.target.value)}
              displayEmpty
              fullWidth
              required
            >
              <MenuItem value="" disabled>Select a project</MenuItem>
              {projects.map((project) => (
                <MenuItem key={project._id} value={project._id}>{project.name}</MenuItem>
              ))}
            </Select>
            <Select
              value={checkoutData.hw_set}
              onChange={(e) => setCheckoutData({ ...checkoutData, hw_set: e.target.value })}
              displayEmpty
              fullWidth
              required
            >
              <MenuItem value="" disabled>Select a hardware set</MenuItem>
              {resources.map((resource) => (
                <MenuItem key={resource.id} value={resource.name}>{resource.name}</MenuItem>
              ))}
            </Select>
            <TextField
              label="Quantity"
              type="number"
              variant="outlined"
              value={checkoutData.quantity}
              onChange={(e) => setCheckoutData({ ...checkoutData, quantity: parseInt(e.target.value) })}
              required
            />
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Button type="submit" variant="contained" color="primary">
                Checkout
              </Button>
              <Button onClick={handleCheckin} variant="contained" color="secondary">
                Check In
              </Button>
            </Box>
          </Box>
        </Paper>
        {selectedProject && (
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6" component="h2" gutterBottom>
              Project Resources
            </Typography>
            <List>
              {projectResources.map(resource => (
                <ListItem key={resource.name}>
                  <ListItemText 
                    primary={resource.name} 
                    secondary={`Checked out: ${resource.checked_out}`} 
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        )}
      </Container>
    </>
  );
};

export default ResourceManagement;