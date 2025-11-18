import React, { useState, useEffect } from 'react';
import { Settings, User, Lock, Mail, Save, CheckSquare } from 'lucide-react';

// --- STYLING CONSTANTS (Dark Theme with Subtle Neon) ---
const primaryTeal = '#00CED1'; // Darker Teal
const softGlow = 'rgba(0, 206, 209, 0.5)';
const darkBackground = '#FFFFFF'; // Base Background
const cardBackground = '#F5F5F5'; // Card Background
const lightText = '#00CED1'; // Light text for dark mode
const mutedText = '#AAAAAA'; // Muted secondary text
const inputBackground = '#FFFFFF'; // Input field background
const lightBackground = lightText; // Defined for toggle thumb (was missing a definition)

const styles = {
    // Main Container
    container: {
        padding: '40px',
        backgroundColor: darkBackground,
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        fontFamily: 'Inter, sans-serif',
    },
    
    // Header and Title
    header: {
        display: 'flex',
        alignItems: 'center',
        marginBottom: '30px',
        width: '90%',
        maxWidth: '800px',
    },
    title: {
        color: primaryTeal,
        fontSize: '28px',
        fontWeight: '700',
        marginLeft: '10px',
        textShadow: `0 0 5px ${softGlow}`,
    },

    // Setting Cards Wrapper
    cardWrapper: (isMobile) => ({
        width: isMobile ? '95%' : '90%',
        maxWidth: '800px',
        display: 'flex',
        flexDirection: 'column',
        gap: '30px',
        marginBottom: '80px',
    }),
    
    // Individual Setting Card
    card: {
        backgroundColor: cardBackground,
        borderRadius: '16px',
        padding: '30px',
        boxShadow: `
            0 10px 30px rgba(0, 0, 0, 0.5), 
            0 0 10px ${softGlow} inset
        `, // 3D dark shadow + subtle inner glow
        border: `1px solid ${primaryTeal}`,
    },
    
    // Card Header (Section Title)
    cardHeader: {
        display: 'flex',
        alignItems: 'center',
        paddingBottom: '15px',
        marginBottom: '20px',
        borderBottom: `1px solid ${inputBackground}`,
    },
    cardTitle: {
        color: lightText,
        fontSize: '20px',
        fontWeight: '600',
        marginLeft: '10px',
    },

    // Form Elements (***CORRECTED FOR HALF-WIDTH SIZING***)
    formGroup: (isHalf) => ({
        marginBottom: isHalf ? '0' : '20px', 
        display: 'flex',
        flexDirection: isHalf ? 'row' : 'column',
        gap: isHalf ? '20px' : '0', 
        flexWrap: 'wrap',
        width: isHalf? '':'100%',
    }),
    inputFieldContainer: (isHalf) => ({
        // Calculates 50% width minus half the gap (10px) to ensure two inputs fit exactly.
        flex: isHalf ? '1 1 calc(50% - 10px)' : '1 1 100%',
        minWidth: isHalf ? '140px' : '250px', 
        maxWidth: isHalf ? '35%' : '100%',
        marginRight: isHalf ? '50px' : '0',
        marginBottom: '20px', // Consistent vertical spacing
    }), 
    inputLabel: {
        display: 'block',
        color: mutedText,
        fontSize: '12px',
        marginBottom: '5px',
    },
    inputBase: {
        width: '100%',
        padding: '12px',
        borderRadius: '8px',
        border: `1px solid ${primaryTeal}`,
        backgroundColor: inputBackground,
        color: lightText,
        fontSize: '14px',
        boxShadow: `0 0 5px rgba(0, 0, 0, 0.3)`,
        outline: 'none',
        transition: 'border-color 0.2s, box-shadow 0.2s',
    },
    
    // Toggle/Preference Row
    preferenceRow: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '15px 0',
        borderBottom: `1px solid ${inputBackground}`,
    },
    prefTextGroup: {
        flex: 1,
    },
    prefTitle: {
        color: lightText,
        fontSize: '16px',
        fontWeight: '500',
    },
    prefSubtitle: {
        color: mutedText,
        fontSize: '12px',
        marginTop: '3px',
    },

    // Toggle Switch (Custom implementation for styling)
    toggleContainer: {
        position: 'relative',
        width: '40px',
        height: '24px',
        cursor: 'pointer',
    },
    toggleTrack: (isOn) => ({
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        borderRadius: '12px',
        backgroundColor: isOn ? primaryTeal : '#555555',
        transition: 'background-color 0.4s',
        boxShadow: isOn ? `0 0 5px ${softGlow}` : 'none', // Neon glow when ON
    }),
    toggleThumb: (isOn) => ({
        position: 'absolute',
        content: '""',
        height: '18px',
        width: '18px',
        borderRadius: '50%',
        backgroundColor: lightBackground,
        transition: 'transform 0.4s',
        top: '3px',
        left: isOn ? 'calc(100% - 21px)' : '3px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.4)',
    }),

    // Profile Photo Section
    photoSection: {
        display: 'flex',
        alignItems: 'center',
        marginBottom: '30px',
    },
    photoIcon: {
        backgroundColor: primaryTeal,
        borderRadius: '50%',
        padding: '15px',
        width: '50px',
        height: '50px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        boxShadow: `0 0 10px ${softGlow}`,
    },
    photoText: {
        marginLeft: '20px',
    },
    changePhotoButton: {
        padding: '8px 15px',
        backgroundColor: primaryTeal,
        color: darkBackground,
        fontWeight: '600',
        borderRadius: '8px',
        border: 'none',
        cursor: 'pointer',
        marginBottom: '5px',
        boxShadow: `0 0 8px ${softGlow}`,
        transition: 'all 0.2s',
        whiteSpace: 'nowrap',
    },
    photoHint: {
        fontSize: '11px',
        color: mutedText,
    },

    // Security
    securityButton: {
        padding: '12px 20px',
        backgroundColor: inputBackground,
        color: primaryTeal,
        fontWeight: '600',
        borderRadius: '8px',
        border: `1px solid ${primaryTeal}`,
        cursor: 'pointer',
        boxShadow: `0 0 8px ${softGlow}`,
        transition: 'all 0.2s',
    },
    securityButtonHover: {
        backgroundColor: primaryTeal,
        color: darkBackground,
        boxShadow: `0 0 15px ${softGlow}`,
    },
    lastChanged: {
        color: mutedText,
        fontSize: '12px',
        marginTop: '10px',
        marginLeft: '5px',
    },

  // Footer Buttons
footer: {
    position: 'fixed',
    bottom: 0,
    width: '100%',
    backgroundColor: 'transparent', 
    padding: '15px 40px',
    display: 'flex',
    justifyContent: 'center', 
    gap: '15px',
    zIndex: 10,
},
    saveButton: {
        padding: '10px 20px',
        backgroundColor: primaryTeal,
        color: darkBackground,
        fontWeight: '700',
        borderRadius: '8px',
        border: 'none',
        cursor: 'pointer',
        boxShadow: `0 0 10px ${softGlow}`,
        transition: 'all 0.2s',
    },
    saveButtonHover: {
        color: '#101525',
        backgroundColor: '#E0FFFF',
        boxShadow: `0 0 15px #E0FFFF`,
    },
    cancelButton: {
        padding: '10px 20px',
        backgroundColor: inputBackground,
        color: lightText,
        fontWeight: '500',
        borderRadius: '8px',
        border: `1px solid ${mutedText}`,
        cursor: 'pointer',
        transition: 'all 0.2s',
    },
};

// --- Custom Hook for Responsive Design ---
const useIsMobile = (breakpoint = 600) => {
    const [isMobile, setIsMobile] = useState(window.innerWidth < breakpoint);

    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < breakpoint);
        };
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, [breakpoint]);

    return isMobile;
};

// --- Custom Components for Reusability (Defined OUTSIDE main component) ---

const CustomToggle = ({ isOn, onToggle }) => {
    return (
        <div style={styles.toggleContainer} onClick={onToggle}>
            <div style={styles.toggleTrack(isOn)}></div>
            <div style={styles.toggleThumb(isOn)}></div>
        </div>
    );
};

const PreferenceRow = ({ title, subtitle, isChecked, onToggle }) => (
    <div style={styles.preferenceRow}>
        <div style={styles.prefTextGroup}>
            <div style={styles.prefTitle}>{title}</div>
            <div style={styles.prefSubtitle}>{subtitle}</div>
        </div>
        <CustomToggle isOn={isChecked} onToggle={onToggle} />
    </div>
);

// ***CORRECTED: Added isHalf prop and passed it to inputFieldContainer style***
const InputField = ({ label, value, icon: Icon, type = 'text', readOnly = false, isHalf = false, onChange = () => {} }) => {
    const [isFocused, setIsFocused] = useState(false);
    
    // Set up dynamic styles for focus glow
    const inputStyle = {
        ...styles.inputBase,
        ...(Icon ? { paddingLeft: '40px' } : {}),
        ...(isFocused ? { 
            borderColor: primaryTeal,
            boxShadow: `0 0 8px ${softGlow}` 
        } : {}),
    };

    return (
        <div style={styles.inputFieldContainer(isHalf)}>
            <label style={styles.inputLabel}>{label}</label>
            <div style={{ position: 'relative' }}>
                {Icon && (
                    <Icon size={18} style={{ position: 'absolute', top: '12px', left: '12px', color: primaryTeal, zIndex: 1 }} />
                )}
                <input
                    type={type}
                    value={value}
                    readOnly={readOnly}
                    onChange={(e) => onChange(e.target.value)}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    style={inputStyle}
                />
            </div>
        </div>
    );
};

// Reusable button components to encapsulate hover state logic
const HoverTealButton = ({ children, style, ...props }) => {
    const [isHovered, setIsHovered] = useState(false);
    const combinedStyle = {
        ...styles.securityButton,
        ...style,
        ...(isHovered ? styles.securityButtonHover : {})
    };

    return (
        <button
            style={combinedStyle}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            {...props}
        >
            {children}
        </button>
    );
};

const SaveButton = ({ children, style, ...props }) => {
    const [isHovered, setIsHovered] = useState(false);
    const combinedStyle = {
        ...styles.saveButton,
        ...style,
        ...(isHovered ? styles.saveButtonHover : {})
    };

    return (
        <button
            style={combinedStyle}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            {...props}
        >
            {children}
        </button>
    );
};


// --- Refactored Card Components (Defined OUTSIDE main component) ---
const PersonalInformationCard = ({ settingsData, handleDataChange }) => (
    <div style={styles.card}>
        <div style={styles.cardHeader}>
            <User size={24} color={primaryTeal} />
            <h2 style={styles.cardTitle}>Personal Information</h2>
        </div>
        
        {/* Photo Section (omitted for brevity) */}
        <div style={styles.photoSection}>
            <div style={styles.photoIcon}>
                <User size={28} color={darkBackground} fill={darkBackground} />
            </div>
            <div style={styles.photoText}>
                <button style={styles.changePhotoButton}>Change Photo</button>
                <div style={styles.photoHint}>JPG, PNG or GIF. Max size 2MB</div>
            </div>
        </div>
        
        {/* Form Fields - Half-Width Group 1 */}
        <div style={styles.formGroup(true)}>
            <InputField 
                label="First Name" 
                value={settingsData.firstName} 
                isHalf={true} 
                onChange={(v) => handleDataChange('firstName', v)} 
            />
            <InputField 
                label="Last Name" 
                value={settingsData.lastName} 
                isHalf={true} 
                onChange={(v) => handleDataChange('lastName', v)} 
            />
        </div>

        {/* ***CORRECTED FIELD: isHalf={true} added, readOnly removed*** */}
        {/* We use formGroup(true) here to ensure the reduced size is applied correctly */}
        <div style={styles.formGroup(true)}> 
            <InputField 
                label="Email Address (Login ID)" 
                value={settingsData.email} 
                icon={Mail} 
                isHalf={true} // Reduced width 
                onChange={(v) => handleDataChange('email', v)} 
            />
        </div>
        
        {/* Form Fields - Half-Width Group 2 */}
        <div style={styles.formGroup(true)}>
            <InputField 
                label="Institution/School" 
                value={settingsData.institution} 
                icon={CheckSquare} 
                isHalf={true} 
                onChange={(v) => handleDataChange('institution', v)} 
            />
            <InputField 
                label="Role" 
                value={settingsData.role} 
                isHalf={true} 
                onChange={(v) => handleDataChange('role', v)} 
            />
        </div>
    </div>
);

const PreferencesCard = ({ preferences, handleToggle }) => (
    <div style={styles.card}>
        <div style={styles.cardHeader}>
            <Settings size={24} color={primaryTeal} />
            <h2 style={styles.cardTitle}>Preferences</h2>
        </div>
        
        <PreferenceRow
            title="Email Notifications"
            subtitle="Receive email updates about your papers and platform activity"
            isChecked={preferences.emailNotifications}
            onToggle={() => handleToggle('emailNotifications')}
        />
        <PreferenceRow
            title="Auto-save Work"
            subtitle="Automatically save generated papers and drafts every 30 seconds"
            isChecked={preferences.autoSavePapers}
            onToggle={() => handleToggle('autoSavePapers')}
        />
        <PreferenceRow
            title="Show Difficulty Badges"
            subtitle="Display a colored badge indicating question difficulty levels"
            isChecked={preferences.showDifficultyBadges}
            onToggle={() => handleToggle('showDifficultyBadges')}
        />
        <PreferenceRow
            title="Dark Mode"
            subtitle="Use dark theme for the interface (current theme)"
            isChecked={preferences.darkMode}
            onToggle={() => handleToggle('darkMode')}
        />
    </div>
);

const SecurityCard = () => (
    <div style={styles.card}>
        <div style={styles.cardHeader}>
            <Lock size={24} color={primaryTeal} />
            <h2 style={styles.cardTitle}>Security</h2>
        </div>
        
        <HoverTealButton onClick={() => alert('Password change initiated.')}>
            Change Password
        </HoverTealButton>
        
        <div style={styles.lastChanged}>
            Last changed: November 1, 2025
        </div>
    </div>
);


// --- Main Settings Component ---
const SettingsScreen = () => {
    const isMobile = useIsMobile();
    
    // State to hold settings data
    const [settingsData, setSettingsData] = useState({
        firstName: "John",
        lastName: "Doe",
        email: "john.doe@example.com",
        institution: "Springfield High School",
        role: "Teacher",
    });

    // State for preferences (toggles)
    const [preferences, setPreferences] = useState({
        emailNotifications: true,
        autoSavePapers: true,
        showDifficultyBadges: true,
        darkMode: true,
    });

    const handleDataChange = (key, value) => {
        setSettingsData(prev => ({ ...prev, [key]: value }));
    };

    const handleToggle = (key) => {
        setPreferences(prev => ({ ...prev, [key]: !prev[key] }));
    };
    
    // Handler for saving changes (stub)
    const handleSave = () => {
        console.log('Saving Changes:', { settingsData, preferences });
        alert('Settings saved successfully!');
    };

    // Handler for canceling changes (stub)
    const handleCancel = () => {
        // In a real app, this would revert to initial state or fetched data
        alert('Changes cancelled.');
        // For demonstration, we'll just log
        console.log('Changes cancelled.');
    };

    // --- MAIN RENDER ---
    return (
        <div style={styles.container}>
            <div style={styles.header}>
                <Settings size={30} color={primaryTeal} />
                <h1 style={styles.title}>Settings</h1>
            </div>
            
            <div style={styles.cardWrapper(isMobile)}>
                {/* 1. Personal Information */}
                <PersonalInformationCard 
                    settingsData={settingsData} 
                    handleDataChange={handleDataChange} 
                />
                
                {/* 2. Preferences */}
                <PreferencesCard 
                    preferences={preferences} 
                    handleToggle={handleToggle} 
                />
                
                {/* 3. Security */}
                <SecurityCard />
            </div>

            {/* Floating Footer for Save/Cancel */}
            <div style={styles.footer}>
                <button style={styles.cancelButton} onClick={handleCancel}>Cancel</button>
                <SaveButton onClick={handleSave}>
                    <Save size={16} style={{ marginRight: '8px' }} />
                    Save Changes
                </SaveButton>
            </div>
        </div>
    ); 
};
 
export default SettingsScreen;