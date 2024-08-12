import React, { useState, useEffect } from 'react';
import { getProjects, createProject, getAllProjects, joinProject } from '../api';
import { Container, Typography, TextField, Button, List, ListItem, ListItemText, Box, Paper, Select, MenuItem, Alert } from '@mui/material';
import Navbar from './navbar';

const ProjectManagement = ({ onLogout }) => {
  const [projects, setProjects] = useState([]);
  const [allProjects, setAllProjects] = useState([]);
  const [newProject, setNewProject] = useState({ name: '', description: '', projectID: '' });
  const [selectedProject, setSelectedProject] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchProjects();
    fetchAllProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await getProjects();
      setProjects(response.data);
    } catch (error) {
      setError('Error fetching projects');
    }
  };

  const fetchAllProjects = async () => {
    try {
      const response = await getAllProjects();
      setAllProjects(response.data);
    } catch (error) {
      setError('Error fetching all projects');
    }
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      await createProject(newProject);
      setNewProject({ name: '', description: '', projectID: '' });
      fetchProjects();
      fetchAllProjects();
      setSuccess('Project created successfully');
    } catch (error) {
      setError(error.response?.data?.message || 'Error creating project. Project ID may already exist.');
    }
  };

  const handleJoinProject = async () => {
    setError('');
    setSuccess('');
    try {
      await joinProject(selectedProject);
      fetchProjects();
      setSelectedProject('');
      setSuccess('Joined project successfully');
    } catch (error) {
      setError(error.response?.data?.message || 'Error joining project');
    }
  };

  return (
    <>
      <Navbar onLogout={onLogout} />
      <Container maxWidth="md" sx={{ mt: 4 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
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
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" component="h2" gutterBottom>
            Join Existing Project
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Select
              value={selectedProject}
              onChange={(e) => setSelectedProject(e.target.value)}
              displayEmpty
              fullWidth
            >
              <MenuItem value="" disabled>Select a project to join</MenuItem>
              {allProjects.map((project) => (
                <MenuItem key={project._id} value={project._id}>{project.name} (ID: {project.projectID})</MenuItem>
              ))}
            </Select>
            <Button onClick={handleJoinProject} variant="contained" color="secondary" disabled={!selectedProject}>
              Join Project
            </Button>
          </Box>
        </Paper>
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" component="h2" gutterBottom>
            Your Projects
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