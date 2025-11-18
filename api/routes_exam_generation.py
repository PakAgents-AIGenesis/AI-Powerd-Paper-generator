# api/routes_exam_generation.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
import uuid
import sys
from pathlib import Path

# Add services to path
sys.path.append(str(Path(__file__).parent.parent / "services"))

try:
    from services.exam_service import exam_service
except ImportError as e:
    print(f"Warning: Could not import exam_service: {e}")
    # Create a mock service for development
    class MockExamService:
        def initialize_controller(self):
            return False
        def generate_exam_from_pdf(self, **kwargs):
            return {"success": False, "error": "Exam service not available"}
    exam_service = MockExamService()

router = APIRouter()

@router.post("/generate-exam")
async def generate_exam_from_pdf(
    pdf_file: UploadFile = File(...),
    query: str = Form("general topics"),
    mcq_count: int = Form(10),
    short_count: int = Form(5),
    long_count: int = Form(2),
    total_marks: int = Form(100)
):
    """
    Generate exam paper from uploaded PDF
    """
    try:
        # Validate file type
        if not pdf_file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Create temporary upload directory
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(pdf_file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        pdf_path = os.path.join(temp_dir, unique_filename)
        
        # Save uploaded file
        with open(pdf_path, "wb") as f:
            content = await pdf_file.read()
            f.write(content)
        
        # Generate exam
        result = exam_service.generate_exam_from_pdf(
            pdf_path=pdf_path,
            query=query,
            mcq_count=mcq_count,
            short_count=short_count,
            long_count=long_count,
            total_marks=total_marks
        )
        
        # Clean up temporary file
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception as e:
            print(f"Warning: Could not delete temp file {pdf_path}: {e}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exam generation failed: {str(e)}")

@router.get("/exam-service-status")
def get_exam_service_status():
    """Check if exam generation service is available"""
    try:
        if exam_service.initialize_controller():
            return {
                "status": "available",
                "message": "Exam generation service is ready"
            }
        else:
            return {
                "status": "unavailable", 
                "message": "Exam generation service failed to initialize"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Service check failed: {str(e)}"
        }

@router.post("/test-exam-generation")
async def test_exam_generation():
    """
    Test endpoint with sample data
    """
    try:
        # You can create a sample PDF for testing or use an existing one
        sample_pdf_path = "sample.pdf"  # Make sure this exists for testing
        
        if not os.path.exists(sample_pdf_path):
            return {
                "success": False,
                "error": "Sample PDF not found for testing",
                "note": "Place a sample.pdf file in the root directory for testing"
            }
        
        result = exam_service.generate_exam_from_pdf(
            pdf_path=sample_pdf_path,
            query="artificial intelligence and machine learning",
            mcq_count=5,
            short_count=3,
            long_count=1,
            total_marks=50
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")