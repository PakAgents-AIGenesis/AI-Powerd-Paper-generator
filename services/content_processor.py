# services/content_processor.py
import re
import nltk
from typing import List, Tuple
import os

class ContentProcessor:
    def __init__(self):
        self.min_sentence_length = 15
        self.min_chunk_length = 100
        
    def extract_meaningful_content(self, text: str) -> Tuple[List[str], List[str]]:
        """Extract meaningful sentences and key concepts from text"""
        if not text or len(text.strip()) < 200:
            print("❌ Text too short for meaningful extraction")
            return [], []
        
        print(f"📄 Processing text of length: {len(text)}")
        
        # Clean the text
        text = self.clean_text(text)
        
        # Split into sentences (improved approach)
        sentences = self.smart_sentence_split(text)
        meaningful_sentences = []
        key_concepts = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) >= self.min_sentence_length and self.is_meaningful(sentence):
                meaningful_sentences.append(sentence)
                
                # Extract key concepts (nouns and important phrases)
                concepts = self.extract_concepts(sentence)
                key_concepts.extend(concepts)
        
        # Remove duplicates from key concepts
        key_concepts = list(set(key_concepts))
        
        print(f"📝 Found {len(meaningful_sentences)} meaningful sentences and {len(key_concepts)} key concepts")
        
        if not meaningful_sentences:
            print("⚠️ No meaningful sentences found, using fallback extraction")
            return self.fallback_extraction(text)
            
        return meaningful_sentences, key_concepts
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page numbers and headers
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        return text.strip()
    
    def smart_sentence_split(self, text: str) -> List[str]:
        """Split text into sentences intelligently"""
        # Simple sentence splitting that handles abbreviations
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def is_meaningful(self, sentence: str) -> bool:
        """Check if a sentence is meaningful (not a header/footer)"""
        # Exclude very short sentences
        if len(sentence) < self.min_sentence_length:
            return False
        
        # Exclude all-caps sentences (likely headers)
        if sentence.isupper() and len(sentence) < 100:
            return False
            
        # Exclude page number indicators
        if re.search(r'page\s*\d+|\d+\s*of\s*\d+', sentence.lower()):
            return False
            
        # Should contain some substantive words
        words = sentence.split()
        if len(words) < 4:  # Too short
            return False
            
        return True
    
    def extract_concepts(self, sentence: str) -> List[str]:
        """Extract key concepts from a sentence"""
        concepts = []
        
        # Extract capitalized phrases (potential proper nouns/terms)
        words = sentence.split()
        for i, word in enumerate(words):
            if (len(word) > 3 and word[0].isupper() and 
                not word.isupper() and  # Not all caps
                i > 0 and words[i-1][-1] not in '.!?'):  # Not start of sentence
                concepts.append(word)
        
        # Extract noun phrases (simple pattern)
        noun_phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', sentence)
        concepts.extend(noun_phrases)
        
        return concepts
    
    def fallback_extraction(self, text: str) -> Tuple[List[str], List[str]]:
        """Fallback method when no meaningful sentences are found"""
        print("🔄 Using fallback extraction")
        # Split by paragraphs or large chunks
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
        
        if paragraphs:
            return paragraphs, ["General Concepts"]
        else:
            # Last resort: split by fixed length
            chunk_size = 200
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            return chunks[:10], ["Extracted Concepts"]
    
    def create_chunks(self, sentences: List[str], chunk_size: int = 5) -> List[str]:
        """Create coherent chunks from sentences"""
        if not sentences:
            return []
            
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence would exceed chunk size and we have content, save current chunk
            if current_length + sentence_length > 500 and current_chunk:  # Increased chunk size
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length + 1  # +1 for space
        
        # Add the last chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        # Filter chunks that are too short
        chunks = [chunk for chunk in chunks if len(chunk) >= self.min_chunk_length]
        
        print(f"📦 Created {len(chunks)} chunks from {len(sentences)} sentences")
        return chunks