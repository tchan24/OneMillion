import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Container, Typography, Button, List, ListItem, ListItemText, AppBar, Toolbar } from '@mui/material';
import { getProjects, getResources } from '../api';

const Dashboard = ({ onLogout }) => {
  const [projects, setProjects] = useState([]);
  const [resources, setResources] = useState([]);

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

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Dashboard
          </Typography>
          <Button color="inherit" component={Link} to="/projects">Projects</Button>
          <Button color="inherit" component={Link} to="/resources">Resources</Button>
          <Button color="inherit" onClick={onLogout}>Logout</Button>
        </Toolbar>
      </AppBar>
      <Container>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          Projects
        </Typography>
        <List>
          {projects.map(project => (
            <ListItem key={project._id}>
              <ListItemText primary={project.name} secondary={project.description} />
            </ListItem>
          ))}
        </List>
        <Typography variant="h5" component="h2" gutterBottom>
          Resources
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
      </Container>
    </>
  );
};

export default Dashboard;