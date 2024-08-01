import React, { useState, useEffect } from 'react';
import { getProjects, createProject } from '../api';

const ProjectManagement = () => {
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
    <div>
      <h2>Project Management</h2>
      <form onSubmit={handleCreateProject}>
        <input
          type="text"
          placeholder="Project Name"
          value={newProject.name}
          onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Description"
          value={newProject.description}
          onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
        />
        <input
          type="text"
          placeholder="Project ID"
          value={newProject.projectID}
          onChange={(e) => setNewProject({ ...newProject, projectID: e.target.value })}
        />
        <button type="submit">Create Project</button>
      </form>
      <ul>
        {projects.map(project => (
          <li key={project._id}>{project.name} - {project.description}</li>
        ))}
      </ul>
    </div>
  );
};

export default ProjectManagement;