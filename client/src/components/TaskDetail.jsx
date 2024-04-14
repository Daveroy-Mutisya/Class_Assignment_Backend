// TaskDetail.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const TaskDetail = () => {
  const { taskId } = useParams();
  const [task, setTask] = useState(null);

  useEffect(() => {
    fetch(`/tasks/${taskId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to fetch task with ID ${taskId}`);
        }
        return response.json();
      })
      .then(data => {
        setTask(data);
      })
      .catch(error => {
        console.error(`Error fetching task with ID ${taskId}:`, error);
      });
  }, [taskId]);

  if (!task) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{task.title}</h1>
      <p>Description: {task.description}</p>
      <p>Due Date: {task.due_date}</p>
      {/* Add more details as needed */}
    </div>
  );
};

export default TaskDetail;
