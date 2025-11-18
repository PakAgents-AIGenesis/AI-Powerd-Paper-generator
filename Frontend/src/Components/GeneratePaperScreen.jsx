import React, { useState } from 'react';

// Color definitions for consistency
const colors = {
    // UPDATED: Main background is white, contrast text is dark
    cardBackground: 'rgba(255, 255, 255, 0.5)',     // Transparent white for glass
    borderColor: 'rgba(0, 0, 0, 0.1)',              // Light border for definition
    headerText: '#1f2937',                           // Dark text for contrast
    label: '#374151',
    inputBorder: '#d1d5db',
    accentColor: '#059669',                          // Professional Green/Teal (Neon Base)
    lightGrayText: '#6b7280',
    backgroundLight: '#fff',                         // PAGE BACKGROUND IS WHITE
    errorColor: '#ef4444',
    disabledColor: '#a0a0a0', 
    
    // Difficulty Colors (remain bright for usability)
    easyColor: '#22c55e',    
    mediumColor: '#f97316',  
    hardColor: '#ef4444',    
    mixedColor: '#3b82f6',   
};

// Centralized style object using inline React styling conventions.
const styles = {
    screenContainer: {
        padding: '2rem 2.5rem',
        minHeight: 'calc(100vh - 4rem)', 
        backgroundColor: colors.backgroundLight, // White background
        fontFamily: 'sans-serif',
        color: colors.headerText,
    },
    topHeader: {
        fontSize: '1.75rem',
        fontWeight: 'bold',
        color: colors.accentColor, 
        marginBottom: '0.25rem',
    },
    topSubheader: {
        color: colors.lightGrayText,
        marginBottom: '2rem',
    },
    featureSection: {
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: '2.5rem',
        gap: '1rem',
    },
    featureCardBase: {
        flex: 1,
        backgroundColor: colors.cardBackground,
        padding: '1rem',
        borderRadius: '0.5rem',
        boxShadow: `0 0 10px ${colors.borderColor} inset`, 
        border: `1px solid ${colors.borderColor}`,
        textAlign: 'left',
        display: 'flex',
        alignItems: 'center',
        transition: 'all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94)',
        cursor: 'default',
    },
    featureCardHover: {
        boxShadow: `0 0 10px ${colors.accentColor}33, 0 6px 15px rgba(0, 0, 0, 0.15)`,
        transform: 'translateY(-3px) scale(1.01)', 
        borderColor: colors.accentColor,
    },
    featureIcon: {
        fontSize: '1.8rem',
        color: colors.accentColor,
        marginRight: '0.75rem',
    },
    featureText: {
        lineHeight: 1.3,
    },
    featureTitle: {
        fontSize: '0.9rem',
        fontWeight: 'bold',
        color: colors.headerText,
    },
    featureSubtitle: {
        fontSize: '0.75rem',
        color: colors.lightGrayText,
    },
    card: {
        backgroundColor: colors.cardBackground, 
        padding: '1.5rem',
        borderRadius: '0.75rem',
        boxShadow: `0 4px 10px rgba(0, 0, 0, 0.05)`, 
        border: `1px solid ${colors.borderColor}`,
        marginBottom: '2rem',
        backdropFilter: 'blur(10px)',
        WebkitBackdropFilter: 'blur(10px)',
        transition: 'transform 0.3s ease-out, box-shadow 0.3s ease-out',
        transformStyle: 'preserve-3d',
    },
    cardHoverEffect: {
        boxShadow: `0 0 3px ${colors.accentColor}, 0 4px 15px rgba(0, 0, 0, 0.1)`, 
        borderColor: colors.accentColor,
    },
    cardHeader: {
        fontSize: '1.1rem',
        fontWeight: 'bold',
        color: colors.headerText,
        marginBottom: '1rem',
        display: 'flex', 
        alignItems: 'center',
    },
    requiredMarker: { 
        color: colors.errorColor,
        marginLeft: '0.5rem',
        fontSize: '1.2rem',
        lineHeight: 1,
    },
    inputGroup: {
        marginBottom: '1.5rem',
    },
    inputField: {
        width: '100%',
        padding: '0.65rem 1rem',
        border: `1px solid ${colors.inputBorder}`,
        borderRadius: '0.375rem',
        fontSize: '1rem',
        boxSizing: 'border-box',
        transition: 'border-color 0.2s, box-shadow 0.2s',
        backgroundColor: '#fff', 
        color: colors.headerText,
    },
    inputFieldFocused: {
        outline: 'none',
        borderColor: colors.accentColor,
        boxShadow: `0 0 0 3px ${colors.accentColor}33`,
    },
    label: {
        display: 'block',
        fontSize: '0.875rem',
        fontWeight: 'medium',
        color: colors.label,
        marginBottom: '0.35rem',
    },
    checkboxGroup: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem',
        marginTop: '1.5rem',
    },
    checkboxLabel: {
        fontSize: '0.9rem',
        color: colors.lightGrayText,
        cursor: 'pointer',
    },
    // UPDATED GRID: 1.5fr for Label, 1fr for Input, 1fr for each of the 4 buttons (5 total equal-sized interactive boxes)
    questionRow: {
        display: 'grid',
        gridTemplateColumns: '1.5fr 1fr 1fr 1fr 1fr 1fr', 
        gap: '1rem',
        alignItems: 'center',
        marginBottom: '1.5rem',
    },
    questionRowLabel: {
        // Now only spanning 1 column in the new grid
        fontSize: '1rem',
        fontWeight: 'bold',
        color: colors.headerText,
    },
    difficultyButton: (isDisabled) => ({
        padding: '0.5rem 0.2rem',
        textAlign: 'center',
        borderRadius: '0.25rem',
        fontSize: '0.875rem',
        cursor: isDisabled ? 'not-allowed' : 'pointer',
        border: `1px solid ${isDisabled ? colors.disabledColor : colors.inputBorder}`,
        color: isDisabled ? colors.disabledColor : colors.label,
        backgroundColor: '#fff', 
        transition: 'all 0.1s ease',
        opacity: isDisabled ? 0.6 : 1,
    }),
    activeDifficulty: (level) => {
        let bgColor = colors.mixedColor; 
        let borderColor = colors.mixedColor;
        
        if (level === 'Easy') {
            bgColor = colors.easyColor;
            borderColor = colors.easyColor;
        } else if (level === 'Medium') {
            bgColor = colors.mediumColor;
            borderColor = colors.mediumColor;
        } else if (level === 'Hard') {
            bgColor = colors.hardColor;
            borderColor = colors.hardColor;
        }

        return {
            backgroundColor: bgColor,
            color: '#fff', 
            borderColor: borderColor,
        };
    },
    uploadControlGroup: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginTop: '1rem',
        marginBottom: '1rem',
    },
    multiFileButton: {
        padding: '0.5rem 1rem',
        backgroundColor: '#fff', 
        color: colors.accentColor,
        border: `1px solid ${colors.accentColor}`,
        borderRadius: '0.375rem',
        cursor: 'pointer',
        fontWeight: 'bold',
        transition: 'background-color 0.2s, boxShadow 0.2s',
        fontSize: '0.875rem',
        boxShadow: `0 0 5px ${colors.accentColor}33`,
    },
    fileListContainer: (isMissing) => ({
        display: 'flex',
        flexWrap: 'wrap',
        gap: '0.75rem',
        marginBottom: '1rem',
        padding: '0.5rem 0',
        minHeight: '3rem', 
        border: isMissing ? `1px solid ${colors.errorColor}` : '1px solid transparent', 
        borderRadius: '0.5rem',
    }),
    fileItem: {
        display: 'flex',
        alignItems: 'center',
        padding: '0.5rem 0.75rem',
        borderRadius: '0.375rem',
        backgroundColor: '#f3f4f6', 
        border: '1px solid transparent', 
        fontSize: '0.85rem',
        fontWeight: '500',
        color: colors.headerText,
        maxWidth: '100%',
    },
    removeFileButton: {
        marginLeft: '0.5rem',
        backgroundColor: 'transparent',
        border: 'none',
        color: colors.errorColor,
        cursor: 'pointer',
        fontWeight: 'bold',
        fontSize: '1rem',
        lineHeight: 1,
        padding: 0,
    },
    uploadArea: (isUploaded, isMissing, isMulti) => ({
        ...(isMulti ? {
            width: '120px', 
            height: '100px',
            padding: '0.5rem',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            flexShrink: 0,
        } : {
            padding: '2rem 1.5rem',
            width: '100%',
            height: 'auto',
        }),
        border: `2px dashed ${colors.inputBorder}`, 
        borderRadius: '0.5rem',
        textAlign: 'center',
        cursor: 'pointer',
        backgroundColor: isUploaded && !isMulti ? '#ecfdf5' : '#fff', 
        transition: 'background-color 0.2s, box-shadow 0.2s',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
    }),
    uploadIcon: {
        fontSize: '1.5rem',
        color: colors.accentColor,
        marginBottom: '0.5rem',
    },
    uploadText: (isMulti) => ({
        fontSize: isMulti ? '0.75rem' : '1rem',
        color: colors.accentColor,
        fontWeight: 'bold',
        lineHeight: 1.2,
    }),
    uploadHint: {
        fontSize: '0.8rem',
        color: colors.lightGrayText,
        marginTop: '0.25rem',
    },
    generateButton: (isFormInvalid) => ({ 
        padding: '0.75rem 2rem',
        backgroundColor: isFormInvalid ? colors.disabledColor : colors.accentColor, 
        color: '#fff',
        fontWeight: 'bold',
        borderRadius: '0.375rem',
        border: 'none',
        cursor: isFormInvalid ? 'not-allowed' : 'pointer',
        transition: 'background-color 0.2s, box-shadow 0.2s',
        marginTop: '2rem',
        fontSize: '1.1rem',
        float: 'right', 
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        boxShadow: isFormInvalid ? 'none' : `0 0 10px ${colors.accentColor}aa`,
    }),
    errorMessage: {
        color: colors.errorColor,
        fontSize: '0.8rem',
        marginTop: '0.5rem',
        textAlign: 'right',
        fontWeight: 'bold',
    },
};

/**
 * Custom hook to manage and apply hover styles to an element.
 */
const useHover = (initialStyle, hoverStyle) => {
    const [style, setStyle] = useState(initialStyle);
    
    const handleMouseEnter = () => setStyle({ ...initialStyle, ...hoverStyle });
    const handleMouseLeave = () => setStyle(initialStyle);
    
    return [style, handleMouseEnter, handleMouseLeave];
};

/**
 * Custom hook for the 3D tilt and professional glow effect on cards.
 */
const useCardHover = () => {
    const [transform, setTransform] = useState('');
    const [isHovered, setIsHovered] = useState(false);

    const handleMouseMove = (e) => {
        const { currentTarget: target } = e;
        const rect = target.getBoundingClientRect();
        
        const xPct = (e.clientX - (rect.left + rect.width / 2)) / rect.width * 100;
        const yPct = (e.clientY - (rect.top + rect.height / 2)) / rect.height * 100;
        
        const tiltX = (yPct / 50) * -3;
        const tiltY = (xPct / 50) * 3;
        
        setTransform(`perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale(1.005)`);
        setIsHovered(true);
    };

    const handleMouseLeave = () => {
        setTransform(''); 
        setIsHovered(false);
    };
    
    const style = {
        ...styles.card,
        ...(isHovered ? styles.cardHoverEffect : {}),
        transform: transform,
    };
    
    return [style, handleMouseMove, handleMouseLeave];
};


/**
 * Stateless component for selecting a specific question difficulty level.
 */
const DifficultySelector = ({ level, onSelect, currentSelection, isDisabled }) => {
    const isActive = currentSelection === level;

    return (
        <button 
            type="button" 
            style={{
                ...styles.difficultyButton(isDisabled),
                ...(isActive ? styles.activeDifficulty(level) : {}),
            }}
            onClick={() => {
                if (!isDisabled) {
                    onSelect(level);
                }
            }}
            disabled={isDisabled}
        >
            {level}
        </button>
    );
};

/**
 * Stateless component rendering a marketing feature card with hover effects.
 */
const FeatureCard = ({ icon, title, subtitle }) => {
    const [cardStyle, handleMouseEnter, handleMouseLeave] = useHover(
        styles.featureCardBase,
        styles.featureCardHover
    );
    
    return (
        <div 
            style={cardStyle}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            <div style={styles.featureIcon}>{icon}</div>
            <div style={styles.featureText}>
                <div style={styles.featureTitle}>{title}</div>
                <div style={styles.featureSubtitle}>{subtitle}</div>
            </div>
        </div>
    );
};


/**
 * Main component for the paper generation configuration screen.
 */
const GeneratePaperScreen = () => {
    const [formData, setFormData] = useState({
        paperHeading: '',
        totalMarks: 5, 
        includeRollNumber: true,
        includeName: true,
        includeClassSection: false,
        mcqCount: 0,
        mcqDifficulty: 'Mixed',
        saqCount: 0,
        saqDifficulty: 'Mixed', 
        laqCount: 0,
        laqDifficulty: 'Mixed',
    });
    const [allowMultipleFiles, setAllowMultipleFiles] = useState(false);
    const [focusedInput, setFocusedInput] = useState(null);
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [submissionAttempted, setSubmissionAttempted] = useState(false);
    const [isUserSignedIn] = useState(true); 

    // Hover state hooks for the three main cards
    const [paperCardStyle, paperHandleMouseMove, paperHandleMouseLeave] = useCardHover();
    const [questionCardStyle, questionHandleMouseMove, questionHandleMouseLeave] = useCardHover();
    const [uploadCardStyle, uploadHandleMouseMove, uploadHandleMouseLeave] = useCardHover();


    const MAX_FILES = 10;

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        
        setFormData(prev => ({ 
            ...prev, 
            [name]: type === 'checkbox' ? checked : (type === 'number' ? parseInt(value) || 0 : value)
        }));
    };

    const handleFileChange = (e) => {
        const files = Array.from(e.target.files);
        
        if (allowMultipleFiles) {
            const newFiles = [...uploadedFiles, ...files].slice(0, MAX_FILES);
            setUploadedFiles(newFiles);
        } else {
            setUploadedFiles(files.slice(0, 1));
        }
        e.target.value = null; 
    };

    const handleRemoveFile = (fileName) => {
        setUploadedFiles(uploadedFiles.filter(file => file.name !== fileName));
    };

    const handleDifficultySelect = (type, level) => {
        setFormData(prev => ({
            ...prev,
            [`${type}Difficulty`]: level
        }));
    };
    
    const { paperHeading, totalMarks, mcqCount, saqCount, laqCount } = formData;
    
    const isMcqDisabled = mcqCount === 0;
    const isSaqDisabled = saqCount === 0;
    const isLaqDisabled = laqCount === 0;
    
    const isQuestionCountValid = mcqCount > 0 || saqCount > 0 || laqCount > 0;
    const isMcqCountValid = mcqCount === 0 || (mcqCount >= 5 && mcqCount <= 100);
    const isSaqCountValid = saqCount === 0 || (saqCount >= 2 && saqCount <= 100);
    const isLaqCountValid = laqCount === 0 || (laqCount >= 1 && laqCount <= 10);
    
    const isUploaded = uploadedFiles.length > 0;
    const isMarksValid = totalMarks >= 5 && totalMarks <= 1000;
    
    const isFormInvalid = 
        !isUserSignedIn || 
        !paperHeading.trim() || 
        !isMarksValid || 
        !isUploaded ||
        !isQuestionCountValid ||
        !isMcqCountValid || 
        !isSaqCountValid || 
        !isLaqCountValid;
    
    const isMissingUpload = !isUploaded && submissionAttempted;
    const isMissingQuestionType = !isQuestionCountValid && submissionAttempted;

    const handleSubmit = (e) => {
        e.preventDefault();
        setSubmissionAttempted(true);

        if (isFormInvalid) {
            alert('Please fill all required fields and ensure all constraints (paper heading, marks, question counts, file upload, and sign-in status) are met.');
            return;
        }

        console.log('Generating paper with:', formData, 'Files:', uploadedFiles);
    };

    const getInputStyle = (isFocused) => {
        return {
            ...styles.inputField,
            ...(isFocused ? styles.inputFieldFocused : {}), 
        };
    };
    
    const uploadText = (isMulti, isSingleUploaded) => {
        if (isMulti) return "Add File";
        return isSingleUploaded ? "Click to change" : "Click to upload a single PDF/Document";
    };

    const showMultiFileUploadArea = allowMultipleFiles && uploadedFiles.length < MAX_FILES;

    return (
        <div style={styles.screenContainer}>
            <h1 style={styles.topHeader}>Generate Your Paper</h1>
            <p style={styles.topSubheader}>
                Create professional exam papers with AI assistance in seconds
            </p>

            <div style={styles.featureSection}>
                <FeatureCard icon="🤖" title="AI-Powered" subtitle="Smart Generation" />
                <FeatureCard icon="🕒" title="30 sec" subtitle="Average Generation" />
                <FeatureCard icon="✍️" title="100%" subtitle="Customizable" />
                <FeatureCard icon="📁" title="Multiple" subtitle="Export Formats" />
            </div>

            <form onSubmit={handleSubmit}>
                {/* Paper Configuration Section */}
                <div 
                    style={paperCardStyle}
                    onMouseMove={paperHandleMouseMove}
                    onMouseLeave={paperHandleMouseLeave}
                >
                    <h2 style={styles.cardHeader}>Paper Configuration</h2>
                    <p style={{ color: colors.lightGrayText, fontSize: '0.9rem', marginBottom: '1.5rem' }}>
                        Fill in the details to generate your exam paper
                    </p>

                    <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
                        <div>
                            <div style={styles.inputGroup}>
                                <label style={styles.label} htmlFor="paperHeading">Paper Heading *</label>
                                <input 
                                    type="text" 
                                    id="paperHeading" 
                                    name="paperHeading" 
                                    value={paperHeading}
                                    onChange={handleChange}
                                    style={getInputStyle(focusedInput === 'paperHeading')} 
                                    onFocus={() => setFocusedInput('paperHeading')}
                                    onBlur={() => setFocusedInput(null)}
                                    placeholder="e.g., Computer Science - Final Exam 2025"
                                    required 
                                />
                            </div>

                            <div style={styles.inputGroup}>
                                <label style={styles.label} htmlFor="totalMarks">Total Marks *</label>
                                <input 
                                    type="number" 
                                    id="totalMarks" 
                                    name="totalMarks" 
                                    value={totalMarks}
                                    onChange={handleChange}
                                    style={{
                                        ...getInputStyle(focusedInput === 'totalMarks'),
                                        borderColor: submissionAttempted && !isMarksValid ? colors.errorColor : getInputStyle(focusedInput === 'totalMarks').borderColor,
                                        ...(focusedInput === 'totalMarks' ? styles.inputFieldFocused : {})
                                    }} 
                                    onFocus={() => setFocusedInput('totalMarks')}
                                    onBlur={() => setFocusedInput(null)}
                                    min="5" 
                                    max="1000" 
                                    required
                                />
                                {submissionAttempted && !isMarksValid && (
                                    <p style={{ ...styles.errorMessage, textAlign: 'left' }}>
                                        Total Marks must be between 5 and 1000.
                                    </p>
                                )}
                            </div>
                        </div>

                        <div style={styles.inputGroup}>
                            <label style={styles.label}>Optional Fields on Paper</label>
                            <div style={styles.checkboxGroup}>
                                <label style={styles.checkboxLabel}>
                                    <input type="checkbox" name="includeRollNumber" checked={formData.includeRollNumber} onChange={handleChange} style={{ marginRight: '0.5rem', accentColor: colors.accentColor }} />
                                    Include Roll Number field
                                </label>
                                <label style={styles.checkboxLabel}>
                                    <input type="checkbox" name="includeName" checked={formData.includeName} onChange={handleChange} style={{ marginRight: '0.5rem', accentColor: colors.accentColor }} />
                                    Include Name Field
                                </label>
                                <label style={styles.checkboxLabel}>
                                    <input type="checkbox" name="includeClassSection" checked={formData.includeClassSection} onChange={handleChange} style={{ marginRight: '0.5rem', accentColor: colors.accentColor }} />
                                    Include Class/Section field
                                </label>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Question Configuration Section */}
                <div 
                    style={questionCardStyle}
                    onMouseMove={questionHandleMouseMove}
                    onMouseLeave={questionHandleMouseLeave}
                >
                    <h2 style={styles.cardHeader}>
                        Question Configuration 
                        <span style={styles.requiredMarker}>*</span>
                        {isMissingQuestionType && (
                            <span style={{ fontSize: '0.8rem', color: colors.errorColor, marginLeft: '1rem' }}>
                                Must choose at least one question type (MCQ, SAQ, or LAQ).
                            </span>
                        )}
                    </h2>
                    
                    {/* Multiple Choice Questions Row */}
                    <div style={styles.questionRow}>
                        <div style={styles.questionRowLabel}>Multiple Choice Questions (5-100)</div>
                        <input 
                            type="number" 
                            name="mcqCount" 
                            value={mcqCount}
                            onChange={handleChange}
                            style={getInputStyle(focusedInput === 'mcqCount')} 
                            onFocus={() => setFocusedInput('mcqCount')}
                            onBlur={() => setFocusedInput(null)}
                            min="0" 
                            max="100"
                        />
                        <DifficultySelector level="Easy" onSelect={(l) => handleDifficultySelect('mcq', l)} currentSelection={formData.mcqDifficulty} isDisabled={isMcqDisabled} />
                        <DifficultySelector level="Medium" onSelect={(l) => handleDifficultySelect('mcq', l)} currentSelection={formData.mcqDifficulty} isDisabled={isMcqDisabled} />
                        <DifficultySelector level="Hard" onSelect={(l) => handleDifficultySelect('mcq', l)} currentSelection={formData.mcqDifficulty} isDisabled={isMcqDisabled} />
                        {/* MOVED: Mixed selector is now placed after Hard */}
                        <DifficultySelector level="Mixed" onSelect={(l) => handleDifficultySelect('mcq', l)} currentSelection={formData.mcqDifficulty} isDisabled={isMcqDisabled} />
                    </div>
                    
                    {/* Short Answer Questions Row */}
                    <div style={styles.questionRow}>
                        <div style={styles.questionRowLabel}>Short Answer Questions (2-100)</div>
                        <input 
                            type="number" 
                            name="saqCount" 
                            value={saqCount}
                            onChange={handleChange}
                            style={getInputStyle(focusedInput === 'saqCount')} 
                            onFocus={() => setFocusedInput('saqCount')}
                            onBlur={() => setFocusedInput(null)}
                            min="0" 
                            max="100" 
                        />
                        <DifficultySelector level="Easy" onSelect={(l) => handleDifficultySelect('saq', l)} currentSelection={formData.saqDifficulty} isDisabled={isSaqDisabled} />
                        <DifficultySelector level="Medium" onSelect={(l) => handleDifficultySelect('saq', l)} currentSelection={formData.saqDifficulty} isDisabled={isSaqDisabled} />
                        <DifficultySelector level="Hard" onSelect={(l) => handleDifficultySelect('saq', l)} currentSelection={formData.saqDifficulty} isDisabled={isSaqDisabled} />
                        {/* MOVED: Mixed selector is now placed after Hard */}
                        <DifficultySelector level="Mixed" onSelect={(l) => handleDifficultySelect('saq', l)} currentSelection={formData.saqDifficulty} isDisabled={isSaqDisabled} />
                    </div>
                    
                    {/* Long Answer Questions Row */}
                    <div style={styles.questionRow}>
                        <div style={styles.questionRowLabel}>Long Answer Questions (1-10)</div>
                        <input 
                            type="number" 
                            name="laqCount" 
                            value={laqCount}
                            onChange={handleChange}
                            style={getInputStyle(focusedInput === 'laqCount')} 
                            onFocus={() => setFocusedInput('laqCount')}
                            onBlur={() => setFocusedInput(null)}
                            min="0" 
                            max="10" 
                        />
                        <DifficultySelector level="Easy" onSelect={(l) => handleDifficultySelect('laq', l)} currentSelection={formData.laqDifficulty} isDisabled={isLaqDisabled} />
                        <DifficultySelector level="Medium" onSelect={(l) => handleDifficultySelect('laq', l)} currentSelection={formData.laqDifficulty} isDisabled={isLaqDisabled} />
                        <DifficultySelector level="Hard" onSelect={(l) => handleDifficultySelect('laq', l)} currentSelection={formData.laqDifficulty} isDisabled={isLaqDisabled} />
                        {/* MOVED: Mixed selector is now placed after Hard */}
                        <DifficultySelector level="Mixed" onSelect={(l) => handleDifficultySelect('laq', l)} currentSelection={formData.laqDifficulty} isDisabled={isLaqDisabled} />
                    </div>
                </div>

                {/* Upload PDF/Notes Section */}
                <div 
                    style={uploadCardStyle}
                    onMouseMove={uploadHandleMouseMove}
                    onMouseLeave={uploadHandleMouseLeave}
                >
                    <h2 style={{ ...styles.cardHeader, borderBottom: 'none', marginBottom: '0' }}>
                        Upload PDF/Notes 
                        <span style={styles.requiredMarker}>*</span>
                    </h2>
                    
                    <div style={styles.uploadControlGroup}>
                        <p style={{...styles.uploadHint, color: isMissingUpload ? colors.errorColor : colors.lightGrayText}}>
                            {allowMultipleFiles 
                                ? `Max ${MAX_FILES} files allowed. Currently selected: ${uploadedFiles.length}` 
                                : `This document is **required** for generation.`
                            }
                        </p>
                        <button 
                            type="button" 
                            style={styles.multiFileButton}
                            onClick={() => {
                                setAllowMultipleFiles(!allowMultipleFiles);
                                setUploadedFiles([]); 
                            }}
                        >
                            {allowMultipleFiles ? 'Switch to Single File' : 'Allow Multiple Files'}
                        </button>
                    </div>

                    <div 
                        style={styles.fileListContainer(isMissingUpload)}
                    >
                        
                        {/* -------------------- MULTI-FILE MODE DISPLAY -------------------- */}
                        {allowMultipleFiles && (
                            <>
                                {uploadedFiles.map((file, index) => (
                                    <div key={index} style={styles.fileItem}>
                                        <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '150px' }}>{file.name}</span>
                                        <button 
                                            type="button" 
                                            style={styles.removeFileButton}
                                            onClick={() => handleRemoveFile(file.name)}
                                        >
                                            &times;
                                        </button>
                                    </div>
                                ))}

                                {/* The Dynamic '+ Add File' Box (Visible until MAX_FILES is reached) */}
                                {showMultiFileUploadArea && (
                                    <div 
                                        style={styles.uploadArea(false, false, true)} 
                                        onClick={() => document.getElementById('file-upload').click()}
                                    >
                                        <input 
                                            type="file" 
                                            id="file-upload" 
                                            name="file-upload"
                                            onChange={handleFileChange}
                                            style={{ display: 'none' }} 
                                            multiple={allowMultipleFiles} 
                                            accept=".pdf, .doc, .docx, .txt" 
                                        />
                                        <div style={styles.uploadIcon}>
                                            {'+'}
                                        </div>
                                        <div style={styles.uploadText(true)}>
                                            Add File
                                        </div>
                                    </div>
                                )}
                                
                                {uploadedFiles.length === MAX_FILES && (
                                    <p style={{...styles.uploadHint, color: colors.errorColor, width: '100%', textAlign: 'left', marginLeft: '0.5rem'}}>
                                        Maximum limit of {MAX_FILES} files reached.
                                    </p>
                                )}
                            </>
                        )}
                        
                        {/* -------------------- SINGLE-FILE MODE DISPLAY -------------------- */}
                        {!allowMultipleFiles && (
                            <div 
                                style={styles.uploadArea(isUploaded, isMissingUpload, false)}
                                onClick={() => document.getElementById('file-upload').click()}
                            >
                                <input 
                                    type="file" 
                                    id="file-upload" 
                                    name="file-upload"
                                    onChange={handleFileChange}
                                    style={{ display: 'none' }} 
                                    multiple={false} 
                                    accept=".pdf, .doc, .docx, .txt" 
                                />
                                <div style={styles.uploadIcon}>
                                    {isUploaded ? '✅' : '⬆️'}
                                </div>
                                <div style={styles.uploadText(false, isUploaded)}>
                                    {isUploaded ? uploadedFiles[0].name : uploadText(false, false)}
                                </div>
                                {!isUploaded && 
                                    <p style={{...styles.uploadHint, color: colors.lightGrayText}}>
                                        PDF, DOCX, TXT formats
                                    </p>
                                }
                                {isUploaded && 
                                    <p style={{...styles.uploadHint, color: colors.lightGrayText}}>
                                        Click to change file
                                    </p>
                                }
                            </div>
                        )}
                    </div>
                </div>

                {/* Primary Submission Button */}
                {!isUserSignedIn && (
                    <p style={{ ...styles.errorMessage, textAlign: 'right' }}>
                        You must be signed in to generate the paper.
                    </p>
                )}
                <button 
                    type="submit" 
                    style={styles.generateButton(isFormInvalid)}
                    disabled={!isUserSignedIn} 
                >
                    <span style={{ fontSize: '1.25rem' }}>✨</span> Generate Paper
                </button>
            </form>
        </div>
    );
};

export default GeneratePaperScreen;