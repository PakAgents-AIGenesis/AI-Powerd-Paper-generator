import React, { useState } from 'react';

const Sidebar = ({ activeLink, setActiveLink }) => {
  const [hoveredLink, setHoveredLink] = useState(null);

  // *** IMPORTANT: REPLACE THIS with the actual path to your logo image ***
  const LOGO_SRC = "./src/assets/hack-logo.png"; 
  // *******************************************************************

  const styles = {
    sidebar: {
      width: '18rem',
      height: '100vh', 
      backgroundColor: '#101525', // Deep Dark Blue Sidebar color
      padding: '0 0 1.5rem 0', 
      position: 'fixed',
      top: 0, 
      left: 0,
      display: 'flex',
      flexDirection: 'column',
      color: '#fff',
      zIndex: 10,
    },
    logo: {
      padding: '0.5rem 1.5rem', 
      backgroundColor: '#101525', // MATCHES TopBar background
      borderBottom: '1px solid rgba(16, 21, 37, 0.5)', 
      marginBottom: '0.5rem',
      height: '4rem', 
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'flex-start',
    },
    logoImage: {
        maxHeight: '3rem', 
        width: 'auto',
        objectFit: 'contain',
    },
    
    // --- NEW STYLES FOR ANIMATION ---
    // 1. Outer container (for horizontal padding and click area)
    linkOuter: { 
      padding: '0 1.5rem', // Horizontal padding applied here
      color: '#A9B4D5', // Base text color
      textDecoration: 'none',
      fontSize: '1rem',
      fontWeight: 500,
      cursor: 'pointer',
      marginBottom: '0.4rem', // Space between links
    },
    
    // 2. Inner element (the part that moves and changes color/shadow)
    innerLinkBase: {
      display: 'flex',
      alignItems: 'center',
      padding: '0.75rem 1rem', // Padding inside the rounded box
      // Smooth 3D transition for all effects
      transition: 'all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94)', 
      borderRadius: '8px', // Rounded corners
      transform: 'translateY(0)', // Base position
    },
    
    
    // 3. Effect applied on hover or active (Teal background + 3D lift)
    innerLinkEffect: {
        backgroundColor: '#18B097', // Teal Accent Color
        color: '#fff',
        // 3D Lift Effect using box-shadow and translation/scale
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.3)', 
        transform: 'translateY(-2px) scale(1.02)', // Pop and lift effect
    },
    // --- END NEW STYLES ---

    iconSpace: {
      marginRight: '0.75rem',
    },
    utilitySection: {
        marginTop: 'auto', 
        borderTop: '1px solid rgba(255, 255, 255, 0.1)', 
        paddingTop: '0.5rem',
        marginBottom: '0.5rem', 
    },
    footerText: {
        padding: '0 1.5rem 1rem 1.5rem', 
        fontSize: '0.75rem',
        color: '#A9B4D5',
    }
  };

  const navItems = [
    { id: 'generate', name: 'Generate Your Paper', icon: '📄' },
    { id: 'saved', name: 'My Saved Papers', icon: '📚' },
    { id: 'settings', name: 'Settings', icon: '⚙️' },
  ];

  const utilityItems = [
    { id: 'about', name: 'About', icon: 'ⓘ' },
    { id: 'signup', name: 'Sign Up / Login', icon: '👤' },
  ];

  // Function now calculates the dynamic style for the inner animated element
  const getInnerLinkStyle = (itemId, isUtility = false) => {
    let style = styles.innerLinkBase;
    const currentActiveLink = isUtility ? null : activeLink; 
    
    // Apply the 3D effect if hovered OR if it is the active link
    if (hoveredLink === itemId || currentActiveLink === itemId) {
      style = { ...style, ...styles.innerLinkEffect };
      style.color = '#fff'; // Force white text when active/hovered
    } else {
        style.color = styles.linkOuter.color; // Base text color when inactive/not hovered
    }
    
    return style;
  };

  return (
    <div style={styles.sidebar}>
      
      {/* 1. Logo Section */}
      <div style={styles.logo}>
        <img 
            src={LOGO_SRC} 
            alt="Paper Generator Logo"
            style={styles.logoImage}
        />
      </div>
      
      {/* 2. Main Navigation Links */}
      <nav 
        style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          flexGrow: 1, 
          paddingTop: '1rem', 
        }}
      >
        {navItems.map((item) => (
          // OUTER DIV: Handles padding and events
          <div
            key={item.id}
            style={styles.linkOuter}
            onClick={() => setActiveLink(item.id)}
            onMouseEnter={() => setHoveredLink(item.id)}
            onMouseLeave={() => setHoveredLink(null)}
          >
            {/* INNER DIV: Handles the rounded corners, color, and 3D animation */}
            <div style={getInnerLinkStyle(item.id)}> 
              <span style={styles.iconSpace}>{item.icon}</span>
              {item.name}
            </div>
          </div>
        ))}
      </nav>
      
      {/* 3. Utility Section (About and Sign Up) */}
      <div style={styles.utilitySection}>
        {utilityItems.map((item) => (
            <div
                key={item.id}
                style={styles.linkOuter}
                onClick={() => setActiveLink(item.id)}
                onMouseEnter={() => setHoveredLink(item.id)}
                onMouseLeave={() => setHoveredLink(null)}
            >
                {/* INNER DIV for Utility links */}
                <div style={getInnerLinkStyle(item.id, true)}>
                    <span style={styles.iconSpace}>{item.icon}</span>
                    {item.name}
                </div>
            </div>
        ))}
      </div>

      {/* 4. Static Footer Text */}
      <div style={styles.footerText}>
        AI to generate automatically.
      </div>
    </div>
  );
};

export default Sidebar;