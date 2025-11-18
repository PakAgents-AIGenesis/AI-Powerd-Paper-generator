import React, { useState } from 'react';

// --- Shared Styles (for Inline CSS) ---

const styles = {
  // --- Container & Card Styles (White Background) ---
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    backgroundColor: '#ffffff', // Pure white background
    fontFamily: 'Arial, sans-serif',
    // We keep perspective, but remove card transform logic
    // to prevent hit area issues.
    perspective: '1000px', 
    overflow: 'hidden',
  },
  card: {
    width: '100%',
    maxWidth: '400px',
    padding: '40px',
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 8px 30px rgba(0, 0, 0, 0.1)', 
    border: '1px solid #e0e0e0',
    position: 'relative',
    transformStyle: 'flat', 
  },
  
  // --- Text & Input Styles ---
  title: {
    textAlign: 'center',
    marginBottom: '30px',
    color: '#101525', // Primary blue
  },
  formGroup: {
    marginBottom: '20px',
    position: 'relative',
  },
  label: {
    display: 'block',
    marginBottom: '8px',
    fontWeight: 'bold',
    color: '#333',
    fontSize: '14px',
  },
  input: {
    width: '100%',
    padding: '12px',
    background: '#f8f8f8',
    border: '1px solid #ddd',
    borderRadius: '6px',
    boxSizing: 'border-box',
    color: '#333',
    fontSize: '16px',
    transition: 'none', 
  },
  inputFocus: { 
    borderColor: '#00ffff', 
    boxShadow: '0 0 5px rgba(0, 255, 255, 0.5)', 
    transform: 'scale(1.01)',
  },
  
  // --- Button Styles (where 3D animation remains) ---
  submitButton: {
    width: '100%',
    padding: '14px',
    backgroundColor: '#101525', 
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    fontSize: '17px',
    fontWeight: 'bold',
    cursor: 'pointer',
    marginTop: '20px',
    boxShadow: '0 4px 10px rgba(0, 123, 255, 0.3)',
    // Added a slight translation to ensure Z-depth is applied cleanly
    transform: 'translateY(0) translateZ(0)',
    transition: 'none', 
  },
  submitButtonHover: {
    backgroundColor: '#18B097', 
    color: '#333',
    boxShadow: '0 6px 15px rgba(0, 255, 255, 0.5)',
    // Subtler 3D animation for safety
    transform: 'scale(1.02) translateZ(5px)', 
  },

  // --- Toggle Link Styles ---
  toggleText: {
    textAlign: 'center',
    marginTop: '25px',
    color: '#666',
    fontSize: '14px',
  },
  toggleButton: {
    color: '#101525', 
    backgroundColor: 'transparent',
    border: 'none',
    cursor: 'pointer',
    fontWeight: 'bold',
    marginLeft: '8px',
    padding: '0',
    fontSize: '14px',
    textDecoration: 'none',
    transition: 'none',
    transform: 'translateZ(0)',
  },
  toggleButtonHover: { 
    textShadow: '0 0 5px rgba(0, 255, 255, 0.6)',
    transform: 'scale(1.05)',
  }
};

// --- Component Definition ---

const AuthScreen = () => {
  const [isSignIn, setIsSignIn] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });

  // States for dynamic styling (Hover and Focus)
  const [isSubmitHovered, setIsSubmitHovered] = useState(false);
  const [isToggleHovered, setIsToggleHovered] = useState(false);
  // Removed isCardHovered
  const [focusedInput, setFocusedInput] = useState(null); 

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSignIn = (e) => {
    e.preventDefault();
    if (!formData.email || !formData.password) {
      alert("Please enter both email and password.");
      return;
    }
    console.log('Signing In with:', { email: formData.email, password: formData.password });
    alert(`Sign In Attempt: Email: ${formData.email}`);
  };

  const handleSignUp = (e) => {
    e.preventDefault();
    if (!formData.username || !formData.email || !formData.password) {
      alert("Please fill in all fields.");
      return;
    }
    console.log('Signing Up with:', formData);
    alert(`Sign Up Attempt: Username: ${formData.username}`);
  };

  const toggleMode = () => {
    setIsSignIn(prev => !prev);
    setFormData({ username: '', email: '', password: '' });
  };

  // Helper function to dynamically combine styles
  const getStyle = (baseStyle, isTrue, hoverStyle) => {
    return { 
      ...baseStyle, 
      ...(isTrue ? hoverStyle : {}),
      transition: 'none', 
    };
  };

  return (
    <div style={styles.container}>
      {/* Removed onMouseEnter/onMouseLeave from card */}
      <div style={styles.card}>
        <h2 style={styles.title}>
          {isSignIn ? 'Welcome Back! 👋' : 'Create Account 🚀'}
        </h2>

        <form onSubmit={isSignIn ? handleSignIn : handleSignUp}>
          
          {/* Username Field */}
          {!isSignIn && (
            <div style={styles.formGroup}>
              <label htmlFor="username" style={styles.label}>Username</label>
              <input 
                type="text" 
                id="username" 
                name="username"
                value={formData.username}
                onChange={handleChange}
                style={getStyle(styles.input, focusedInput === 'username', styles.inputFocus)}
                onFocus={() => setFocusedInput('username')}
                onBlur={() => setFocusedInput(null)}
                placeholder="Choose a username"
                required={!isSignIn}
              />
            </div>
          )}
          
          {/* Email Field */}
          <div style={styles.formGroup}>
            <label htmlFor="email" style={styles.label}>Email Address</label>
            <input 
              type="email" 
              id="email" 
              name="email"
              value={formData.email}
              onChange={handleChange}
              style={getStyle(styles.input, focusedInput === 'email', styles.inputFocus)}
              onFocus={() => setFocusedInput('email')}
              onBlur={() => setFocusedInput(null)}
              placeholder="you@example.com"
              required
            />
          </div>

          {/* Password Field */}
          <div style={styles.formGroup}>
            <label htmlFor="password" style={styles.label}>Password</label>
            <input 
              type="password" 
              id="password" 
              name="password"
              value={formData.password}
              onChange={handleChange}
              style={getStyle(styles.input, focusedInput === 'password', styles.inputFocus)}
              onFocus={() => setFocusedInput('password')}
              onBlur={() => setFocusedInput(null)}
              placeholder="Enter your password"
              required
            />
          </div>

          {/* Submit Button */}
          <button 
            type="submit" 
            style={getStyle(styles.submitButton, isSubmitHovered, styles.submitButtonHover)}
            onMouseEnter={() => setIsSubmitHovered(true)}
            onMouseLeave={() => setIsSubmitHovered(false)}
          >
            {isSignIn ? 'Sign In' : 'Sign Up'}
          </button>
        </form>

        <div style={styles.toggleText}>
          {isSignIn ? "Don't have an account?" : "Already have an account?"}
          <button 
            type="button" 
            onClick={toggleMode} 
            style={getStyle(styles.toggleButton, isToggleHovered, styles.toggleButtonHover)}
            onMouseEnter={() => setIsToggleHovered(true)}
            onMouseLeave={() => setIsToggleHovered(false)}
          >
            {isSignIn ? 'Sign Up' : 'Sign In'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthScreen;