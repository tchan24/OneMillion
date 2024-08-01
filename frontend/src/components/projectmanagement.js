import React, { useState, useEffect } from 'react';
import { getProjects, createProject } from '../api';
import { Container, Typography, TextField, Button, List, ListItem, ListItemText, Box, Paper } from '@mui/material';
import Navbar from './navbar';

const ProjectManagement = ({ onLogout }) => {
  const [projects, setProjects] = useState([]);
  const [newProject, setNewProject] = useState({ name: '', description: '', projectID: '' });

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await getProjects();
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
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

  return (
    <>
      <Navbar onLogout={onLogout} />
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Project Management
        </Typography>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" component="h2" gutterBottom>
            Create New Project
          </Typography>
          <Box component="form" onSubmit={handleCreateProject} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Project Name"
              variant="outlined"
              value={newProject.name}
              onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
              required
            />
            <TextField
              label="Description"
              variant="outlined"
              value={newProject.description}
              onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
              required
            />
            <TextField
              label="Project ID"
              variant="outlined"
              value={newProject.projectID}
              onChange={(e) => setNewProject({ ...newProject, projectID: e.target.value })}
              required
            />
            <Button type="submit" variant="contained" color="primary">
              Create Project
            </Button>
          </Box>
        </Paper>
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" component="h2" gutterBottom>
            Existing Projects
          </Typography>
          <List>
            {projects.map(project => (
              <ListItem key={project._id}>
                <ListItemText 
                  primary={project.name} 
                  secondary={`${project.description} (ID: ${project.projectID})`} 
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      </Container>
    </>
  );
};

export default ProjectManagement;