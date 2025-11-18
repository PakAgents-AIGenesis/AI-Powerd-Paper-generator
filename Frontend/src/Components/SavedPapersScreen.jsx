import React, { useState, useEffect } from 'react';

// --- 1. Custom Hook for Media Queries (FIXED to avoid synchronous setState) ---
const useMediaQuery = (query) => {
  // FIX: Initialize state using the functional form of useState. 
  // This ensures the initial value is set correctly on the first render 
  // without causing a cascading render from within useEffect.
  const [matches, setMatches] = useState(() => {
    if (typeof window !== 'undefined') {
      return window.matchMedia(query).matches;
    }
    return false;
  });

  useEffect(() => {
    const media = window.matchMedia(query);
    
    // The previous synchronous setMatches(media.matches); call is removed.

    // Define the listener function 
    const listener = (event) => setMatches(event.matches); 

    // Attach listener directly to the media query object
    media.addEventListener('change', listener); 
    
    // Clean up
    return () => media.removeEventListener('change', listener);
  }, [query]); 

  return matches;
};

// --- 2. Dummy Data (Unchanged) ---
const dummySavedPapers = [
  { id: 1, title: "Math Quiz - Easy", level: "Easy", date: "2025-10-20" },
  { id: 2, title: "Physics Final Exam - Hard", level: "Hard", date: "2025-10-25" },
  { id: 3, title: "Chemistry Midterm - Medium", level: "Medium", date: "2025-11-01" },
  { id: 4, title: "Biology Paper 1 - Easy", level: "Easy", date: "2025-11-10" },
];

// --- 3. Inline Styles (Unchanged) ---
const primaryTeal = '#008080'; // Dark Teal for contrast
const softGlow = 'rgba(0, 128, 128, 0.2)'; // Very subtle glow
const lightBackground = '#FFFFFF'; // White Background
const cardBackground = '#F5F5F5'; // Off-white/Light Gray for cards
const darkText = '#333333'; // Dark text color

const styles = {
  // Base Styles
  container: {
    padding: '40px',
    backgroundColor: lightBackground, // <<< WHITE BACKGROUND
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    fontFamily: 'Arial, sans-serif',
  },
  
  // Navigation Boxes
  navContainer: {
    display: 'flex',
    gap: '30px',
    marginBottom: '40px',
    width: '80%',
    maxWidth: '800px',
  },
  navBoxBase: {
    flex: '1',
    padding: '30px 20px',
    borderRadius: '12px',
    textAlign: 'center',
    cursor: 'pointer',
    backgroundColor: cardBackground,
    color: primaryTeal,
    border: `2px solid ${primaryTeal}`,
    transition: 'all 0.3s ease-in-out',
    boxShadow: `0 0 5px ${softGlow}`, 
  },
  
  // Active Navigation Box (Subtle highlight on white)
  navBoxActive: {
    backgroundColor: 'rgba(0, 128, 128, 0.1)', // Very light teal tint
    color: darkText, 
    transform: 'translateY(-3px) scale(1.01)', 
    boxShadow: `
      0 3px 10px rgba(0, 0, 0, 0.1), 
      0 0 10px ${primaryTeal}
    `, // Subtle shadow and teal outer glow
    border: `2px solid ${primaryTeal}`,
  },
  navTitle: {
    margin: 0,
    fontSize: '18px',
    fontWeight: '600',
    textShadow: `0 0 1px ${primaryTeal}`,
  },
  
  // Main Content Box
  contentBox: {
    width: '90%',
    maxWidth: '1100px',
    padding: '30px',
    borderRadius: '15px',
    backgroundColor: lightBackground,
    border: `1px solid ${primaryTeal}`,
    boxShadow: `0 0 10px rgba(0, 0, 0, 0.1)`, // Clean, simple shadow
  },
  
  // General
  title: {
    color: primaryTeal,
    textAlign: 'center',
    marginBottom: '25px',
    borderBottom: `1px solid ${softGlow}`,
    paddingBottom: '10px',
    textShadow: 'none', // Removed text shadow for cleanliness
  },

  // Buttons
  actionButton: {
    padding: '10px 25px',
    borderRadius: '20px',
    fontSize: '15px',
    cursor: 'pointer',
    backgroundColor: primaryTeal, // Dark teal button
    color: lightBackground, // White text
    fontWeight: 'bold',
    border: 'none',
    boxShadow: `0 3px 8px ${softGlow}`,
    transition: 'all 0.2s',
    margin: '0 10px',
  },
  actionButtonHover: {
    backgroundColor: '#006666', // Slightly darker teal on hover
    boxShadow: `0 5px 12px rgba(0, 0, 0, 0.15)`,
  },
  
  // Generated Paper Preview Specific
  previewContent: {
    color: darkText, // Dark text on light background
    backgroundColor: lightBackground,
    padding: '20px',
    borderRadius: '8px',
    minHeight: '350px',
    fontSize: '14px',
    whiteSpace: 'pre-wrap',
    border: `1px solid ${cardBackground}`,
    lineHeight: '1.6',
    overflowY: 'auto',
  },
  
  // Saved Papers List Specific
  statsContainer: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '25px',
    gap: '20px',
  },
  statBox: {
    flex: '1',
    backgroundColor: cardBackground,
    padding: '15px',
    borderRadius: '8px',
    textAlign: 'center',
    color: darkText,
    border: `1px solid ${softGlow}`,
    boxShadow: `0 0 5px ${softGlow}`,
  },
  statCount: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: primaryTeal,
    textShadow: 'none',
  },
  statLabel: {
    fontSize: '12px',
    marginTop: '5px',
    color: '#888888',
  },
  
  // Search Bar
  searchBar: {
    width: '100%',
    padding: '12px',
    marginBottom: '20px',
    borderRadius: '20px',
    border: `1px solid ${primaryTeal}`,
    backgroundColor: lightBackground,
    color: darkText,
    fontSize: '16px',
    boxShadow: `0 0 3px ${softGlow}`,
    outline: 'none',
  },

  // Paper List Item
  paperItem: {
    padding: '15px',
    marginBottom: '10px',
    borderRadius: '8px',
    backgroundColor: lightBackground,
    borderLeft: `4px solid ${primaryTeal}`,
    color: darkText,
    cursor: 'pointer',
    transition: 'background-color 0.2s, transform 0.2s',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.08)',
  },
  paperItemHover: {
    backgroundColor: '#EEEEEE', // Slightly darker hover
    transform: 'translateX(3px)',
  },
  paperTitle: {
    fontWeight: '600',
    marginBottom: '5px',
    color: primaryTeal,
  },
  paperMeta: {
    fontSize: '12px',
    color: '#888888',
  }
};

// --- 4. Main Component with Responsive Logic (Unchanged) ---
const SavedPaperScreens = () => {
  const [activeTab, setActiveTab] = useState('none'); 
  const [searchTerm, setSearchTerm] = useState('');
  const [hoverSaveBtn, setHoverSaveBtn] = useState(false);
  const [hoverLocalBtn, setHoverLocalBtn] = useState(false);
  
  const isMobile = useMediaQuery('(max-width: 600px)');

  // Calculations for stats (Unchanged)
  const totalPapers = dummySavedPapers.length;
  const easyCount = dummySavedPapers.filter(p => p.level === 'Easy').length;
  const mediumCount = dummySavedPapers.filter(p => p.level === 'Medium').length;
  const hardCount = dummySavedPapers.filter(p => p.level === 'Hard').length;
  const averageLevel = totalPapers > 0 
    ? (easyCount > mediumCount && easyCount > hardCount ? 'Easy' : 
      mediumCount > hardCount ? 'Medium' : 'Hard')
    : 'N/A';
  const filteredPapers = dummySavedPapers.filter(paper => 
    paper.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // --- RESPONSIVE STYLES OVERRIDES (Unchanged) ---
  const responsiveStyles = {
    container: {
      ...styles.container,
      padding: isMobile ? '20px 10px' : '40px',
    },
    navContainer: {
      ...styles.navContainer,
      width: isMobile ? '100%' : '80%',
      flexDirection: isMobile ? 'column' : 'row',
      gap: isMobile ? '15px' : '30px',
    },
    statsContainer: {
        ...styles.statsContainer,
        flexDirection: isMobile ? 'column' : 'row',
        gap: isMobile ? '10px' : '20px',
    },
    contentBox: {
        ...styles.contentBox,
        padding: isMobile ? '20px' : '30px',
        width: isMobile ? '100%' : '90%',
    },
    buttonContainer: {
        textAlign: isMobile ? 'left' : 'center',
        marginTop: '25px',
        display: isMobile ? 'flex' : 'block',
        flexDirection: 'column',
    },
    actionButton: {
        ...styles.actionButton,
        width: isMobile ? '100%' : 'auto',
        marginBottom: isMobile ? '10px' : '0',
    }
  };


  // --- RENDERING COMPONENTS (Unchanged) ---
  
  const PaperItem = ({ paper }) => {
    // ... (logic unchanged)
    const [hoverItem, setHoverItem] = useState(false);
    return (
      <div 
        style={{...styles.paperItem, ...(hoverItem ? styles.paperItemHover : {})}}
        onMouseEnter={() => setHoverItem(true)}
        onMouseLeave={() => setHoverItem(false)}
        onClick={() => alert(`Opening paper: ${paper.title}`)}
      >
        <div style={styles.paperTitle}>{paper.title}</div>
        <div style={styles.paperMeta}>
          Level: **{paper.level}** | Saved: {paper.date}
        </div>
      </div>
    );
  };

  const GeneratedPaperContent = () => (
    <div style={responsiveStyles.contentBox}>
      <h2 style={styles.title}>📄 Current Generated Paper Preview</h2>
      
      <div style={styles.previewContent}>
        {/* Mock Paper Content */}
        **Subject:** Computer Science <br/>
        **Topic:** React Hooks & State Management <br/>
        **Level:** Medium <br/>
        <br/>
        --- **Question 1 (10 Marks)** ---<br/>
        Explain the purpose of the `useEffect` hook in React. Provide a small code snippet demonstrating how to fetch data once when a component mounts.<br/>
        <br/>
        --- **Question 2 (15 Marks)** ---<br/>
        What is the difference between `useState` and `useReducer`? ...<br/>
        <br/>
        *... (More paper content here) ...*
      </div>
      
      <div style={responsiveStyles.buttonContainer}>
        <button 
          style={{...responsiveStyles.actionButton, ...(hoverSaveBtn ? styles.actionButtonHover : {})}}
          onMouseEnter={() => setHoverSaveBtn(true)}
          onMouseLeave={() => setHoverSaveBtn(false)}
          onClick={() => alert('Saving paper to WebApp...')}
        >
          Save to WebApp
        </button>
        <button 
          style={{...responsiveStyles.actionButton, ...(hoverLocalBtn ? styles.actionButtonHover : {})}}
          onMouseEnter={() => setHoverLocalBtn(true)}
          onMouseLeave={() => setHoverLocalBtn(false)}
          onClick={() => alert('Downloading PDF locally...')}
        >
          Download Locally (PDF)
        </button>
      </div>
    </div>
  );

  const SavedPapersContent = () => (
    <div style={responsiveStyles.contentBox}>
      <h2 style={styles.title}>📚 My Saved Papers List</h2>

      {/* Top Stat Boxes (Responsive) */}
      <div style={responsiveStyles.statsContainer}>
        <div style={styles.statBox}>
          <div style={styles.statCount}>{totalPapers}</div>
          <div style={styles.statLabel}>Total Saved Papers</div>
        </div>
        <div style={styles.statBox}>
          <div style={styles.statCount}>{averageLevel}</div>
          <div style={styles.statLabel}>Avg. Difficulty Level</div>
        </div>
        <div style={styles.statBox}>
          <div style={styles.statCount}>{easyCount} Easy</div>
          <div style={styles.statLabel}>Highest Concentration</div>
        </div>
      </div>

      {/* Search Bar */}
      <input
        type="text"
        placeholder="Search paper by title..."
        style={styles.searchBar}
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      
      {/* Saved Papers List */}
      <div style={{ maxHeight: isMobile ? '300px' : '400px', overflowY: 'auto' }}>
        {filteredPapers.length > 0 ? (
          filteredPapers.map(paper => (
            <PaperItem key={paper.id} paper={paper} />
          ))
        ) : (
          <p style={{ color: '#888', textAlign: 'center', marginTop: '50px' }}>
            No papers found matching "{searchTerm}".
          </p>
        )}
      </div>
    </div>
  );
  
  // --- MAIN RENDER (Unchanged) ---
  return (
    <div style={responsiveStyles.container}>
      
      {/* --- Navigation Boxes (Responsive) --- */}
      <div style={responsiveStyles.navContainer}>
        {/* Generated Paper Nav Box */}
        <div 
          style={{
            ...styles.navBoxBase, 
            ...(activeTab === 'generated' ? styles.navBoxActive : {})
          }}
          onClick={() => setActiveTab('generated')}
        >
          <h3 style={{...styles.navTitle, fontSize: isMobile ? '16px' : '18px'}}>📝 Generated Paper</h3>
        </div>
        
        {/* Saved Papers Nav Box */}
        <div 
          style={{
            ...styles.navBoxBase, 
            ...(activeTab === 'saved' ? styles.navBoxActive : {})
          }}
          onClick={() => setActiveTab('saved')}
        >
          <h3 style={{...styles.navTitle, fontSize: isMobile ? '16px' : '18px'}}>💾 My Saved Papers</h3>
        </div>
      </div>
      
      {/* --- Dynamic Content Area --- */}
      {activeTab === 'generated' && <GeneratedPaperContent />}
      {activeTab === 'saved' && <SavedPapersContent />}
      
      {activeTab === 'none' && (
        <div style={{ color: primaryTeal, fontSize: '18px', marginTop: '100px' }}>
          Select an option above to view content.
        </div>
      )}
      
    </div>
  );
};

export default SavedPaperScreens;