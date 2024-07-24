import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Container } from '@mui/material';

import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import ProjectManagement from './components/ProjectManagement';
import ResourceManagement from './components/ResourceManagement';

const theme = createTheme();

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('token');
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Container>
          <Switch>
            <Route exact path="/">
              {isAuthenticated ? <Redirect to="/dashboard" /> : <Redirect to="/login" />}
            </Route>
            <Route path="/login">
              <Login onLogin={handleLogin} />
            </Route>
            <Route path="/register">
              <Register />
            </Route>
            <Route path="/dashboard">
              {isAuthenticated ? <Dashboard onLogout={handleLogout} /> : <Redirect to="/login" />}
            </Route>
            <Route path="/projects">
              {isAuthenticated ? <ProjectManagement /> : <Redirect to="/login" />}
            </Route>
            <Route path="/resources">
              {isAuthenticated ? <ResourceManagement /> : <Redirect to="/login" />}
            </Route>
          </Switch>
        </Container>
      </Router>
    </ThemeProvider>
  );
};

export default App;