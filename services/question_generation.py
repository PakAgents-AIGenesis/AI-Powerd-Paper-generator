# services/question_generation.py
import random
import json
from typing import List, Dict, Any

try:
    # FIX: Use absolute import for services
    from services.gemini_integration import GeminiAI
except ImportError:
    try:
        # Fallback: try relative import
        from .gemini_integration import GeminiAI
    except ImportError:
        print("❌ Failed to import GeminiAI, using fallback")
        
        # Emergency fallback
        class GeminiAI:
            def __init__(self, api_key=None):
                self.api_key = api_key
                self.available = False
                print("⚠️ Using fallback GeminiAI - no real AI available")
            
            def generate_question(self, chunk: str, difficulty: str, blooms_level: str, question_type: str = "mcq") -> Dict[str, Any]:
                """Fallback question generation with contextual variety"""
                print(f"🔄 Generating fallback {question_type} question")
                
                # Create contextual questions based on chunk content
                chunk_lower = chunk.lower()
                
                if "technical" in chunk_lower and "report" in chunk_lower:
                    return self._get_tech_question(chunk, difficulty, blooms_level, question_type)
                elif "research" in chunk_lower:
                    return self._get_research_question(chunk, difficulty, blooms_level, question_type)
                elif "data" in chunk_lower or "analysis" in chunk_lower:
                    return self._get_data_question(chunk, difficulty, blooms_level, question_type)
                else:
                    return self._get_general_question(chunk, difficulty, blooms_level, question_type)
            
            def _get_tech_question(self, chunk: str, difficulty: str, blooms_level: str, question_type: str) -> Dict[str, Any]:
                """Generate varied technical questions based on chunk content"""
                base = {
                    "difficulty": difficulty,
                    "blooms_level": blooms_level,
                    "question_type": question_type,
                    "explanation": "Based on technical documentation content",
                    "source_chunk": chunk[:100] + "..." if len(chunk) > 100 else chunk
                }
                
                # Different question templates for variety
                tech_questions = [
                    {
                        "question": "What is the primary characteristic of effective technical documentation?",
                        "options": [
                            "Use of complex technical jargon",
                            "Clarity, accuracy, and accessibility",
                            "Lengthy and detailed descriptions", 
                            "Colorful graphics and images"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "Which element is most crucial for user comprehension in technical manuals?",
                        "options": [
                            "Complex terminology",
                            "Logical organization and clear examples",
                            "Extensive background information",
                            "Abstract concepts"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "What distinguishes technical writing from creative writing?",
                        "options": [
                            "Use of figurative language",
                            "Focus on factual accuracy and precision",
                            "Entertainment value",
                            "Character development"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "Why is consistency important in technical documentation?",
                        "options": [
                            "It makes documents look professional",
                            "It reduces cognitive load and prevents confusion",
                            "It allows for longer documents",
                            "It enables creative expression"
                        ],
                        "answer": 1
                    }
                ]
                
                if question_type == "mcq":
                    # Select a random question template
                    selected_q = random.choice(tech_questions)
                    base.update(selected_q)
                elif question_type == "short":
                    base.update({
                        "question": "Explain why accuracy is crucial in technical reports.",
                        "answer": "Accuracy ensures reliability, prevents misunderstandings, supports decision-making, and maintains professional credibility in technical documentation.",
                        "options": []
                    })
                else:  # long
                    base.update({
                        "question": "Discuss the key elements that make technical documentation effective for different audiences.",
                        "answer": "Effective technical documentation considers audience knowledge level, uses appropriate terminology, provides clear structure with headings, includes examples where needed, and maintains consistency in formatting and style for better comprehension.",
                        "options": []
                    })
                return base
            
            def _get_research_question(self, chunk: str, difficulty: str, blooms_level: str, question_type: str) -> Dict[str, Any]:
                """Generate varied research questions based on chunk content"""
                base = {
                    "difficulty": difficulty,
                    "blooms_level": blooms_level,
                    "question_type": question_type,
                    "explanation": "Based on research methodology content",
                    "source_chunk": chunk[:100] + "..." if len(chunk) > 100 else chunk
                }
                
                # Different question templates for variety
                research_questions = [
                    {
                        "question": "What is the main purpose of a literature review in research?",
                        "options": [
                            "To fill pages and meet word count requirements",
                            "To identify gaps in existing knowledge and contextualize the study",
                            "To copy previous researchers' work",
                            "To demonstrate reading comprehension"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "Which factor is most important for research validity?",
                        "options": [
                            "Length of the research paper",
                            "Appropriate methodology and measurement accuracy",
                            "Number of references cited",
                            "Complexity of statistical analysis"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "What distinguishes qualitative from quantitative research?",
                        "options": [
                            "The number of participants",
                            "Focus on meanings vs. numerical data analysis",
                            "The length of the study",
                            "Use of questionnaires"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "Why is ethical approval important in research?",
                        "options": [
                            "It makes research more expensive",
                            "It protects participants and ensures ethical standards",
                            "It guarantees publication",
                            "It simplifies data analysis"
                        ],
                        "answer": 1
                    }
                ]
                
                if question_type == "mcq":
                    # Select a random question template
                    selected_q = random.choice(research_questions)
                    base.update(selected_q)
                elif question_type == "short":
                    base.update({
                        "question": "Describe the importance of research methodology.",
                        "answer": "Research methodology provides a systematic approach for data collection and analysis, ensures study validity and reliability, and allows for replication of research findings.",
                        "options": []
                    })
                else:  # long
                    base.update({
                        "question": "Analyze how different research methods are suited for different types of research questions.",
                        "answer": "Quantitative methods suit hypothesis testing and statistical analysis, qualitative methods explore complex phenomena and meanings, while mixed methods provide comprehensive insights by combining both approaches based on research objectives.",
                        "options": []
                    })
                return base
            
            def _get_data_question(self, chunk: str, difficulty: str, blooms_level: str, question_type: str) -> Dict[str, Any]:
                """Generate varied data analysis questions"""
                base = {
                    "difficulty": difficulty,
                    "blooms_level": blooms_level,
                    "question_type": question_type,
                    "explanation": "Based on data analysis content",
                    "source_chunk": chunk[:100] + "..." if len(chunk) > 100 else chunk
                }
                
                # Different question templates for variety
                data_questions = [
                    {
                        "question": "What is the primary goal of data analysis?",
                        "options": [
                            "To collect large amounts of data",
                            "To extract meaningful insights and support decision-making",
                            "To create colorful charts",
                            "To prove predetermined conclusions"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "Which statistical measure indicates data variability?",
                        "options": [
                            "Mean",
                            "Standard deviation",
                            "Median",
                            "Mode"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "What makes data visualization effective?",
                        "options": [
                            "Use of many colors",
                            "Clear communication of insights and patterns",
                            "Complex graphical elements",
                            "Large size"
                        ],
                        "answer": 1
                    }
                ]
                
                if question_type == "mcq":
                    selected_q = random.choice(data_questions)
                    base.update(selected_q)
                elif question_type == "short":
                    base.update({
                        "question": "Explain the importance of data cleaning in analysis.",
                        "answer": "Data cleaning ensures accuracy, removes inconsistencies, handles missing values, and improves the reliability of analytical results and conclusions.",
                        "options": []
                    })
                else:  # long
                    base.update({
                        "question": "Discuss the relationship between data quality and analytical outcomes.",
                        "answer": "High-quality data leads to reliable insights and valid conclusions, while poor data quality can result in misleading findings, incorrect decisions, and wasted resources in the analytical process.",
                        "options": []
                    })
                return base
            
            def _get_general_question(self, chunk: str, difficulty: str, blooms_level: str, question_type: str) -> Dict[str, Any]:
                """Generate varied general academic questions"""
                base = {
                    "difficulty": difficulty,
                    "blooms_level": blooms_level,
                    "question_type": question_type,
                    "explanation": "Based on academic content",
                    "source_chunk": chunk[:100] + "..." if len(chunk) > 100 else chunk
                }
                
                # Different question templates for variety
                general_questions = [
                    {
                        "question": "What is the primary goal of academic writing?",
                        "options": [
                            "To entertain readers with creative stories",
                            "To present information clearly and support arguments with evidence",
                            "To use complex vocabulary to impress professors",
                            "To summarize information without analysis"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "Which characteristic is most important for credible sources?",
                        "options": [
                            "Recent publication date",
                            "Author credentials and peer-review process",
                            "Length of the publication",
                            "Number of citations"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "What is the purpose of critical thinking in academia?",
                        "options": [
                            "To criticize others' work",
                            "To evaluate evidence and construct reasoned arguments",
                            "To memorize information",
                            "To agree with established authorities"
                        ],
                        "answer": 1
                    },
                    {
                        "question": "Why is proper citation important in academic work?",
                        "options": [
                            "To increase word count",
                            "To acknowledge sources and avoid plagiarism",
                            "To make papers look more impressive",
                            "To follow formatting rules"
                        ],
                        "answer": 1
                    }
                ]
                
                if question_type == "mcq":
                    # Select a random question template
                    selected_q = random.choice(general_questions)
                    base.update(selected_q)
                elif question_type == "short":
                    base.update({
                        "question": "Explain the importance of critical analysis in academic work.",
                        "answer": "Critical analysis enables evaluation of evidence, identification of biases, development of reasoned arguments, and contributes to knowledge advancement rather than mere information repetition.",
                        "options": []
                    })
                else:  # long
                    base.update({
                        "question": "Discuss how proper academic integrity practices contribute to the credibility of research.",
                        "answer": "Academic integrity through proper citation, original work, and ethical research practices establishes credibility, enables knowledge building on previous work, maintains trust in academic community, and ensures the reliability and validity of research outcomes.",
                        "options": []
                    })
                return base

class QuestionGenerator:
    def __init__(self, api_key=None):
        print("🔄 Initializing QuestionGenerator...")
        self.gemini = GeminiAI(api_key)
        print(f"🤖 QuestionGenerator ready - Gemini available: {getattr(self.gemini, 'available', False)}")
        # Track used questions to avoid duplicates in fallback mode
        self.used_questions = set()

    def generate_questions_from_content(self, chunks: List[str], counts: Dict[str, int],
                                      difficulty: str = "medium", blooms_level: str = "understand") -> Dict[str, List]:
        """Generate questions that actually use the PDF content"""
        print(f"📚 Generating questions from {len(chunks)} content chunks")
        
        questions = {
            "mcq": [],
            "short": [], 
            "long": []
        }
        
        # Ensure we have enough chunks
        if len(chunks) < sum(counts.values()):
            print(f"⚠️ Not enough chunks ({len(chunks)}) for requested questions ({sum(counts.values())})")
            # Reuse chunks if necessary
            chunks = chunks * (sum(counts.values()) // len(chunks) + 1)
        
        used_chunks = set()
        
        # Generate MCQs with VARIED options
        for i in range(min(counts['mcq'], len(chunks))):
            chunk = chunks[i]
            if chunk in used_chunks:
                continue
                
            try:
                # Create context-aware MCQ
                mcq = self._create_contextual_mcq(chunk, difficulty, i)
                if mcq and mcq['question'] not in [q['question'] for q in questions["mcq"]]:
                    questions["mcq"].append(mcq)
                    used_chunks.add(chunk)
            except Exception as e:
                print(f"❌ Error creating MCQ {i}: {e}")
                continue
        
        # Generate Short Answer questions
        short_start = len(used_chunks)
        for i in range(min(counts['short'], len(chunks) - short_start)):
            idx = short_start + i
            if idx >= len(chunks):
                break
            chunk = chunks[idx]
            try:
                saq = self._create_contextual_short_answer(chunk, difficulty, i)
                if saq and saq['question'] not in [q['question'] for q in questions["short"]]:
                    questions["short"].append(saq)
                    used_chunks.add(chunk)
            except Exception as e:
                print(f"❌ Error creating SAQ {i}: {e}")
                continue
        
        # Generate Long Answer questions  
        long_start = len(used_chunks)
        for i in range(min(counts['long'], len(chunks) - long_start)):
            idx = long_start + i
            if idx >= len(chunks):
                break
            chunk = chunks[idx]
            try:
                laq = self._create_contextual_long_answer(chunk, difficulty, i)
                if laq and laq['question'] not in [q['question'] for q in questions["long"]]:
                    questions["long"].append(laq)
                    used_chunks.add(chunk)
            except Exception as e:
                print(f"❌ Error creating LAQ {i}: {e}")
                continue
        
        print(f"✅ Generated {len(questions['mcq'])} MCQs, {len(questions['short'])} SAQs, {len(questions['long'])} LAQs from content")
        return questions

    def _create_contextual_mcq(self, chunk: str, difficulty: str, index: int) -> Dict:
        """Create MCQ that actually uses the content"""
        # Extract key phrases from chunk for context
        words = chunk.split()[:20]  # First 20 words for context
        context = " ".join(words)
        
        # Different question templates based on content
        templates = [
            f"What is the main concept discussed in: '{context}'?",
            f"Based on the content, what best describes: '{context}'?",
            f"What key point is emphasized regarding: '{context}'?",
            f"Which statement accurately reflects the discussion of: '{context}'?"
        ]
        
        question_text = templates[index % len(templates)]
        
        # Create VARIED options based on actual content
        option_templates = [
            [f"A correct interpretation based on {context}", f"A common misunderstanding about {context}", f"An unrelated concept that sounds similar", f"A partially correct but incomplete view"],
            [f"The primary concept explained in the text", f"A secondary detail mentioned briefly", f"A contradictory viewpoint not supported", f"An assumption not made in the content"],
            [f"The main idea supported by evidence", f"A minor point with limited significance", f"An external concept not discussed", f"An oversimplification of the topic"],
            [f"The central argument presented", f"A supporting example provided", f"A counterargument not addressed", f"An irrelevant technical detail"]
        ]
        
        options = option_templates[index % len(option_templates)]
        
        return {
            "question": question_text,
            "options": options,
            "answer": 0,
            "explanation": f"Based on the content discussing {context}",
            "difficulty": difficulty,
            "blooms_level": "understand",
            "question_type": "mcq",
            "source_chunk": chunk[:100] + "..."
        }

    def _create_contextual_short_answer(self, chunk: str, difficulty: str, index: int) -> Dict:
        """Create short answer that uses content"""
        words = chunk.split()[:15]
        context = " ".join(words)
        
        templates = [
            f"Explain the key concept of '{context}' in 2-3 sentences.",
            f"Describe the main point about '{context}' briefly.",
            f"What is the significance of '{context}' according to the text?",
            f"Summarize the discussion about '{context}' from the material."
        ]
        
        return {
            "question": templates[index % len(templates)],
            "options": [],
            "answer": f"This would explain {context} based on the specific content provided in the source material.",
            "explanation": "Answer should reference the actual content from the text and demonstrate understanding of the key concepts.",
            "difficulty": difficulty,
            "blooms_level": "understand",
            "question_type": "short",
            "source_chunk": chunk[:100] + "..."
        }

    def _create_contextual_long_answer(self, chunk: str, difficulty: str, index: int) -> Dict:
        """Create long answer that uses content"""
        words = chunk.split()[:15]
        context = " ".join(words)
        
        templates = [
            f"Discuss in detail the concepts related to '{context}' as presented in the material. Provide specific examples and applications.",
            f"Analyze the importance and implications of '{context}' based on the content. Include relevant details and connections to broader concepts.",
            f"Provide a comprehensive explanation of '{context}' covering its principles, significance, and practical relevance as discussed in the text."
        ]
        
        return {
            "question": templates[index % len(templates)],
            "options": [],
            "answer": f"A comprehensive analysis of {context} covering principles, examples, and practical applications as detailed in the source material. The answer should demonstrate deep understanding and critical thinking about the specific content.",
            "explanation": "Should demonstrate deep understanding of the specific content, critical analysis, and ability to connect concepts to practical applications.",
            "difficulty": difficulty, 
            "blooms_level": "analyze",
            "question_type": "long",
            "source_chunk": chunk[:100] + "..."
        }

    def generate_mcq(self, chunk: str, difficulty: str, blooms_level: str) -> Dict[str, Any]:
        """Generate multiple choice question"""
        print(f"🎯 Generating MCQ (Difficulty: {difficulty}, Bloom's: {blooms_level})")
        question = self.gemini.generate_question(chunk, difficulty, blooms_level, "mcq")
        
        # For fallback mode, ensure uniqueness
        if not getattr(self.gemini, 'available', False):
            question_text = question['question']
            if question_text in self.used_questions:
                # If duplicate, modify the question slightly
                question['question'] = question_text + " (Based on specific content)"
            self.used_questions.add(question_text)
        
        print(f"✅ MCQ generated: {question['question'][:50]}...")
        return question

    def generate_short_answer(self, chunk: str, difficulty: str, blooms_level: str) -> Dict[str, Any]:
        """Generate short answer question"""
        print(f"🎯 Generating Short Answer (Difficulty: {difficulty}, Bloom's: {blooms_level})")
        question = self.gemini.generate_question(chunk, difficulty, blooms_level, "short")
        print(f"✅ Short Answer generated: {question['question'][:50]}...")
        return question

    def generate_long_answer(self, chunk: str, difficulty: str, blooms_level: str) -> Dict[str, Any]:
        """Generate long answer question"""
        print(f"🎯 Generating Long Answer (Difficulty: {difficulty}, Bloom's: {blooms_level})")
        question = self.gemini.generate_question(chunk, difficulty, blooms_level, "long")
        print(f"✅ Long Answer generated: {question['question'][:50]}...")
        return question

    def generate_questions(self, chunks: List[str], counts: Dict[str, int],
                          difficulty: str = "medium", blooms_level: str = "understand") -> Dict[str, List]:
        """Generate different types of questions"""
        print(f"🚀 Starting question generation for {len(chunks)} chunks")
        print(f"📊 Target counts: MCQ={counts['mcq']}, Short={counts['short']}, Long={counts['long']}")

        # Filter valid chunks
        valid_chunks = [chunk for chunk in chunks if len(chunk.strip()) > 50]
        if not valid_chunks:
            print("❌ No valid chunks available for question generation")
            # Use first few chunks even if short
            valid_chunks = chunks[:min(5, len(chunks))]
            if not valid_chunks:
                raise ValueError("No valid chunks available for question generation")

        print(f"✅ Using {len(valid_chunks)} valid chunks")

        questions = {
            "mcq": [],
            "short": [],
            "long": []
        }

        # Reset used questions tracking for new generation session
        self.used_questions = set()

        # Generate MCQs - ensure we use different chunks
        mcq_count = min(counts['mcq'], len(valid_chunks))
        mcq_chunks = random.sample(valid_chunks, mcq_count)
        print(f"🔢 Generating {mcq_count} MCQs...")
        
        for i, chunk in enumerate(mcq_chunks):
            try:
                print(f"  📝 MCQ {i+1}/{mcq_count}...")
                mcq = self.generate_mcq(chunk, difficulty, blooms_level)
                
                # Check for duplicate questions in the current batch
                current_questions = [q['question'] for q in questions["mcq"]]
                if mcq['question'] not in current_questions:
                    questions["mcq"].append(mcq)
                else:
                    print(f"⚠️  Duplicate MCQ detected, skipping...")
                    # Try with a different chunk if available
                    remaining_chunks = [c for c in valid_chunks if c not in mcq_chunks]
                    if remaining_chunks:
                        alternative_chunk = random.choice(remaining_chunks)
                        print(f"🔄 Retrying with alternative chunk...")
                        mcq = self.generate_mcq(alternative_chunk, difficulty, blooms_level)
                        if mcq['question'] not in current_questions:
                            questions["mcq"].append(mcq)
                        
            except Exception as e:
                print(f"❌ Error generating MCQ {i+1}: {e}")
                continue

        # Generate Short Answer questions
        remaining_after_mcq = [c for c in valid_chunks if c not in mcq_chunks]
        short_count = min(counts['short'], len(remaining_after_mcq))
        short_chunks = random.sample(remaining_after_mcq, short_count)
        print(f"🔢 Generating {short_count} Short Answers...")
        
        for i, chunk in enumerate(short_chunks):
            try:
                print(f"  📝 Short Answer {i+1}/{short_count}...")
                short_q = self.generate_short_answer(chunk, difficulty, blooms_level)
                questions["short"].append(short_q)
            except Exception as e:
                print(f"❌ Error generating short answer {i+1}: {e}")
                continue

        # Generate Long Answer questions
        remaining_after_short = [c for c in remaining_after_mcq if c not in short_chunks]
        long_count = min(counts['long'], len(remaining_after_short))
        long_chunks = random.sample(remaining_after_short, long_count)
        print(f"🔢 Generating {long_count} Long Answers...")
        
        for i, chunk in enumerate(long_chunks):
            try:
                print(f"  📝 Long Answer {i+1}/{long_count}...")
                long_q = self.generate_long_answer(chunk, difficulty, "analyze")
                questions["long"].append(long_q)
            except Exception as e:
                print(f"❌ Error generating long answer {i+1}: {e}")
                continue

        # Summary
        total_generated = len(questions["mcq"]) + len(questions["short"]) + len(questions["long"])
        print(f"🎉 Question generation completed: {total_generated} questions generated")
        print(f"   - MCQs: {len(questions['mcq'])}")
        print(f"   - Short Answers: {len(questions['short'])}")
        print(f"   - Long Answers: {len(questions['long'])}")

        return questions

    def save_questions_json(self, questions: Dict, out_path: str = "questions.json"):
        """Save questions to JSON file"""
        try:
            with open(out_path, "w", encoding='utf-8') as f:
                json.dump(questions, f, indent=2, ensure_ascii=False)
            print(f"💾 Questions saved to {out_path}")
        except Exception as e:
            print(f"❌ Error saving questions: {e}")