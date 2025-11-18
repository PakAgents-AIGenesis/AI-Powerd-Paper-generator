# services/data_ingestion.py
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re

class PDFIngestor:
    def __init__(self, chunk_size=512, chunk_overlap=64):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )

    def extract_text(self, file_path):
        """Extract text from PDF using PyMuPDF"""
        try:
            print(f"🔍 Extracting text from: {file_path}")
            doc = fitz.open(file_path)
            text = ""
            for page_num, page in enumerate(doc):
                try:
                    page_text = page.get_text("text")
                    if page_text.strip():
                        text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                        print(f"✅ Page {page_num + 1}: {len(page_text)} chars")
                except Exception as e:
                    print(f"⚠️ Error extracting text from page {page_num}: {e}")
                    continue
            doc.close()
            
            if text.strip():
                print(f"✅ Successfully extracted {len(text)} characters")
                return text
            else:
                print("❌ No text extracted")
                return None
                
        except Exception as e:
            print(f"❌ Error opening PDF: {e}")
            return None

    def clean_text(self, text):
        """Clean and preprocess extracted text"""
        if not text:
            return ""
            
        print("🔄 Cleaning extracted text...")
        
        # Remove page markers
        text = re.sub(r'--- Page \d+ ---', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove duplicate lines while preserving order
        lines = text.split('\n')
        seen = set()
        clean_lines = []

        for line in lines:
            line = line.strip()
            if line and line not in seen:
                # Filter out headers/footers (all caps, page indicators)
                if not (line.isupper() and len(line) < 100):
                    if not re.search(r'page\s*\d+|\d+\s*of\s*\d+', line.lower()):
                        clean_lines.append(line)
                        seen.add(line)

        cleaned_text = ' '.join(clean_lines)
        print(f"✅ Cleaned text: {len(cleaned_text)} characters")
        return cleaned_text

    def ingest(self, file_path):
        """Main ingestion method"""
        print(f"📥 Ingesting PDF: {file_path}")

        # Try direct text extraction first
        text = self.extract_text(file_path)

        # Fallback to OCR if no text found
        if not text or len(text.strip()) < 200:
            print("🔄 No text found, attempting OCR...")
            text = self.ocr_extract(file_path)

        if not text or len(text.strip()) < 100:
            raise ValueError("❌ Could not extract sufficient text from PDF")

        # Clean text
        cleaned = self.clean_text(text)
        print(f"📊 Cleaned text length: {len(cleaned)} characters")

        if len(cleaned) < 100:
            raise ValueError("❌ Insufficient text after cleaning")

        # Split into chunks
        chunks = self.splitter.split_text(cleaned)
        print(f"✅ Created {len(chunks)} text chunks")

        return chunks

    def ocr_extract(self, file_path):
        """Extract text using OCR for scanned PDFs"""
        try:
            print("🔄 Starting OCR extraction...")
            images = convert_from_path(file_path, dpi=200)  # Lower DPI for speed
            text = ""
            for i, img in enumerate(images):
                print(f"📄 Processing page {i+1}/{len(images)} with OCR")
                page_text = pytesseract.image_to_string(img)
                text += f"\n--- Page {i+1} ---\n{page_text}"
            return text
        except Exception as e:
            print(f"❌ Error in OCR extraction: {e}")
            return ""

class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size=512, chunk_overlap=64, separators=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators if separators else ["\n\n", "\n", ". ", "! ", "? ", " ", ""]

    def split_text(self, text):
        """Split text into chunks"""
        if not text:
            return []

        text = str(text)
        chunks = []
        start = 0
        
        while start < len(text):
            # Calculate end position
            end = min(start + self.chunk_size, len(text))
            
            # If we're not at the end, try to break at a separator
            if end < len(text):
                for separator in self.separators:
                    if separator:
                        # Look for the separator before the end
                        pos = text.rfind(separator, start, end)
                        if pos != -1 and pos > start:
                            end = pos + len(separator)
                            break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position, considering overlap
            start = end - self.chunk_overlap
            if start < 0:
                start = 0
            if end >= len(text):
                break

        return chunks