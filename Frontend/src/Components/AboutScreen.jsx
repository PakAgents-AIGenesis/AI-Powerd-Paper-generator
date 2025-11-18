import React from 'react';

// --- Styles for the About Screen ---
const styles = {
  container: {
    padding: '40px',
    maxWidth: '1000px',
    margin: '0 auto',
    fontFamily: 'Arial, sans-serif',
    color: '#333333', // Dark text color
  },
  header: {
    color: '#008080', // Primary Teal color for branding
    borderBottom: '2px solid #008080',
    paddingBottom: '10px',
    marginBottom: '30px',
    fontSize: '28px',
  },
  sectionTitle: {
    color: '#444444',
    marginTop: '30px',
    marginBottom: '15px',
    fontSize: '22px',
    borderLeft: '4px solid #008080',
    paddingLeft: '10px',
  },
  paragraph: {
    lineHeight: '1.6',
    marginBottom: '15px',
  },
  teamList: {
    listStyleType: 'none',
    paddingLeft: '15px',
    display: 'flex',
    flexWrap: 'wrap',
    gap: '20px',
  },
  teamItem: {
    backgroundColor: '#F5F5F5', // Light gray background
    padding: '12px 18px',
    borderRadius: '8px',
    boxShadow: '0 2px 5px rgba(0, 0, 0, 0.05)',
    fontWeight: '600',
    minWidth: '200px',
  },
  motto: {
    fontStyle: 'italic',
    color: '#006666',
    marginTop: '20px',
    fontSize: '18px',
  },
  thankYou: {
    marginTop: '40px',
    padding: '20px',
    backgroundColor: 'rgba(0, 128, 128, 0.05)', // Very light teal tint
    border: '1px solid rgba(0, 128, 128, 0.1)',
    borderRadius: '10px',
    textAlign: 'center',
    fontWeight: 'bold',
  }
};

const AboutScreen = () => {
  const teamMembers = [
    { name: 'Muhammad Faisal Shahzad Nadeem', role: 'AI Engineer' },
    { name: 'Uma Ammara', role: 'Computer Scientist' },
    { name: 'Muhammad Aashan', role: 'IT Engineer' },
    { name: 'Raqeeba Yasin', role: 'Computer Scientist' },
    { name: 'Poise_Ravencnql', role: 'Team Member' },
    { name: 'Rimsha Rani', role: 'Computer Scientist' },
  ];

  return (
    <div style={styles.container}>
      
      <h1 style={styles.header}>ⓘ About the Project: Paper Generator</h1>

      <p style={styles.paragraph}>
        The **Paper Generator** is an innovative solution built to empower educators by automating the creation of customized, high-quality question papers and quizzes using state-of-the-art Artificial Intelligence. Our mission is to save valuable time for teachers, allowing them to focus more on student interaction and learning outcomes.
      </p>

      <h2 style={styles.sectionTitle}>Meet the Team: PakAgents 🇵🇰</h2>
      <p style={styles.motto}>
        *Motto: “Building intelligent agents — empowering intelligent nations.”*
      </p>
      
      <p style={styles.paragraph}>
        This project was collaboratively developed by **Team PakAgents**, a group of passionate innovators dedicated to leveraging AI for social impact, especially in the education sector.
      </p>

      <ul style={styles.teamList}>
        {teamMembers.map((member, index) => (
          <li key={index} style={styles.teamItem}>
            {member.name}
            <div style={{ fontSize: '12px', color: '#008080', fontWeight: 'normal', marginTop: '3px' }}>
              {member.role}
            </div>
          </li>
        ))}
      </ul>
      
      <h2 style={styles.sectionTitle}>Our Gratitude</h2>

      <div style={styles.thankYou}>
        <p style={{ margin: 0 }}>
          We extend our sincere thanks to **LabLab.ai** for providing the incredible opportunity to showcase our talent and develop this project during the **AI Genesis Hackathon**.
          The platform and resources were instrumental in bringing the Paper Generator to life.
        </p>
      </div>

    </div>
  );
};

export default AboutScreen;