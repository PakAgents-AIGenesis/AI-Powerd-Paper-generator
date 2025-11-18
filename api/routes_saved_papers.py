# api/routes/saved_papers.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional
from pydantic import BaseModel
from pathlib import Path
import json
import uuid
from datetime import datetime

router = APIRouter()

SAVE_FILE = Path("saved_papers.json")
GENERATED_PAPER_FILE = Path("latest_generated_paper.json")

# Ensure files exist
SAVE_FILE.touch(exist_ok=True)
GENERATED_PAPER_FILE.touch(exist_ok=True)

# Extended Pydantic Model with content support
class Paper(BaseModel):
    id: int
    title: str
    level: str
    date: str
    content: Optional[str] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    questions: Optional[str] = None

class GeneratedPaper(BaseModel):
    id: int
    title: str
    level: str
    date: str
    content: Optional[str] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    questions: Optional[str] = None

# --- Get all saved papers ---
@router.get("/saved-papers", response_model=List[Paper])
async def get_saved_papers():
    with open(SAVE_FILE, "r") as f:
        try:
            data = json.load(f)
        except:
            data = []
    return data

# --- Save new paper ---
@router.post("/saved-papers")
async def save_paper(paper: Paper):
    with open(SAVE_FILE, "r+") as f:
        try:
            data = json.load(f)
        except:
            data = []
        
        # Check if paper with same ID already exists
        paper_exists = any(p.get('id') == paper.id for p in data)
        if paper_exists:
            raise HTTPException(status_code=400, detail="Paper with this ID already exists")
        
        data.append(paper.dict())
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    
    return JSONResponse({"message": "Paper saved successfully!"})

# --- Get latest generated paper ---
@router.get("/latest-paper")
async def get_latest_paper():
    try:
        with open(GENERATED_PAPER_FILE, "r") as f:
            try:
                data = json.load(f)
                if data:
                    return data
                else:
                    raise HTTPException(status_code=404, detail="No generated paper found")
            except json.JSONDecodeError:
                raise HTTPException(status_code=404, detail="No generated paper found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No generated paper found")

# --- Save generated paper (for when paper is generated) ---
@router.post("/save-generated-paper")
async def save_generated_paper(paper: GeneratedPaper):
    try:
        with open(GENERATED_PAPER_FILE, "w") as f:
            json.dump(paper.dict(), f, indent=4)
        return JSONResponse({"message": "Generated paper saved successfully!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save generated paper: {str(e)}")

# --- Download paper as PDF (placeholder - returns JSON for now) ---
@router.post("/download-paper")
async def download_paper(paper: Paper):
    try:
        # For now, we'll return a JSON response since PDF generation requires additional libraries
        # In production, you would use libraries like reportlab, weasyprint, or pdfkit
        return JSONResponse({
            "message": "PDF download functionality",
            "paper": paper.dict(),
            "note": "PDF generation would be implemented here with libraries like reportlab or weasyprint"
        })
        
        # Example of actual PDF implementation (commented out):
        # pdf_content = generate_pdf(paper.dict())
        # return Response(
        #     content=pdf_content,
        #     media_type="application/pdf",
        #     headers={"Content-Disposition": f"attachment; filename={paper.title}.pdf"}
        # )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

# --- Get specific paper by ID ---
@router.get("/paper/{paper_id}")
async def get_paper_by_id(paper_id: int):
    with open(SAVE_FILE, "r") as f:
        try:
            data = json.load(f)
        except:
            data = []
    
    paper = next((p for p in data if p.get('id') == paper_id), None)
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    return paper

# --- Delete paper by ID ---
@router.delete("/paper/{paper_id}")
async def delete_paper(paper_id: int):
    with open(SAVE_FILE, "r+") as f:
        try:
            data = json.load(f)
        except:
            data = []
        
        initial_length = len(data)
        data = [p for p in data if p.get('id') != paper_id]
        
        if len(data) == initial_length:
            raise HTTPException(status_code=404, detail="Paper not found")
        
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    
    return JSONResponse({"message": "Paper deleted successfully!"})

# --- Update the generate-paper endpoint to also save as latest generated paper ---
@router.post("/generate-paper")
async def generate_paper_endpoint(paper_data: dict):
    try:
        # Your existing paper generation logic here
        # ...
        
        # Create a paper object from the generated data
        generated_paper = GeneratedPaper(
            id=paper_data.get('id', int(datetime.now().timestamp())),
            title=paper_data.get('paperHeading', 'Generated Paper'),
            level=paper_data.get('difficulty', 'Mixed'),
            date=datetime.now().strftime("%Y-%m-%d"),
            content=paper_data.get('content', ''),
            subject=paper_data.get('subject', 'General'),
            topic=paper_data.get('topic', 'Various Topics'),
            questions=paper_data.get('questions', '')
        )
        
        # Save as latest generated paper
        with open(GENERATED_PAPER_FILE, "w") as f:
            json.dump(generated_paper.dict(), f, indent=4)
        
        return JSONResponse({
            "message": "Paper generated successfully!",
            "paper": generated_paper.dict()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate paper: {str(e)}")