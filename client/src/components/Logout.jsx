// Logout.jsx
import React from 'react';

const Logout = () => {
  const handleLogout = async () => {
    try {
      const response = await fetch('/logout');

      if (!response.ok) {
        throw new Error('Failed to logout');
      }

      console.log('User logged out successfully');
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return (
    <div>
      <h2>Logout</h2>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Logout;
