import React, { useState, useEffect } from 'react';
import { 
  Typography, Box, Button, TextField, List, ListItem, 
  ListItemText, Paper, Grid 
} from '@mui/material';
import { getProjects, createProject, getResources, checkoutResources, checkinResources } from '../api';

const Dashboard = ({ onLogout }) => {
  const [projects, setProjects] = useState([]);
  const [newProject, setNewProject] = useState({ name: '', description: '', projectID: '' });
  const [resources, setResources] = useState([]);
  const [checkout, setCheckout] = useState({ hw_set: '', quantity: 0 });

  useEffect(() => {
    fetchProjects();
    fetchResources();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await getProjects();
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const fetchResources = async () => {
    try {
      const response = await getResources();
      setResources(response.data);
    } catch (error) {
      console.error('Error fetching resources:', error);
    }
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();
    try {
      await createProject(newProject);
      setNewProject({ name: '', description: '', projectID: '' });
      fetchProjects();
    } catch (error) {
      console.error('Error creating project:', error);
    }
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    try {
      await checkoutResources(checkout);
      setCheckout({ hw_set: '', quantity: 0 });
      fetchResources();
    } catch (error) {
      console.error('Error checking out resources:', error);
    }
  };

  const handleCheckin = async (e) => {
    e.preventDefault();
    try {
      await checkinResources(checkout);
      setCheckout({ hw_set: '', quantity: 0 });
      fetchResources();
    } catch (error) {
      console.error('Error checking in resources:', error);
    }
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Button onClick={onLogout} variant="contained" color="secondary" sx={{ mb: 2 }}>
        Logout
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Project Management
            </Typography>
            <form onSubmit={handleCreateProject}>
              <TextField
                fullWidth
                label="Project Name"
                value={newProject.name}
                onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Project Description"
                value={newProject.description}
                onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Project ID"
                value={newProject.projectID}
                onChange={(e) => setNewProject({ ...newProject, projectID: e.target.value })}
                margin="normal"
              />
              <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
                Create Project
              </Button>
            </form>
            <List>
              {projects.map((project) => (
                <ListItem key={project._id}>
                  <ListItemText 
                    primary={project.name} 
                    secondary={`${project.description} (ID: ${project.projectID})`} 
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Resource Management
            </Typography>
            <form onSubmit={handleCheckout}>
              <TextField
                fullWidth
                label="Hardware Set"
                value={checkout.hw_set}
                onChange={(e) => setCheckout({ ...checkout, hw_set: e.target.value })}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Quantity"
                type="number"
                value={checkout.quantity}
                onChange={(e) => setCheckout({ ...checkout, quantity: parseInt(e.target.value) })}
                margin="normal"
              />
              <Button type="submit" variant="contained" color="primary" sx={{ mt: 2, mr: 2 }}>
                Checkout
              </Button>
              <Button onClick={handleCheckin} variant="contained" color="secondary" sx={{ mt: 2 }}>
                Check-in
              </Button>
            </form>
            <List>
              {resources.map((resource) => (
                <ListItem key={resource._id}>
                  <ListItemText 
                    primary={resource.name} 
                    secondary={`Available: ${resource.available}, Capacity: ${resource.capacity}`} 
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;