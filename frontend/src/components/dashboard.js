import React, { useState, useEffect } from 'react';
   import { getProjects, getResources } from '../api';

   const Dashboard = () => {
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
       <div>
         <h1>Dashboard</h1>
         <h2>Projects</h2>
         <ul>
           {projects.map(project => (
             <li key={project._id}>{project.name} - {project.description}</li>
           ))}
         </ul>
         <h2>Resources</h2>
         <ul>
           {resources.map(resource => (
             <li key={resource._id}>{resource.name} - Available: {resource.available}/{resource.capacity}</li>
           ))}
         </ul>
       </div>
     );
   };

   export default Dashboard;