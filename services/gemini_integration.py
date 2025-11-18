# services/gemini_integration.py
import google.generativeai as genai
import os
import json
import time
from typing import List, Dict, Any

class GeminiAI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        print(f"🔑 Gemini API Key: {'***' + self.api_key[-4:] if self.api_key else 'NOT SET'}")
        
        if not self.api_key:
            print("❌ No Google API key found")
            self.available = False
            return

        try:
            genai.configure(api_key=self.api_key)
            
            # Find a working model
            working_model = self._find_working_model()
            if working_model:
                self.model = genai.GenerativeModel(working_model)
                self.available = True
                print(f"✅ Gemini AI configured successfully with model: {working_model}")
            else:
                print("❌ No working Gemini model found")
                self.available = False
                
        except Exception as e:
            print(f"❌ Error configuring Gemini: {e}")
            self.available = False

    def _find_working_model(self):
        """Find a working Gemini model with the current API key"""
        model_attempts = [
            'gemini-pro',           # Most widely available
            'models/gemini-pro',    # Alternative format
            'gemini-1.0-pro',       # Version-specific
            'models/gemini-1.0-pro',
            'gemini-1.5-flash',     # Newer models
            'models/gemini-1.5-flash',
            'gemini-1.5-pro',
            'models/gemini-1.5-pro'
        ]
        
        for model_name in model_attempts:
            try:
                print(f"🔄 Testing model: {model_name}")
                test_model = genai.GenerativeModel(model_name)
                # Quick test with minimal content
                test_response = test_model.generate_content(
                    "Say 'OK'",
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=10,
                        temperature=0.1
                    )
                )
                if test_response.text:
                    print(f"✅ Model {model_name} is working")
                    return model_name
            except Exception as e:
                print(f"❌ Model {model_name} failed: {str(e)[:80]}")
                continue
        
        return None

    def generate_content(self, prompt, temperature=0.7, max_tokens=1000):
        """Generate content using Gemini with retry logic"""
        if not self.available:
            print("❌ Gemini not available")
            return None
        
        # Retry logic for API calls
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 Gemini API call attempt {attempt + 1}/{max_retries}")
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    )
                )
                print("✅ Gemini response received")
                return response.text
                
            except Exception as e:
                print(f"❌ Gemini API error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print("❌ All Gemini API retries failed")
                    return None
        
        return None

    def extract_topics(self, chunks: List[str]) -> Dict[str, Any]:
        """Extract topics and subtopics from text chunks"""
        if not self.available:
            print("❌ Gemini not available for topic extraction")
            return self._get_fallback_topics()

        # Use more chunks for better topic extraction
        combined_text = " ".join(chunks[:5])[:3000]  # Use first 5 chunks, limit to 3000 chars
        print(f"🔄 Extracting topics from {len(combined_text)} characters...")

        prompt = f"""
        Analyze the following educational content and extract main topics and structure.

        CONTENT:
        {combined_text}

        Return ONLY valid JSON in this format:
        {{
            "main_topics": ["topic1", "topic2", "topic3"],
            "subtopics": {{
                "topic1": ["subtopic1.1", "subtopic1.2"],
                "topic2": ["subtopic2.1", "subtopic2.2"]
            }},
            "knowledge_gaps": ["gap1", "gap2"],
            "topic_density": {{
                "topic1": 0.8,
                "topic2": 0.6
            }},
            "blooms_distribution": {{
                "remember": 0.3,
                "understand": 0.4,
                "apply": 0.2,
                "analyze": 0.1,
                "evaluate": 0.0,
                "create": 0.0
            }}
        }}

        Base your analysis ONLY on the provided content. Be specific to the actual content.
        """

        response = self.generate_content(prompt, temperature=0.3)
        if response:
            try:
                # Extract JSON from response
                json_str = self._extract_json_from_response(response)
                result = json.loads(json_str)
                print("✅ Topics extracted successfully")
                return result
            except Exception as e:
                print(f"❌ Failed to parse topics JSON: {e}")
                print(f"Raw response: {response[:500]}...")

        print("🔄 Using fallback topics")
        return self._get_fallback_topics()

    def generate_question(self, chunk: str, difficulty: str, blooms_level: str, question_type: str = "mcq") -> Dict[str, Any]:
        """Generate question using Gemini AI"""
        print(f"🔄 Generating {question_type} question from {len(chunk)} chars...")
        
        if not self.available:
            print(f"❌ Gemini not available, using fallback for {question_type}")
            return self._get_contextual_fallback_question(chunk, difficulty, blooms_level, question_type)

        prompt = self._build_question_prompt(chunk, difficulty, blooms_level, question_type)
        response = self.generate_content(prompt, temperature=0.3)
        
        if response:
            try:
                json_str = self._extract_json_from_response(response)
                question_data = json.loads(json_str)
                
                # Validate the question data
                if self._validate_question(question_data, question_type):
                    print(f"✅ {question_type} question generated successfully")
                    return question_data
                    
            except Exception as e:
                print(f"❌ Failed to parse question JSON: {e}")
                print(f"Raw response: {response[:200]}...")

        print(f"🔄 Using fallback for {question_type} question")
        return self._get_contextual_fallback_question(chunk, difficulty, blooms_level, question_type)

    def _extract_json_from_response(self, response: str) -> str:
        """Extract JSON from API response"""
        # Remove markdown code blocks if present
        if '```json' in response:
            response = response.split('```json')[1].split('```')[0]
        elif '```' in response:
            response = response.split('```')[1].split('```')[0]
        
        # Find JSON object
        start = response.find('{')
        end = response.rfind('}') + 1
        
        if start != -1 and end != 0:
            return response[start:end]
        
        return response.strip()

    def _build_question_prompt(self, chunk: str, difficulty: str, blooms_level: str, question_type: str) -> str:
        """Build specific prompt for each question type"""
        # Extract context from chunk for better prompts
        context_words = chunk.split()[:15]
        context = " ".join(context_words)
        
        base_prompt = f"""
        Create ONE {question_type.upper()} question based EXCLUSIVELY on the following text.

        TEXT CONTENT:
        {chunk[:1500]}

        CONTEXT: {context}

        REQUIREMENTS:
        - Difficulty: {difficulty}
        - Bloom's Taxonomy Level: {blooms_level}
        - Use ONLY information from the provided text
        - Make the question specific and relevant to the content
        - Ensure the question can be answered using ONLY the provided text
        """

        if question_type == "mcq":
            base_prompt += """
            - Provide EXACTLY 4 distinct options
            - One option must be clearly correct based on the text
            - Options should be plausible but distinct
            - Avoid "all of the above" or "none of the above"
            """
        elif question_type == "short":
            base_prompt += """
            - Provide a clear, concise expected answer
            - Answer should be 2-3 sentences maximum
            - Focus on key concepts from the text
            """
        elif question_type == "long":
            base_prompt += """
            - Provide detailed evaluation criteria
            - Answer should demonstrate deep understanding
            - Include specific references to the text content
            """

        json_format = '''
        {
            "question": "generated question here",
            "options": ["option1", "option2", "option3", "option4"],
            "answer": 0,
            "explanation": "brief explanation referencing the specific text content",
            "difficulty": "''' + difficulty + '''",
            "blooms_level": "''' + blooms_level + '''",
            "question_type": "''' + question_type + '''",
            "source_chunk": "''' + chunk[:100] + '''..."
        }
        '''

        base_prompt += f"""
        Return ONLY valid JSON in this exact format:
        {json_format}

        IMPORTANT: Base everything ONLY on the provided text content. Do not use external knowledge.
        """

        return base_prompt

    def _validate_question(self, question_data: Dict, question_type: str) -> bool:
        """Validate generated question data"""
        required_fields = ["question", "answer", "explanation", "difficulty", "blooms_level", "question_type"]
        
        for field in required_fields:
            if field not in question_data:
                print(f"❌ Missing required field: {field}")
                return False
        
        if question_type == "mcq":
            if "options" not in question_data or len(question_data["options"]) != 4:
                print("❌ MCQ must have exactly 4 options")
                return False
                
            # Check for duplicate options
            if len(set(question_data["options"])) != len(question_data["options"]):
                print("❌ MCQ has duplicate options")
                return False
        
        return True

    def _get_contextual_fallback_question(self, chunk: str, difficulty: str, blooms_level: str, question_type: str) -> Dict[str, Any]:
        """Create contextual fallback questions based on content"""
        # Extract context from the chunk for more relevant questions
        chunk_words = chunk.split()[:20]
        context = " ".join(chunk_words)
        chunk_lower = chunk.lower()
        
        # Determine content type for better contextual questions
        if any(word in chunk_lower for word in ['technical', 'report', 'documentation', 'manual']):
            return self._get_tech_report_question(context, difficulty, blooms_level, question_type)
        elif any(word in chunk_lower for word in ['research', 'method', 'study', 'experiment']):
            return self._get_research_question(context, difficulty, blooms_level, question_type)
        elif any(word in chunk_lower for word in ['data', 'analysis', 'statistic', 'result']):
            return self._get_data_question(context, difficulty, blooms_level, question_type)
        elif any(word in chunk_lower for word in ['computer', 'software', 'system', 'algorithm']):
            return self._get_computer_science_question(context, difficulty, blooms_level, question_type)
        else:
            return self._get_general_question(context, difficulty, blooms_level, question_type)

    def _get_tech_report_question(self, context: str, difficulty: str, blooms_level: str, question_type: str) -> Dict[str, Any]:
        """Technical report related questions"""
        base = {
            "difficulty": difficulty,
            "blooms_level": blooms_level,
            "question_type": question_type,
            "explanation": f"Based on technical content about {context}",
            "source_chunk": f"Technical content: {context}..."
        }
        
        if question_type == "mcq":
            base.update({
                "question": f"What is the primary purpose of technical documentation regarding {context}?",
                "options": [
                    f"To entertain readers interested in {context}",
                    f"To convey technical information about {context} objectively and factually",
                    f"To promote commercial products related to {context}",
                    f"To tell fictional stories about {context}"
                ],
                "answer": 1
            })
        elif question_type == "short":
            base.update({
                "question": f"Explain the key characteristics of effective technical documentation for {context}.",
                "answer": f"Effective technical documentation for {context} should be clear, concise, objective, well-structured, and evidence-based with proper documentation of methods and findings specific to this domain.",
                "options": []
            })
        else:  # long
            base.update({
                "question": f"Discuss the importance of proper structure and documentation in technical reports about {context} for professional communication.",
                "answer": f"Proper structure ensures logical flow and readability for {context} topics, while comprehensive documentation provides credibility, enables reproducibility, facilitates peer review, and serves as a permanent record for future reference and knowledge transfer in this technical domain.",
                "options": []
            })
        
        return base

    def _get_research_question(self, context: str, difficulty: str, blooms_level: str, question_type: str) -> Dict[str, Any]:
        """Research methodology questions"""
        base = {
            "difficulty": difficulty,
            "blooms_level": blooms_level,
            "question_type": question_type,
            "explanation": f"Based on research methodology content about {context}",
            "source_chunk": f"Research content: {context}..."
        }
        
        if question_type == "mcq":
            base.update({
                "question": f"What is the main purpose of research methodology in studying {context}?",
                "options": [
                    f"To make research on {context} more complicated",
                    f"To ensure systematic and valid investigation of {context}",
                    f"To increase the length of research papers about {context}", 
                    f"To satisfy academic requirements only for {context}"
                ],
                "answer": 1
            })
        elif question_type == "short":
            base.update({
                "question": f"Describe the key components of a research methodology section for studying {context}.",
                "answer": f"A research methodology section for {context} should include research design, population and sampling, data collection methods specific to this topic, data analysis techniques, and ethical considerations relevant to the study.",
                "options": []
            })
        else:  # long
            base.update({
                "question": f"Analyze the importance of selecting appropriate research methods for studying {context} compared to other topics.",
                "answer": f"Appropriate research methods ensure validity and reliability of findings about {context}. Quantitative methods suit hypothesis testing in this domain, qualitative methods explore complex phenomena, and mixed methods provide comprehensive insights. Method selection depends on research questions about {context}, available resources, and epistemological stance.",
                "options": []
            })
        
        return base

    def _get_data_question(self, context: str, difficulty: str, blooms_level: str, question_type: str) -> Dict[str, Any]:
        """Data analysis questions"""
        base = {
            "difficulty": difficulty,
            "blooms_level": blooms_level,
            "question_type": question_type,
            "explanation": f"Based on data analysis principles applied to {context}",
            "source_chunk": f"Data analysis content: {context}..."
        }
        
        if question_type == "mcq":
            base.update({
                "question": f"What is the primary goal of data analysis for {context}?",
                "options": [
                    f"To collect as much data as possible about {context}",
                    f"To extract meaningful insights and patterns from data about {context}",
                    f"To create colorful charts and graphs for {context}",
                    f"To prove predetermined conclusions about {context}"
                ],
                "answer": 1
            })
        elif question_type == "short":
            base.update({
                "question": f"Explain how descriptive and inferential statistics differ when analyzing {context}.",
                "answer": f"Descriptive statistics summarize and describe data features about {context} (mean, median, mode), while inferential statistics make predictions or inferences about populations based on sample data related to {context}.",
                "options": []
            })
        else:  # long
            base.update({
                "question": f"Discuss the importance of data quality and preprocessing specifically for analyzing {context}.",
                "answer": f"Data quality ensures accurate results for {context}; preprocessing handles missing values, outliers, and normalization specific to this domain. Poor data quality leads to misleading conclusions about {context}, while proper preprocessing enhances model performance and reliability of insights for this topic.",
                "options": []
            })
        
        return base

    def _get_computer_science_question(self, context: str, difficulty: str, blooms_level: str, question_type: str) -> Dict[str, Any]:
        """Computer science questions"""
        base = {
            "difficulty": difficulty,
            "blooms_level": blooms_level,
            "question_type": question_type,
            "explanation": f"Based on computer science principles related to {context}",
            "source_chunk": f"Computer science content: {context}..."
        }
        
        if question_type == "mcq":
            base.update({
                "question": f"What is the primary goal of software engineering principles applied to {context}?",
                "options": [
                    f"To write code for {context} as quickly as possible",
                    f"To develop reliable, maintainable software systems for {context} efficiently",
                    f"To use the latest programming languages and frameworks for {context}",
                    f"To create software for {context} with the most features"
                ],
                "answer": 1
            })
        elif question_type == "short":
            base.update({
                "question": f"Explain the importance of algorithms specifically for {context} in computer science.",
                "answer": f"Algorithms provide step-by-step procedures for solving problems efficiently in {context}, enabling automation, optimization, and reliable computation across various applications and systems in this domain.",
                "options": []
            })
        else:  # long
            base.update({
                "question": f"Discuss the role of data structures and algorithms in building efficient software systems for {context}.",
                "answer": f"Data structures organize and store data efficiently for {context}, while algorithms process this data effectively. Together they enable optimized performance, scalability, and maintainability in software systems for {context}, impacting everything from response times to resource utilization and system reliability in this specific application domain.",
                "options": []
            })
        
        return base

    def _get_general_question(self, context: str, difficulty: str, blooms_level: str, question_type: str) -> Dict[str, Any]:
        """General knowledge questions"""
        base = {
            "difficulty": difficulty,
            "blooms_level": blooms_level,
            "question_type": question_type,
            "explanation": f"Based on academic content about {context}",
            "source_chunk": f"Academic content: {context}..."
        }
        
        if question_type == "mcq":
            base.update({
                "question": f"What is the main purpose of academic writing about {context}?",
                "options": [
                    f"To entertain readers with creative stories about {context}",
                    f"To present information and arguments about {context} clearly and logically",
                    f"To use complex vocabulary to impress readers about {context}",
                    f"To summarize existing knowledge about {context} without analysis"
                ],
                "answer": 1
            })
        elif question_type == "short":
            base.update({
                "question": f"Explain the importance of critical thinking specifically for academic work on {context}.",
                "answer": f"Critical thinking enables objective analysis of {context}, evaluation of evidence, identification of biases, and development of well-reasoned arguments, leading to more robust and credible academic work in this specific domain.",
                "options": []
            })
        else:  # long
            base.update({
                "question": f"Discuss the role of proper citation and referencing specifically for academic work on {context}.",
                "answer": f"Proper citation acknowledges original authors in {context} research, avoids plagiarism, enables verification of sources, demonstrates research depth in this field, and contributes to scholarly conversation. It maintains academic integrity and builds credibility for research specifically about {context}.",
                "options": []
            })
        
        return base

    def _get_fallback_topics(self):
        """Return fallback topic structure"""
        return {
            "main_topics": ["Technical Documentation", "Professional Communication", "Content Analysis"],
            "subtopics": {
                "Technical Documentation": ["Report Structure", "Content Organization", "Best Practices", "Audience Adaptation"],
                "Professional Communication": ["Clarity", "Accuracy", "Audience Adaptation", "Purpose"],
                "Content Analysis": ["Topic Extraction", "Key Concepts", "Structure Analysis", "Application"]
            },
            "knowledge_gaps": ["Advanced formatting techniques", "Industry-specific standards", "Practical applications"],
            "topic_density": {
                "Technical Documentation": 0.7, 
                "Professional Communication": 0.5,
                "Content Analysis": 0.6
            },
            "blooms_distribution": {
                "remember": 0.3, "understand": 0.4, "apply": 0.2,
                "analyze": 0.1, "evaluate": 0.0, "create": 0.0
            }
        }