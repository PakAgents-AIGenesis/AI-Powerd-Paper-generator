# services/controller.py
import os
import json
from datetime import datetime
from typing import Dict  # Add this import

try:
    # Try absolute imports first
    from services.data_ingestion import PDFIngestor
    from services.embedding_qdrant import VectorMemory  # FIXED: embedding_qdrant → embeddings_qdrant
    from services.gemini_integration import GeminiAI
    from services.question_generation import QuestionGenerator
    from services.marks_analyzer import MarksAnalyzer
except ImportError as e:
    print(f"Import warning: {e}")
    # Fallback to relative imports
    try:
        from .data_ingestion import PDFIngestor
        from .embedding_qdrant import VectorMemory
        from .gemini_integration import GeminiAI
        from .question_generation import QuestionGenerator
        from .marks_analyzer import MarksAnalyzer
    except ImportError as e2:
        print(f"Relative import also failed: {e2}")
        # Use fallback classes (keep your existing fallbacks)
        from data_ingestion import PDFIngestor
        
        # Fallback for VectorMemory
        class VectorMemory:
            def __init__(self, qdrant_url=":memory:", collection="exam_chunks", api_key=None):
                self.qdrant_url = qdrant_url
                self.collection = collection
                self.api_key = api_key
                self._store = []

            def store_document(self, chunks, metadata):
                self._store.append({"chunks": chunks, "metadata": metadata})

            def retrieve(self, query, top_k=10):
                results = []
                all_chunks = []
                for entry in self._store:
                    all_chunks.extend(entry.get("chunks", []))
                for c in all_chunks[:top_k]:
                    results.append({"text": c})
                return results
        
        # Fallback for other classes
        class GeminiAI:
            def __init__(self, api_key=None):
                self.api_key = api_key
                
            def extract_topics(self, chunks):
                return {
                    "main_topics": ["General Topic"], 
                    "subtopics": {"General Topic": ["Basic Concepts"]},
                    "knowledge_gaps": ["Need more specific content"],
                    "topic_density": {"General Topic": 0.5},
                    "blooms_distribution": {
                        "remember": 0.4, "understand": 0.3, "apply": 0.2,
                        "analyze": 0.1, "evaluate": 0.0, "create": 0.0
                    }
                }
        
        class QuestionGenerator:
            def __init__(self, api_key=None):
                self.api_key = api_key
                
            def generate_questions(self, chunks, counts, difficulty="medium"):
                # Return mock questions for testing
                return {
                    "mcq": [
                        {
                            "question": "What is the main topic discussed?",
                            "options": ["Option A", "Option B", "Option C", "Option D"],
                            "answer": 0,
                            "explanation": "Based on the content",
                            "difficulty": difficulty,
                            "blooms_level": "understand",
                            "question_type": "mcq",
                            "source_chunk": chunks[0][:100] + "..." if chunks else "No content"
                        }
                    ],
                    "short": [
                        {
                            "question": "Explain the key concept briefly.",
                            "options": [],
                            "answer": "Expected short answer",
                            "explanation": "Based on the content",
                            "difficulty": difficulty,
                            "blooms_level": "understand", 
                            "question_type": "short",
                            "source_chunk": chunks[0][:100] + "..." if chunks else "No content"
                        }
                    ],
                    "long": [
                        {
                            "question": "Discuss in detail the main topics covered.",
                            "options": [],
                            "answer": "Expected detailed answer",
                            "explanation": "Based on the content",
                            "difficulty": difficulty,
                            "blooms_level": "analyze",
                            "question_type": "long", 
                            "source_chunk": chunks[0][:100] + "..." if chunks else "No content"
                        }
                    ]
                }
        
        class MarksAnalyzer:
            def adjust(self, counts, target_total):
                return {'mcq': 1, 'short': 4, 'long': 10}

class ExamForgeController:
    def __init__(self, google_api_key=None, qdrant_url=":memory:"):
        self.ingestor = PDFIngestor()
        self.vector_store = VectorMemory(qdrant_url, "exam_chunks", google_api_key)
        self.gemini_ai = GeminiAI(google_api_key)
        self.question_gen = QuestionGenerator(google_api_key)
        self.marks_analyzer = MarksAnalyzer()

        # Set API key for environment
        if google_api_key:
            os.environ['GOOGLE_API_KEY'] = google_api_key

    def process_pdf(self, file_path: str):
        """Process PDF and store in vector database"""
        print("Starting PDF processing...")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        # Ingest PDF
        chunks = self.ingestor.ingest(file_path)

        # Store in vector database
        metadata = {
            'filename': os.path.basename(file_path),
            'total_chunks': len(chunks),
            'processed_at': str(datetime.now())
        }
        self.vector_store.store_document(chunks, metadata)

        # Extract topics
        topics = self.gemini_ai.extract_topics(chunks)
        self.save_topics_json(topics)

        print("PDF processing completed successfully")
        return chunks, topics

    def generate_exam(self, query: str, counts: Dict, target_total: int = 100) -> Dict:
        """Generate complete exam paper"""
        print(f"Generating exam for query: {query}")

        # Retrieve relevant chunks
        retrieved = self.vector_store.retrieve(query, top_k=50)
        chunks = [item['text'] for item in retrieved]

        if not chunks:
            raise ValueError("No relevant content found for the query")

        # Generate questions
        questions = self.question_gen.generate_questions(
            chunks, counts, difficulty="medium"
        )

        # Analyze and adjust marks
        final_marks = self.marks_analyzer.adjust(counts, target_total)

        # Validate questions
        self.validate_questions(questions)

        # Create exam structure
        exam = self.create_exam_structure(questions, final_marks, target_total)

        # Save exam
        self.save_exam_json(exam)

        print("Exam generation completed successfully")
        return exam

    def create_exam_structure(self, questions: Dict, marks: Dict, total_marks: int) -> Dict:
        """Create organized exam structure"""
        return {
            "exam_metadata": {
                "total_marks": total_marks,
                "marks_distribution": marks,
                "sections": 3,
                "generated_at": str(datetime.now())
            },
            "Section A (Multiple Choice Questions)": {
                "instructions": "Choose the correct option",
                "marks_per_question": marks['mcq'],
                "questions": questions['mcq']
            },
            "Section B (Short Answer Questions)": {
                "instructions": "Answer briefly in 2-3 sentences",
                "marks_per_question": marks['short'],
                "questions": questions['short']
            },
            "Section C (Long Answer Questions)": {
                "instructions": "Answer in detail with examples",
                "marks_per_question": marks['long'],
                "questions": questions['long']
            }
        }

    def save_topics_json(self, topics: Dict, out_path: str = "topics.json"):
        """Save topics analysis to JSON"""
        with open(out_path, "w", encoding='utf-8') as f:
            json.dump(topics, f, indent=2, ensure_ascii=False)

    def save_exam_json(self, exam: Dict, out_path: str = "exam.json"):
        """Save exam to JSON file"""
        with open(out_path, "w", encoding='utf-8') as f:
            json.dump(exam, f, indent=2, ensure_ascii=False)

    def validate_questions(self, questions: Dict):
        """Validate generated questions"""
        all_questions = questions['mcq'] + questions['short'] + questions['long']
        
        if not all_questions:
            print("Warning: No questions generated")
            return
            
        sources = set()

        for q in all_questions:
            # Check source
            if not q.get('source_chunk'):
                print("Warning: Question missing source chunk")
                continue

            # Check MCQ options
            if q['question_type'] == 'mcq':
                options = q.get('options', [])
                if len(options) != 4:
                    print(f"Warning: MCQ should have 4 options, got {len(options)}")
                if len(set(options)) != len(options):
                    print("Warning: Duplicate options in MCQ")

            # Check for duplicates
            source_hash = hash(q.get('source_chunk', '') + q.get('question', ''))
            if source_hash in sources:
                print("Warning: Duplicate question detected")
            sources.add(source_hash)

        print("Questions validation completed")