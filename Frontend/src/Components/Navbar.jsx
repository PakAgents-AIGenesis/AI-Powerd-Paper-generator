import React, { useState } from 'react';
// We'll use simple text for the menu icon since we are removing dependencies like lucide-react
// import { Menu, X } from 'lucide-react'; 

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const navLinks = [
    { name: "Home", href: "#home" },
    { name: "Features", href: "#features" },
    { name: "Pricing", href: "#pricing" },
    { name: "How It Works", href: "#how-it-works" },
  ];

  // Define styles as JavaScript objects
  const styles = {
    // General styles
    navContainer: {
      backgroundColor: '#fff',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
      position: 'sticky',
      top: 0,
      zIndex: 50,
    },
    innerContainer: {
      maxWidth: '1280px', // Equivalent to max-w-7xl
      margin: '0 auto',
      padding: '0 1rem', // Equivalent to px-4
      // You'll need media queries for responsive padding, but inline styles are limited here.
    },
    flexRow: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      height: '4rem', // Equivalent to h-16
    },
    // Logo styles
    logo: {
      fontSize: '1.5rem',
      fontWeight: '800',
      color: '#4f46e5', // Indigo-700
      textDecoration: 'none',
    },
    // Desktop Link styles
    desktopLinks: {
      display: 'flex',
      alignItems: 'center',
      gap: '1.5rem', // space-x-6
    },
    linkItem: {
      color: '#4b5563', // Gray-600
      padding: '0.5rem 0.75rem',
      borderRadius: '0.375rem',
      fontSize: '1rem',
      fontWeight: '500',
      transition: 'all 150ms ease-in-out',
      textDecoration: 'none',
      cursor: 'pointer',
      // Note: Inline styles cannot easily handle :hover pseudo-classes
    },
    // CTA Button styles
    ctaButton: {
      backgroundColor: '#4f46e5', // Indigo-600
      color: '#fff',
      fontWeight: '600',
      padding: '0.5rem 1rem',
      borderRadius: '0.5rem',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)',
      border: 'none',
      cursor: 'pointer',
      transition: 'all 200ms ease-in-out',
    },
    // Mobile Button styles
    mobileButton: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '0.5rem',
      borderRadius: '0.375rem',
      color: '#6b7280', // Gray-500
      backgroundColor: 'transparent',
      border: 'none',
      cursor: 'pointer',
      transition: 'all 150ms ease-in-out',
    },
    // Mobile Menu styles
    mobileMenu: {
      padding: '0.5rem 0',
      borderTop: '1px solid #e5e7eb',
    },
    mobileLinkItem: {
      color: '#374151', // Gray-700
      display: 'block',
      padding: '0.5rem 0.75rem',
      borderRadius: '0.375rem',
      fontSize: '1rem',
      fontWeight: '500',
      textDecoration: 'none',
      cursor: 'pointer',
    }
  };

  return (
    <nav style={styles.navContainer}>
      <div style={styles.innerContainer}>
        <div style={styles.flexRow}>

          {/* Logo/Project Name */}
          <div style={{ flexShrink: 0 }}>
            <a href="#" style={styles.logo}>
              AI-Paper <span style={{ fontWeight: '400', color: '#6b7280' }}>& Notes</span>
            </a>
          </div>

          {/* Desktop Navigation Links (Simulating 'hidden md:block' with a size check) */}
          {/* Note: In pure inline React, handling responsiveness like this requires complex JS/Hooks */}
          <div className="hidden-on-mobile-flex" style={{ display: window.innerWidth > 768 ? 'flex' : 'none' }}> 
            <div style={styles.desktopLinks}>
              {navLinks.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  style={styles.linkItem}
                >
                  {item.name}
                </a>
              ))}
            </div>
          </div>

          {/* Call to Action Button (Desktop) */}
          <div className="hidden-on-mobile" style={{ display: window.innerWidth > 768 ? 'block' : 'none' }}>
            <button style={styles.ctaButton}>
              Get Started for Free
            </button>
          </div>

          {/* Mobile Menu Button (Visible on small screens) */}
          <div className="visible-on-mobile" style={{ display: window.innerWidth <= 768 ? 'flex' : 'none' }}>
            <button
              onClick={() => setIsOpen(!isOpen)}
              type="button"
              style={styles.mobileButton}
              aria-controls="mobile-menu"
              aria-expanded={isOpen}
            >
              <span style={{ fontSize: '0.75rem', position: 'absolute', clip: 'rect(0 0 0 0)', width: 1, height: 1 }}>Open main menu</span>
              <span style={{ fontSize: '1.5rem' }}>{isOpen ? '✕' : '☰'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Content (Dropdown) */}
      <div
        className="mobile-menu-content"
        style={{
          display: (isOpen && window.innerWidth <= 768) ? 'block' : 'none',
          ...styles.mobileMenu
        }}
        id="mobile-menu"
      >
        <div style={{ padding: '0 0.5rem', paddingBottom: '0.75rem' }}>
          {navLinks.map((item) => (
            <a
              key={item.name}
              href={item.href}
              onClick={() => setIsOpen(false)}
              style={styles.mobileLinkItem}
            >
              {item.name}
            </a>
          ))}
          {/* Mobile CTA Button */}
          <div style={{ paddingTop: '1rem' }}>
            <button style={{ ...styles.ctaButton, width: '100%' }}>
              Get Started for Free
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;