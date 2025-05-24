class PromptTemplates:
    def get_extraction_prompt(self, user_input, field):
        """Generate prompt for information extraction"""
        return f"""
        You are an information extraction assistant. Extract the {field} from the user's response.
        Return only the extracted information, nothing else. If the information is not present, return 'NOT_FOUND'.
        
        Field to extract: {field}
        User response: "{user_input}"
        
        Examples:
        - For name: "John Smith"
        - For email: "john@email.com"
        - For phone: "1234567890"
        - For experience: "3 years"
        - For position: "Software Engineer"
        - For location: "New York, USA"
        
        Extract only the {field}:
        """
    
    def get_question_generation_prompt(self, tech_stack):
        """Generate prompt for technical questions"""
        return f"""
        You are a technical interviewer. Generate 3-5 relevant technical interview questions for someone with this tech stack:
        {tech_stack}
        
        Make questions practical and specific to the technologies mentioned. Focus on real-world scenarios and problem-solving skills.
        
        Format as numbered list:
        1. Question about practical application
        2. Question about problem-solving
        3. Question about best practices
        etc.
        
        Each question should be clear, specific, and assess practical knowledge.
        """
    
    def get_system_message(self, context):
        """Generate system message for different contexts"""
        if context == "extraction":
            return """
            You are an expert information extraction assistant. Your job is to extract specific information from user responses accurately. 
            Always return only the requested information or 'NOT_FOUND' if the information is not present.
            """
        elif context == "question_generation":
            return """
            You are an experienced technical interviewer. Generate relevant, practical technical questions that assess real-world knowledge and problem-solving skills.
            Focus on the specific technologies mentioned in the candidate's tech stack.
            """
        else:
            return """
            You are a helpful AI assistant for a hiring process. Be professional, friendly, and focused on gathering accurate information.
            """
