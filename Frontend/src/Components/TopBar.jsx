import React from 'react';

const TopBar = () => {
  // Define styles
  const styles = {
    topBar: {
      position: 'fixed',
      top: 0,
      left: '18rem', // Starts where the sidebar ends
      right: 0,
      height: '4rem',
      backgroundColor: '#101525', // <-- UPDATED to Deep Midnight Blue
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
      zIndex: 20,
      display: 'flex',
      justifyContent: 'flex-end',
      alignItems: 'center',
      padding: '0 1.5rem',
    },
    profile: {
      display: 'flex',
      alignItems: 'center',
      cursor: 'pointer',
    },
    // User Name Text Color changed to White for contrast
    userName: {
      fontSize: '1rem',
      color: '#fff', // <-- UPDATED Text color
    },
    // Avatar remains Teal accent color
    avatar: {
      width: '2.25rem',
      height: '2.25rem',
      borderRadius: '50%',
      backgroundColor: '#18B097', // Teal Accent Color
      color: '#fff',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      fontSize: '1rem',
      fontWeight: 'bold',
      marginLeft: '0.75rem',
    }
  };

  return (
    <header style={styles.topBar}>
      <div style={styles.profile}>
        <span style={styles.userName}>Welcome, **User**</span>
        <div style={styles.avatar}>
          W
        </div>
      </div>
    </header>
  );
};

export default TopBar;