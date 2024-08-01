import React, { useState, useEffect } from 'react';
import { getResources, addResource, checkoutResources, checkinResources } from '../api';
import { Container, Typography, TextField, Button, List, ListItem, ListItemText, Box, Paper } from '@mui/material';
import Navbar from './navbar';

const ResourceManagement = ({ onLogout }) => {
  const [resources, setResources] = useState([]);
  const [newResource, setNewResource] = useState({ name: '', capacity: 0 });
  const [checkoutData, setCheckoutData] = useState({ hw_set: '', quantity: 0 });

  useEffect(() => {
    fetchResources();
  }, []);

  const fetchResources = async () => {
    try {
      const response = await getResources();
      setResources(response.data);
    } catch (error) {
      console.error('Error fetching resources:', error);
    }
  };

  const handleAddResource = async (e) => {
    e.preventDefault();
    try {
      await addResource(newResource);
      setNewResource({ name: '', capacity: 0 });
      fetchResources();
    } catch (error) {
      console.error('Error adding resource:', error);
    }
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    try {
      await checkoutResources(checkoutData.hw_set, checkoutData.quantity);
      setCheckoutData({ hw_set: '', quantity: 0 });
      fetchResources();
    } catch (error) {
      console.error('Error checking out resource:', error);
    }
  };

  const handleCheckin = async (e) => {
    e.preventDefault();
    try {
      await checkinResources(checkoutData.hw_set, checkoutData.quantity);
      setCheckoutData({ hw_set: '', quantity: 0 });
      fetchResources();
    } catch (error) {
      console.error('Error checking in resource:', error);
    }
  };

  return (
    <>
      <Navbar onLogout={onLogout} />
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Resource Management
        </Typography>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" component="h2" gutterBottom>
            Add New Resource
          </Typography>
          <Box component="form" onSubmit={handleAddResource} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Resource Name"
              variant="outlined"
              value={newResource.name}
              onChange={(e) => setNewResource({ ...newResource, name: e.target.value })}
              required
            />
            <TextField
              label="Capacity"
              type="number"
              variant="outlined"
              value={newResource.capacity}
              onChange={(e) => setNewResource({ ...newResource, capacity: parseInt(e.target.value) })}
              required
            />
            <Button type="submit" variant="contained" color="primary">
              Add Resource
            </Button>
          </Box>
        </Paper>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" component="h2" gutterBottom>
            Checkout/Check-in Resources
          </Typography>
          <Box component="form" onSubmit={handleCheckout} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Hardware Set"
              variant="outlined"
              value={checkoutData.hw_set}
              onChange={(e) => setCheckoutData({ ...checkoutData, hw_set: e.target.value })}
              required
            />
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
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" component="h2" gutterBottom>
            Available Resources
          </Typography>
          <List>
            {resources.map(resource => (
              <ListItem key={resource._id}>
                <ListItemText 
                  primary={resource.name} 
                  secondary={`Available: ${resource.available}/${resource.capacity}`} 
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      </Container>
    </>
  );
};

export default ResourceManagement;