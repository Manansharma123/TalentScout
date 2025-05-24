import requests
import json
import re
from validators import validate_email, validate_phone
from prompts import PromptTemplates

class HiringAssistant:
    def __init__(self):
        self.prompts = PromptTemplates()
        self.stage = "greeting"
        self.candidate_info = {}
        self.questions = []
        self.current_question = 0

    def get_llm_response(self, prompt):
        """Get response from Ollama LLaMA model"""
        try:
            response = requests.post(
                "http://localhost:11434/v1/chat/completions",
                json={
                    "model": "llama3.2",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 300,
                    "temperature": 0.7
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            return "Technical difficulties. Please try again."
        except:
            return "Connection error. Ensure Ollama is running."

    def get_welcome_message(self):
        """Return welcome message"""
        self.stage = "collect_name"
        return """👋 **Welcome to TalentScout!**

I'm your AI Hiring Assistant. I'll screen you for technology positions in 10-15 minutes.

What's your **full name**?

*(Type 'exit' to end anytime)*"""

    def process_message(self, user_input):
        """Process user input based on current stage"""
        if user_input.lower().strip() in ['exit', 'quit', 'bye']:
            return "Thank you! We'll review your information and get back to you soon. 👋"

        stages = {
            "collect_name": self.collect_name,
            "collect_email": self.collect_email,
            "collect_phone": self.collect_phone,
            "collect_experience": self.collect_experience,
            "collect_position": self.collect_position,
            "collect_location": self.collect_location,
            "collect_tech_stack": self.collect_tech_stack,
            "technical_questions": self.handle_technical_questions,
            "completed": self.completion_message
        }
        
        return stages.get(self.stage, lambda x: "Please rephrase your response.")(user_input)

    def collect_name(self, user_input):
        name = user_input.strip()
        if len(name) > 1:
            self.candidate_info["name"] = name
            self.stage = "collect_email"
            return f"Nice to meet you, {name}! 😊\n\nWhat's your **email address**?"
        return "Please tell me your full name."

    def collect_email(self, user_input):
        email = user_input.strip()
        if validate_email(email):
            self.candidate_info["email"] = email
            self.stage = "collect_phone"
            return "Great! What's your **phone number**?"
        return "Please provide a valid email address."

    def collect_phone(self, user_input):
        phone = user_input.strip()
        if validate_phone(phone):
            self.candidate_info["phone"] = phone
            self.stage = "collect_experience"
            return "Perfect! How many **years of experience** do you have in technology?"
        return "Please provide a valid phone number."

    def collect_experience(self, user_input):
        self.candidate_info["experience"] = user_input.strip()
        self.stage = "collect_position"
        return "Excellent! What **position** are you interested in? (e.g., Software Engineer, Data Scientist)"

    def collect_position(self, user_input):
        self.candidate_info["position"] = user_input.strip()
        self.stage = "collect_location"
        return "Great! What's your **current location** (city, country)?"

    def collect_location(self, user_input):
        self.candidate_info["location"] = user_input.strip()
        self.stage = "collect_tech_stack"
        return """Perfect! Now list your **tech stack** (comma-separated):
- Programming languages (Python, JavaScript, Java)
- Frameworks (React, Django, Spring)
- Databases (MySQL, MongoDB)
- Tools (Docker, Git, AWS)"""

    def collect_tech_stack(self, user_input):
        tech_stack = user_input.strip()
        if len(tech_stack) > 5:
            self.candidate_info["tech_stack"] = tech_stack
            self.questions = self.generate_questions(tech_stack)
            self.current_question = 0
            self.stage = "technical_questions"
            
            if self.questions:
                return f"""Excellent! Based on your tech stack: **{tech_stack}**

**Question 1 of {len(self.questions)}:**

{self.questions[0]}

Please provide your answer."""
            else:
                self.stage = "completed"
                return self.completion_message()
        return "Please list your technical skills and technologies."

    def handle_technical_questions(self, user_input):
        # Store answer
        self.candidate_info[f"answer_{self.current_question+1}"] = user_input
        self.current_question += 1

        if self.current_question < len(self.questions):
            return f"""Thank you!

**Question {self.current_question + 1} of {len(self.questions)}:**

{self.questions[self.current_question]}"""
        else:
            self.stage = "completed"
            return self.completion_message()

    def generate_questions(self, tech_stack):
        """Generate questions based on tech stack"""
        # Create fallback questions for common tech stacks
        tech_lower = tech_stack.lower()
        questions = []
        
        # Add specific questions based on technologies
        if any(term in tech_lower for term in ['python', 'java', 'javascript']):
            questions.append("Explain the difference between object-oriented and functional programming.")
        
        if any(term in tech_lower for term in ['react', 'angular', 'vue']):
            questions.append("How do you manage state in a complex frontend application?")
        
        if any(term in tech_lower for term in ['mysql', 'postgresql', 'mongodb']):
            questions.append("How would you optimize a slow database query?")
        
        if any(term in tech_lower for term in ['ml', 'ai', 'machine learning']):
            questions.append("Describe the bias-variance tradeoff in machine learning.")
        
        if any(term in tech_lower for term in ['llm', 'genai', 'gpt']):
            questions.append("Explain the challenges in deploying Large Language Models in production.")
        
        # Add general questions if we have less than 3
        while len(questions) < 3:
            questions.extend([
                "Describe a challenging technical problem you solved recently.",
                "How do you stay updated with new technologies?",
                "Explain your debugging process for complex issues."
            ])
        
        return questions[:5]

    def completion_message(self):
        candidate = self.candidate_info
        return f"""🎉 **Screening Complete!**

Thank you, {candidate.get('name', 'Candidate')}!

**Summary:**
- **Position:** {candidate.get('position', 'N/A')}
- **Experience:** {candidate.get('experience', 'N/A')}
- **Tech Stack:** {candidate.get('tech_stack', 'N/A')}
- **Location:** {candidate.get('location', 'N/A')}

**Next Steps:**
1. Technical team review (2-3 days)
2. Email notification
3. Technical interview if selected

Best of luck! 🚀"""

    def get_progress(self):
        stages = ['greeting', 'collect_name', 'collect_email', 'collect_phone',
                 'collect_experience', 'collect_position', 'collect_location',
                 'collect_tech_stack', 'technical_questions', 'completed']
        return (stages.index(self.stage) + 1) / len(stages) if self.stage in stages else 0.0

    def reset_conversation(self):
        self.stage = "greeting"
        self.candidate_info = {}
        self.questions = []
        self.current_question = 0
