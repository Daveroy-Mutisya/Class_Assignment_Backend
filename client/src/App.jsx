import React from 'react';
import { BrowserRouter as Router, Route ,Routes } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import Logout from './components/Logout';
import Tasks from './components/Tasks';
import TaskDetail from './components/TaskDetail';
import SubtaskDetail from './components/SubtaskDetail';
import Home from './components/Home'; 
function App() {
  return (
    
    <Router>
      <Routes>
        <Route path="/register" element={<Register/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/logout" element={<Logout/>} />
        <Route path="/tasks/:taskId/subtasks/:subtaskId" element={<SubtaskDetail/>} />
        <Route path="/tasks/:taskId" element={<TaskDetail/>} />
        <Route path="/tasks" element= {<Tasks/>} />
        <Route path="/" component={<Home/>} /> {/* Set Home component as the default route */}
      </Routes>
    </Router>
  );
}

export default App;
