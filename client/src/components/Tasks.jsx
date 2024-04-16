// Tasks.jsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    fetch('/tasks')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch tasks');
        }
        return response.json();
      })
      .then(data => {
        setTasks(data); 
        console.log(data)
      })
      .catch(error => {
        console.log('Error fetching tasks:');
      });
  }, []);

  return (
    <div>
      <h1>All Tasks</h1>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>
            <Link to={`/tasks/${task.id}`}>{task.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Tasks;
