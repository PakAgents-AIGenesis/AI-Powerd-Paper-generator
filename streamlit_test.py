# streamlit_test.py
import streamlit as st
import requests
import json
import io
import base64
from typing import Dict, Any

# ✅ UPDATED: Production Backend URL - Replace with your actual Render URL
BASE_URL = "https://your-backend-name.onrender.com"  # 🔄 YAHAN APNA ACTUAL RENDER URL DALEN

def main():
    st.set_page_config(page_title="Exam Generator Test", page_icon="📝", layout="wide")
    
    st.title("🎓 Exam Generator Testing Dashboard")
    st.markdown("Test your FastAPI backend through Streamlit")
    
    # ✅ ADDED: Backend status display
    display_backend_status()
    
    # Sidebar for API status
    with st.sidebar:
        st.header("API Status")
        if st.button("Check API Status"):
            check_api_status()
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Generate Paper", 
        "📊 Service Status", 
        "🔍 Test Endpoints",
        "📋 Saved Papers"
    ])
    
    with tab1:
        test_paper_generation()
    
    with tab2:
        test_service_status()
    
    with tab3:
        test_other_endpoints()
    
    with tab4:
        view_saved_papers()

# ✅ ADDED: Backend status function
def display_backend_status():
    """Display backend connection status"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            st.success(f"✅ Backend Connected: {BASE_URL}")
        else:
            st.error(f"❌ Backend Error: Status {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error(f"🚫 Cannot connect to backend at: {BASE_URL}")
        st.info("""
        **Please ensure:**
        1. Backend is deployed on Render.com
        2. Correct URL is set in BASE_URL
        3. Backend service is running
        """)
    except requests.exceptions.Timeout:
        st.warning("⏰ Backend is slow to respond (Render free tier)")

def check_api_status():
    """Check if FastAPI backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            st.sidebar.success("✅ Backend is running!")
            return True
        else:
            st.sidebar.error(f"❌ Backend returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        st.sidebar.error(f"❌ Cannot connect to backend at: {BASE_URL}")
        st.sidebar.info("Deploy backend on Render.com first")
        return False
    except requests.exceptions.Timeout:
        st.sidebar.warning("⏰ Backend timeout - may be starting up")
        return True

def test_paper_generation():
    """Test the paper generation endpoint"""
    st.header("📄 Generate Exam Paper")
    
    # ✅ ADDED: Backend check before showing form
    if not check_api_status():
        st.error("🚫 Backend not available. Please deploy backend first.")
        return
    
    with st.form("paper_generation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            paper_heading = st.text_input("Paper Heading", "Computer Science Exam")
            total_marks = st.number_input("Total Marks", min_value=10, max_value=200, value=30)
            
            st.subheader("Question Counts")
            mcq_count = st.number_input("MCQ Count", min_value=0, max_value=20, value=5)
            saq_count = st.number_input("Short Answer Count", min_value=0, max_value=10, value=3)
            laq_count = st.number_input("Long Answer Count", min_value=0, max_value=5, value=2)
        
        with col2:
            st.subheader("Difficulty Levels")
            mcq_difficulty = st.selectbox("MCQ Difficulty", ["easy", "medium", "hard"], index=1)
            saq_difficulty = st.selectbox("Short Answer Difficulty", ["easy", "medium", "hard"], index=1)
            laq_difficulty = st.selectbox("Long Answer Difficulty", ["easy", "medium", "hard"], index=1)
            
            st.subheader("Student Info")
            include_roll = st.checkbox("Include Roll Number", value=True)
            include_name = st.checkbox("Include Name", value=True)
            include_class = st.checkbox("Include Class/Section", value=True)
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload PDF Files", 
            type=["pdf"], 
            accept_multiple_files=True,
            help="Upload one or more PDF files for content extraction"
        )
        
        submitted = st.form_submit_button("🚀 Generate Exam Paper")
        
        if submitted:
            if not uploaded_files:
                st.error("Please upload at least one PDF file")
                return
            
            generate_paper(
                paper_heading, total_marks,
                include_roll, include_name, include_class,
                mcq_count, saq_count, laq_count,
                mcq_difficulty, saq_difficulty, laq_difficulty,
                uploaded_files
            )

def generate_paper(paper_heading, total_marks, include_roll, include_name, include_class,
                  mcq_count, saq_count, laq_count, mcq_difficulty, saq_difficulty, laq_difficulty,
                  uploaded_files):
    """Call the paper generation API"""
    
    with st.spinner("🔄 Generating exam paper..."):
        try:
            # Prepare files and form data
            files = []
            for uploaded_file in uploaded_files:
                files.append(("files", (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")))
            
            data = {
                "paperHeading": paper_heading,
                "totalMarks": total_marks,
                "includeRollNumber": str(include_roll).lower(),
                "includeName": str(include_name).lower(),
                "includeClassSection": str(include_class).lower(),
                "mcqCount": mcq_count,
                "mcqDifficulty": mcq_difficulty,
                "saqCount": saq_count,
                "saqDifficulty": saq_difficulty,
                "laqCount": laq_count,
                "laqDifficulty": laq_difficulty
            }
            
            # ✅ UPDATED: Increased timeout for Render free tier
            response = requests.post(
                f"{BASE_URL}/api/generate-paper",
                files=files,
                data=data,
                timeout=30  # Increased timeout for slow free tier
            )
            
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Paper generated successfully!")
                
                # Display results
                display_generation_results(result)
                
                # Show download option
                if st.button("📥 Download Generated Paper"):
                    download_generated_paper()
                    
            else:
                st.error(f"❌ API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            st.error("⏰ Request timeout - Backend is slow (Render free tier)")
        except requests.exceptions.ConnectionError:
            st.error("🚫 Cannot connect to backend. Please check your BASE_URL")
        except Exception as e:
            st.error(f"❌ Error generating paper: {str(e)}")

# ... (Rest of your functions remain the same, just ensure they use BASE_URL)

def download_generated_paper():
    """Download the generated paper as PDF"""
    try:
        # Get latest paper data
        paper_response = requests.get(f"{BASE_URL}/api/latest-paper", timeout=10)
        if paper_response.status_code == 200:
            paper_data = paper_response.json()
            
            # Call download endpoint
            download_response = requests.post(
                f"{BASE_URL}/api/download-paper",
                json=paper_data,
                timeout=30
            )
            
            if download_response.status_code == 200:
                # Create download link
                pdf_data = download_response.content
                b64_pdf = base64.b64encode(pdf_data).decode()
                
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="generated_paper.pdf">📥 Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.error("❌ Failed to generate PDF download")
                
    except Exception as e:
        st.error(f"❌ Error downloading paper: {str(e)}")

# ... (Keep all other functions as they are)

if __name__ == "__main__":
    main()
