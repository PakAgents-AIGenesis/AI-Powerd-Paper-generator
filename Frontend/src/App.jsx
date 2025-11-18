import React, { useState } from 'react';
import Sidebar from './Components/Sidebar';
import TopBar from './Components/TopBar';
import GeneratePaperScreen from './Components/GeneratePaperScreen';
import SavedPaperScreens from './Components/SavedPapersScreen';
import SettingsScreen from './Components/SettingsScreen';
import AboutScreen from './Components/AboutScreen';
import AuthScreen from './Components/AuthScreen';


function App() {
  // 1. State: Tracks which sidebar link is currently active ('generate', 'saved', or 'settings')
  const [activeLink, setActiveLink] = useState('generate');

  // 2. Logic: Renders the correct screen component based on the active state
  const renderContent = () => {
    switch (activeLink) {
      case 'generate':
        return <GeneratePaperScreen/>;
      case 'saved':
        return <SavedPaperScreens/>;
      case 'settings':
        return <SettingsScreen/>;
      case 'about':
        return <AboutScreen/>;
      case 'signup':
        return <AuthScreen/>;
      default:
        return <GeneratePaperScreen />;
    }
  };

  // 3. Layout: Uses inline CSS to structure the entire application
  return (
    <div style={{ display: 'flex' }}>
      {/* 1. Sidebar (Fixed to the left) */}
      
      <Sidebar activeLink={activeLink} setActiveLink={setActiveLink}/>
      {/* 2. TopBar (Fixed to the top, offset by the sidebar width) */}
      <TopBar/>
      
      {/* 3. Main Content Area */}
      <main 
        style={{ 
          marginLeft: '18rem',      // Pushes content past the fixed 18rem sidebar
          marginTop: '4rem',        // Pushes content below the fixed 4rem top bar
          width: 'calc(100% - 18rem)', // Calculates the remaining width for the main area
          minHeight: 'calc(100vh - 4rem)', // Fills remaining vertical space
          backgroundColor: '#f7f8fa', // Light background for the content area
        }}
      >
        {renderContent()}
      </main>
    </div>
  );
}

export default App;