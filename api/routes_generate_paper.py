# api/routes_generate_paper.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import shutil
from datetime import datetime
import io
import re
import random
import sys
import os

# Add the current directory to Python path to find your modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

router = APIRouter()

# Folder to save uploaded files
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

# Maximum allowed files
MAX_FILES = 10

# Pydantic Model for Download Paper
class DownloadPaperRequest(BaseModel):
    id: int
    title: str
    level: str
    date: str
    content: Optional[str] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    questions: Optional[str] = None
    total_marks: Optional[int] = None
    mcq_count: Optional[int] = None
    saq_count: Optional[int] = None
    laq_count: Optional[int] = None

# Store latest paper in router state
def get_latest_paper_storage():
    if not hasattr(router, 'latest_generated_paper'):
        router.latest_generated_paper = None
    return router.latest_generated_paper

def set_latest_paper_storage(paper):
    router.latest_generated_paper = paper

# --- Import your Gemini AI system ---
try:
    # FIX: Use the unified exam service instead of direct Gemini imports
    from services.exam_service import exam_service
    GEMINI_AVAILABLE = True
    print("✅ Successfully imported unified exam service")
except ImportError as e:
    print(f"❌ Failed to import exam service: {e}")
    GEMINI_AVAILABLE = False
    # Create fallback service
    class FallbackExamService:
        def generate_exam_from_pdf(self, **kwargs):
            return {"success": False, "error": "Exam service not available"}
    exam_service = FallbackExamService()

# --- IMPROVED PDF Extraction Functions ---
def extract_text_from_pdf_enhanced(file_path):
    """Enhanced PDF text extraction with better debugging"""
    try:
        import fitz
        print(f"🔍 Extracting from PDF: {file_path}")
        
        doc = fitz.open(file_path)
        full_text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            
            if page_text and page_text.strip():
                # Clean the text - remove excessive whitespace
                cleaned_text = re.sub(r'\s+', ' ', page_text.strip())
                full_text += f"\n{cleaned_text}"
                print(f"✅ Page {page_num + 1}: {len(cleaned_text)} chars")
            else:
                print(f"❌ Page {page_num + 1}: No text found")
        
        doc.close()
        
        if not full_text.strip():
            print("❌ DEBUG: No text could be extracted from PDF")
            return ""
        
        print(f"✅ DEBUG: Total extracted: {len(full_text)} characters")
        return full_text
        
    except Exception as e:
        print(f"❌ DEBUG: PDF extraction error: {e}")
        return f"Error extracting text from PDF: {str(e)}"

def extract_text_from_file_enhanced(file_path):
    """Enhanced file text extraction"""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"❌ DEBUG: File not found: {file_path}")
            return f"File not found: {file_path}"
            
        if file_path.suffix.lower() == '.pdf':
            return extract_text_from_pdf_enhanced(str(file_path))
        else:
            print(f"❌ DEBUG: Unsupported file type: {file_path.suffix}")
            return f"Unsupported file type: {file_path.suffix}"
            
    except Exception as e:
        print(f"❌ DEBUG: File processing error: {e}")
        return f"Error reading file: {str(e)}"

# --- IMPROVED Content Processing Functions ---
def extract_meaningful_content(content):
    """Extract meaningful sentences and concepts with better filtering"""
    print("🔍 Extracting meaningful content...")
    
    if not content or "Error:" in content:
        print("❌ No content or error in content")
        return [], []
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', content)
    
    meaningful_sentences = []
    key_concepts = set()
    
    for sentence in sentences:
        clean_sentence = sentence.strip()
        # More strict filtering to get only quality content
        if (len(clean_sentence) > 40 and
            len(clean_sentence) < 300 and
            len(clean_sentence.split()) >= 8 and
            not any(word in clean_sentence.lower() for word in [
                'page', 'chapter', 'figure', 'table', 'copyright',
                'confidential', 'error', 'no text', 'unsupported'
            ]) and
            re.search(r'[a-zA-Z]', clean_sentence)):  # Must contain letters
            
            meaningful_sentences.append(clean_sentence)
            
            # Extract key concepts (capitalized phrases)
            concepts = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', clean_sentence)
            for concept in concepts:
                if len(concept) > 3 and concept not in ['The', 'This', 'That', 'These', 'Those']:
                    key_concepts.add(concept)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_sentences = []
    for sentence in meaningful_sentences:
        if sentence not in seen:
            seen.add(sentence)
            unique_sentences.append(sentence)
    
    concepts_list = list(key_concepts)
    
    print(f"📝 Found {len(unique_sentences)} meaningful sentences and {len(concepts_list)} key concepts")
    return unique_sentences[:50], concepts_list[:20]

def prepare_chunks_for_gemini(content):
    """Prepare content chunks for question generation"""
    sentences, concepts = extract_meaningful_content(content)
    
    # Group sentences into meaningful chunks (3-5 sentences each)
    chunks = []
    current_chunk = []
    
    for sentence in sentences:
        current_chunk.append(sentence)
        if len(current_chunk) >= 3:  # 3 sentences per chunk
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    
    # Add remaining sentences
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    print(f"📦 Prepared {len(chunks)} chunks for question generation")
    return chunks

# --- UNIFIED QUESTION GENERATION ---
def generate_questions_with_service(chunks, mcq_count, saq_count, laq_count, difficulty, paper_heading):
    """Generate questions using the unified exam service"""
    print("🚀 USING UNIFIED EXAM SERVICE FOR QUESTION GENERATION")
    
    try:
        # Save chunks to a temporary PDF for processing
        temp_pdf_path = "temp_content.pdf"
        
        # Create a simple text representation (in real implementation, you'd create an actual PDF)
        with open(temp_pdf_path, 'w', encoding='utf-8') as f:
            f.write(f"# {paper_heading}\n\n")
            for i, chunk in enumerate(chunks):
                f.write(f"## Chunk {i+1}\n{chunk}\n\n")
        
        # Use the exam service
        result = exam_service.generate_exam_from_pdf(
            pdf_path=temp_pdf_path,
            query=paper_heading,
            mcq_count=mcq_count,
            short_count=saq_count,
            long_count=laq_count,
            total_marks=(mcq_count * 1 + saq_count * 3 + laq_count * 5)
        )
        
        # Clean up temp file
        try:
            os.remove(temp_pdf_path)
        except:
            pass
        
        if result.get("success"):
            exam_data = result.get("exam", {})
            questions_text = format_exam_questions(exam_data)
            print(f"✅ Unified service generated questions successfully")
            return questions_text
        else:
            print(f"❌ Unified service failed: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Unified service generation failed: {e}")
        return None

def format_exam_questions(exam_data):
    """Format exam questions into text format"""
    questions_text = ""
    question_number = 1
    
    # MCQs from Section A
    mcq_section = exam_data.get("Section A: Multiple Choice Questions", {})
    mcq_questions = mcq_section.get("questions", [])
    
    if mcq_questions:
        questions_text += f"**SECTION A: MULTIPLE CHOICE QUESTIONS** ({len(mcq_questions)} questions - {len(mcq_questions)} marks)\n\n"
        for mcq in mcq_questions:
            questions_text += f"{question_number}. {mcq.get('question', 'Question')}\n"
            options = mcq.get('options', ['Option A', 'Option B', 'Option C', 'Option D'])
            for i, option in enumerate(options):
                questions_text += f"   {chr(97+i)}) {option}\n"
            questions_text += "\n"
            question_number += 1
    
    # Short Answer Questions from Section B
    short_section = exam_data.get("Section B: Short Answer Questions", {})
    short_questions = short_section.get("questions", [])
    
    if short_questions:
        questions_text += f"**SECTION B: SHORT ANSWER QUESTIONS** ({len(short_questions)} questions - {len(short_questions) * 3} marks)\n\n"
        for saq in short_questions:
            questions_text += f"{question_number}. {saq.get('question', 'Question')} ({3} marks)\n\n"
            question_number += 1
    
    # Long Answer Questions from Section C  
    long_section = exam_data.get("Section C: Long Answer Questions", {})
    long_questions = long_section.get("questions", [])
    
    if long_questions:
        questions_text += f"**SECTION C: LONG ANSWER QUESTIONS** ({len(long_questions)} questions - {len(long_questions) * 5} marks)\n\n"
        for laq in long_questions:
            questions_text += f"{question_number}. {laq.get('question', 'Question')} ({5} marks)\n\n"
            question_number += 1
    
    return questions_text

# --- ENHANCED FALLBACK QUESTION GENERATION ---
def generate_enhanced_fallback_questions(content, mcq_count, saq_count, laq_count, difficulty):
    """Enhanced fallback question generation with variety"""
    print("🔄 Using ENHANCED fallback question generation")
    
    sentences, concepts = extract_meaningful_content(content)
    
    if len(sentences) < 3:
        return None
    
    questions = ""
    question_number = 1
    
    # Shuffle for variety
    random.shuffle(sentences)
    random.shuffle(concepts)
    
    # Generate VARIED MCQs
    if mcq_count > 0:
        questions += f"**SECTION A: MULTIPLE CHOICE QUESTIONS** ({mcq_count} questions - {mcq_count} marks)\n\n"
        
        question_types = [
            "What is the PRIMARY purpose of: \"{}\"?",
            "Which statement BEST summarizes: \"{}\"?", 
            "How would you APPLY the concept: \"{}\"?",
            "What can be INFERRED from: \"{}\"?",
            "What is the key CHARACTERISTIC in: \"{}\"?"
        ]
        
        option_templates = [
            ["To achieve the main objective described", "For documentation purposes only", "As a secondary supporting function", "For entertainment value"],
            ["As clearly explained in the material", "A common misconception", "Only partially correct", "Not covered in the text"],
            ["In practical scenarios as outlined", "Only in theoretical frameworks", "With significant modifications", "It has no practical application"],
            ["The logical conclusion supported by evidence", "An assumption not supported", "A contradictory viewpoint", "An irrelevant detail"],
            ["The defining feature mentioned", "A minor attribute", "An external characteristic", "An incorrect assumption"]
        ]
        
        for i in range(min(mcq_count, len(sentences))):
            sentence = sentences[i]
            clean_sentence = re.sub(r'\s+', ' ', sentence).strip()
            
            # Select random question type and options
            question_template = random.choice(question_types)
            options = random.choice(option_templates)
            question = question_template.format(clean_sentence[:80])
            
            questions += f"{question_number}. {question}\n"
            
            for j, option in enumerate(options):
                questions += f"   {chr(97+j)}) {option}\n"
            questions += "\n"
            question_number += 1
    
    # Generate VARIED SAQs
    if saq_count > 0:
        questions += f"**SECTION B: SHORT ANSWER QUESTIONS** ({saq_count} questions - {saq_count * 3} marks)\n\n"
        
        saq_types = [
            "Explain the SIGNIFICANCE of: \"{}\"",
            "How would you IMPLEMENT: \"{}\"?", 
            "ANALYZE the importance of: \"{}\"",
            "DESCRIBE the process in: \"{}\""
        ]
        
        for i in range(min(saq_count, len(sentences) - mcq_count)):
            sentence = sentences[i + mcq_count]
            clean_sentence = re.sub(r'\s+', ' ', sentence).strip()
            
            saq_template = random.choice(saq_types)
            question = saq_template.format(clean_sentence[:100])
            
            questions += f"{question_number}. {question} (3 marks)\n\n"
            question_number += 1
    
    # Generate MEANINGFUL LAQs
    if laq_count > 0:
        questions += f"**SECTION C: LONG ANSWER QUESTIONS** ({laq_count} questions - {laq_count * 5} marks)\n\n"
        
        laq_types = [
            "Compare and contrast '{}' and '{}' with specific examples from the study material. Discuss their applications and practical significance.",
            "Write a comprehensive analysis of '{}' covering its principles, applications, and importance as explained in the text. Provide detailed examples.",
            "Evaluate the impact and relevance of '{}' in the context of the course material, supporting your analysis with specific references."
        ]
        
        for i in range(min(laq_count, len(concepts))):
            if i + 1 < len(concepts):
                question = random.choice(laq_types).format(concepts[i], concepts[i+1])
            else:
                question = random.choice(laq_types).format(concepts[i])
            
            questions += f"{question_number}. {question} (5 marks)\n\n"
            question_number += 1
    
    return questions

def generate_sample_questions(mcq_count, saq_count, laq_count, mcq_diff, saq_diff, laq_diff):
    """Generate sample questions as last resort"""
    print("📝 GENERATING SAMPLE QUESTIONS (LAST RESORT)")
    questions_content = ""
    question_number = 1
    
    if mcq_count > 0:
        questions_content += f"SECTION A: MULTIPLE CHOICE QUESTIONS ({mcq_count} questions - {mcq_count} marks)\n\n"
        for i in range(mcq_count):
            questions_content += f"{question_number}. Sample {mcq_diff} level MCQ question {i+1} about course content?\n"
            questions_content += "   a) Correct answer based on material\n   b) Plausible but incorrect option\n   c) Common misconception\n   d) Unrelated concept\n\n"
            question_number += 1
    
    if saq_count > 0:
        questions_content += f"SECTION B: SHORT ANSWER QUESTIONS ({saq_count} questions - {saq_count * 3} marks)\n\n"
        for i in range(saq_count):
            questions_content += f"{question_number}. Explain {saq_diff.lower()} level concept {i+1} as covered in the course material. (3 marks)\n\n"
            question_number += 1
    
    if laq_count > 0:
        questions_content += f"SECTION C: LONG ANSWER QUESTIONS ({laq_count} questions - {laq_count * 5} marks)\n\n"
        for i in range(laq_count):
            questions_content += f"{question_number}. Write comprehensive answer on {laq_diff.lower()} level topic {i+1} demonstrating deep understanding of course concepts. (5 marks)\n\n"
            question_number += 1
    
    return questions_content

# --- FIXED PDF Generation Function ---
def generate_pdf_content(paper_data):
    """Generate PDF content - FIXED version"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 100, paper_data['title'])
        
        # Details
        p.setFont("Helvetica", 12)
        y_position = height - 150
        
        details = [
            f"Subject: {paper_data.get('subject', 'General')}",
            f"Level: {paper_data.get('level', 'Mixed')}",
            f"Date: {paper_data.get('date', 'N/A')}",
            f"Total Marks: {paper_data.get('total_marks', 'N/A')}",
        ]
        
        for detail in details:
            p.drawString(100, y_position, detail)
            y_position -= 25
        
        y_position -= 30
        
        # Questions
        if paper_data.get('questions'):
            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, y_position, "QUESTIONS")
            y_position -= 40
            p.setFont("Helvetica", 10)
            
            questions_text = paper_data['questions']
            lines = questions_text.split('\n')
            
            for line in lines:
                if y_position < 100:  # New page if needed
                    p.showPage()
                    p.setFont("Helvetica", 10)
                    y_position = height - 100
                
                if line.strip():
                    # Handle long lines by wrapping
                    if len(line) > 90:
                        p.drawString(100, y_position, line[:90])
                        y_position -= 15
                        if len(line) > 180:
                            p.drawString(100, y_position, line[90:180])
                            y_position -= 15
                            p.drawString(100, y_position, line[180:])
                        else:
                            p.drawString(100, y_position, line[90:])
                    else:
                        p.drawString(100, y_position, line)
                    y_position -= 15
        
        p.save()
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"❌ PDF generation error: {e}")
        # Fallback to text file
        buffer = io.BytesIO()
        content = f"""
{paper_data['title']}
{'=' * 40}

Subject: {paper_data.get('subject', 'General')}
Level: {paper_data.get('level', 'Mixed')}
Date: {paper_data.get('date', 'N/A')}
Total Marks: {paper_data.get('total_marks', 'N/A')}

QUESTIONS:
{paper_data.get('questions', 'No questions generated')}
"""
        buffer.write(content.encode('utf-8'))
        buffer.seek(0)
        return buffer

# --- UPDATED API Endpoints ---
@router.post("/generate-paper")
async def generate_paper(
    paperHeading: str = Form(...),
    totalMarks: int = Form(...),
    includeRollNumber: str = Form(...),
    includeName: str = Form(...),
    includeClassSection: str = Form(...),
    mcqCount: int = Form(...),
    mcqDifficulty: str = Form(...),
    saqCount: int = Form(...),
    saqDifficulty: str = Form(...),
    laqCount: int = Form(...),
    laqDifficulty: str = Form(...),
    files: list[UploadFile] = File(...)
):
    print("=== UNIFIED PAPER GENERATION STARTED ===")
    print(f"Paper Heading: {paperHeading}")
    print(f"Total Marks: {totalMarks}")
    print(f"MCQ: {mcqCount}, SAQ: {saqCount}, LAQ: {laqCount}")

    # Convert string booleans
    includeRollNumber = includeRollNumber.lower() in ("true", "1", "yes")
    includeName = includeName.lower() in ("true", "1", "yes")
    includeClassSection = includeClassSection.lower() in ("true", "1", "yes")

    # Validations
    if totalMarks < 5 or totalMarks > 1000:
        raise HTTPException(status_code=400, detail="Total marks must be between 5 and 1000.")

    if mcqCount == 0 and saqCount == 0 and laqCount == 0:
        raise HTTPException(status_code=400, detail="At least one question type must have count > 0.")

    if len(files) == 0:
        raise HTTPException(status_code=400, detail="At least one file must be uploaded.")

    # Save files
    saved_files = []
    for file in files:
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(str(file_path))
        print(f"💾 Saved file: {file_path}")

    # --- Enhanced Content Extraction ---
    all_extracted_content = ""
    extracted_file_count = 0
    
    print("=== CONTENT EXTRACTION ===")
    for file_path in saved_files:
        print(f"🔍 Processing: {file_path}")
        extracted_text = extract_text_from_file_enhanced(file_path)
        print(f"📊 Extraction result: {len(extracted_text)} chars")
        
        # Enhanced content validation
        if (extracted_text and 
            len(extracted_text.strip()) > 200 and
            "Error:" not in extracted_text and
            "not found" not in extracted_text.lower() and
            "unsupported" not in extracted_text.lower() and
            "no text" not in extracted_text.lower()):
            
            all_extracted_content += f"\n{extracted_text}"
            extracted_file_count += 1
            print(f"✅ Meaningful content extracted")
        else:
            print(f"❌ No meaningful content")
            if extracted_text:
                print(f"   Reason: {extracted_text[:200]}...")

    print(f"📈 Total content length: {len(all_extracted_content)}")
    print(f"📈 Files with content: {extracted_file_count}")

    # --- UNIFIED Question Generation ---
    questions_content = None
    service_used = False
    
    if extracted_file_count > 0 and len(all_extracted_content.strip()) > 200:
        # Prepare chunks for question generation
        chunks = prepare_chunks_for_gemini(all_extracted_content)
        
        if chunks:
            print("🚀 ATTEMPTING UNIFIED SERVICE QUESTION GENERATION")
            # Try unified service first
            questions_content = generate_questions_with_service(
                chunks, mcqCount, saqCount, laqCount, mcqDifficulty, paperHeading
            )
            
            if questions_content:
                service_used = True
                print("🎉 SUCCESS: Unified service questions generated!")
        
        # Enhanced fallback generation
        if not questions_content:
            print("🔄 Unified service failed, using ENHANCED fallback generation")
            questions_content = generate_enhanced_fallback_questions(
                all_extracted_content, mcqCount, saqCount, laqCount, mcqDifficulty
            )
            if questions_content:
                print("✅ Enhanced fallback questions generated")
    
    # Final fallback to samples
    if not questions_content:
        print("❌ All generation failed, using sample questions")
        questions_content = generate_sample_questions(mcqCount, saqCount, laqCount, mcqDifficulty, saqDifficulty, laqDifficulty)

    # Create paper
    paper_data = {
        "id": int(datetime.now().timestamp()),
        "title": paperHeading,
        "level": mcqDifficulty,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "content": f"Paper: {paperHeading}",
        "subject": "Generated Paper",
        "topic": "Custom Exam Paper",
        "questions": questions_content.strip(),
        "total_marks": totalMarks,
        "mcq_count": mcqCount,
        "saq_count": saqCount,
        "laq_count": laqCount,
        "content_based": extracted_file_count > 0,
        "service_used": service_used
    }
    
    set_latest_paper_storage(paper_data)

    response_data = {
        "paperHeading": paperHeading,
        "totalMarks": totalMarks,
        "content_based": extracted_file_count > 0,
        "service_used": service_used,
        "extracted_content_files": extracted_file_count
    }

    print(f"=== PAPER GENERATION COMPLETED ===")
    print(f"🤖 Service Used: {service_used}")
    print(f"📚 Content-based: {extracted_file_count > 0}")
    return JSONResponse({
        "message": "Paper generated successfully!", 
        "paper": response_data,
        "saved_as_latest": True
    })

# Keep other endpoints the same...
@router.get("/latest-paper")
async def get_latest_paper():
    latest_paper = get_latest_paper_storage()
    if latest_paper is None:
        raise HTTPException(status_code=404, detail="No generated paper found. Please generate a paper first.")
    return latest_paper

@router.post("/download-paper")
async def download_paper(paper_request: DownloadPaperRequest):
    try:
        paper_data = paper_request.dict()
        
        # Generate PDF using FIXED function
        pdf_buffer = generate_pdf_content(paper_data)
        
        # Return PDF file
        filename = f"{paper_data['title'].replace(' ', '_')}.pdf"
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        print(f"❌ Download error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

