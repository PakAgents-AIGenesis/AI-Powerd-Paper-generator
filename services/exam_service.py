# services/exam_service.py
import os
import sys
from pathlib import Path
from typing import Dict
from datetime import datetime

# Add the services directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from services.controller import ExamForgeController
except ImportError as e:
    print(f"Import error in exam_service: {e}")
    # Fallback for development
    class ExamForgeController:
        def __init__(self, google_api_key=None, qdrant_url=":memory:"):
            self.initialized = False
        
        def process_pdf(self, file_path: str):
            raise Exception("ExamForgeController not properly initialized")
        
        def generate_exam(self, query: str, counts: Dict, target_total: int = 100) -> Dict:
            raise Exception("ExamForgeController not properly initialized")

class ExamGenerationService:
    def __init__(self):
        # FIX: Use environment variable instead of hardcoded key
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            print("❌ GOOGLE_API_KEY environment variable not set")
            print("💡 Please set it: export GOOGLE_API_KEY='your-actual-key'")
        else:
            print(f"🔑 API Key loaded: {self.api_key[:8]}...")
        
        self.controller = None
        
    def initialize_controller(self):
        """Initialize the exam forge controller"""
        try:
            print("🔄 Initializing ExamForgeController...")
            self.controller = ExamForgeController(google_api_key=self.api_key)
            
            # Check if Gemini is available
            if hasattr(self.controller, 'gemini_ai') and hasattr(self.controller.gemini_ai, 'available'):
                print(f"🤖 Gemini AI Available: {self.controller.gemini_ai.available}")
                if self.controller.gemini_ai.available:
                    print("✅ Gemini AI will be used for question generation")
                else:
                    print("⚠️ Gemini AI not available, using fallback generation")
            else:
                print("❌ Gemini AI initialization failed")
                
            return True
        except Exception as e:
            print(f"❌ Error initializing controller: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_exam_from_pdf(self, pdf_path: str, query: str, 
                             mcq_count: int = 10, short_count: int = 5, 
                             long_count: int = 2, total_marks: int = 100):
        """
        Main method to generate exam from PDF - FIXED VERSION
        """
        try:
            if not self.controller:
                if not self.initialize_controller():
                    return {"success": False, "error": "Failed to initialize exam generator"}
            
            # Step 1: Process PDF and extract content
            print("📄 Processing PDF content...")
            chunks, topics = self.controller.process_pdf(pdf_path)
            print(f"✅ Extracted {len(chunks)} content chunks from PDF")
            
            if not chunks or len(chunks) < 3:
                return {
                    "success": False,
                    "error": "Insufficient content extracted from PDF. Please try a different PDF with more text content."
                }
            
            # Step 2: Use CONTENT-BASED question generation
            print("🎯 Using content-based question generation...")
            counts = {
                'mcq': mcq_count,
                'short': short_count, 
                'long': long_count
            }
            
            # Use the new content-based generation
            if hasattr(self.controller.question_gen, 'generate_questions_from_content'):
                questions = self.controller.question_gen.generate_questions_from_content(
                    chunks, counts, "medium"
                )
            else:
                # Fallback to original method
                questions = self.controller.question_gen.generate_questions(
                    chunks, counts, "medium"
                )
            
            # Create exam structure
            exam = self._create_exam_from_questions(questions, counts, total_marks)
            
            # Check Gemini usage
            gemini_used = getattr(self.controller.gemini_ai, 'available', False) if hasattr(self.controller, 'gemini_ai') else False
            
            return {
                "success": True,
                "exam": exam,
                "topics": topics,
                "chunks_processed": len(chunks),
                "gemini_used": gemini_used,
                "content_based": True,
                "message": f"Exam generated from PDF with {len(chunks)} content chunks"
            }
            
        except Exception as e:
            print(f"❌ Error in exam generation: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }

    def _create_exam_from_questions(self, questions: Dict, counts: Dict, total_marks: int) -> Dict:
        """Create exam structure from generated questions"""
        return {
            "exam_metadata": {
                "total_marks": total_marks,
                "generated_at": str(datetime.now()),
                "content_based": True
            },
            "Section A: Multiple Choice Questions": {
                "instructions": "Choose the correct option for each question",
                "marks_per_question": 1,
                "questions": questions.get('mcq', [])
            },
            "Section B: Short Answer Questions": {
                "instructions": "Answer briefly in 2-3 sentences", 
                "marks_per_question": 3,
                "questions": questions.get('short', [])
            },
            "Section C: Long Answer Questions": {
                "instructions": "Answer in detail with examples",
                "marks_per_question": 5, 
                "questions": questions.get('long', [])
            }
        }

# Singleton instance
exam_service = ExamGenerationService()