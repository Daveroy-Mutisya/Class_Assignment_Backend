// SubtaskDetail.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const SubtaskDetail = () => {
  const { taskId, subtaskId } = useParams();
  const [subtask, setSubtask] = useState(null);

  useEffect(() => {
    fetch(`/tasks/${taskId}/subtasks/${subtaskId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to fetch subtask with ID ${subtaskId} for task ${taskId}`);
        }
        return response.json();
      })
      .then(data => {
        setSubtask(data);
      })
      .catch(error => {
        console.error(`Error fetching subtask with ID ${subtaskId} for task ${taskId}:`, error);
      });
  }, [taskId, subtaskId]);

  if (!subtask) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{subtask.title}</h1>
      {/* Add more details as needed */}
    </div>
  );
};

export default SubtaskDetail;
