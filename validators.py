import re

def validate_email(email):
    """Validate email format using regex"""
    if not email:
        return False
    # Email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return False
    # Remove spaces, dashes, parentheses, and other common separators
    cleaned = re.sub(r'[\s\-\(\)\+\.]', '', phone)
    # Check if it contains only digits and is of reasonable length
    if not cleaned.isdigit():
        return False
    # Phone number should be between 7 and 15 digits
    return 7 <= len(cleaned) <= 15

def sanitize_input(text):
    """Sanitize user input to prevent potential issues"""
    if not text:
        return ""
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\']', '', text)
    # Remove excessive whitespace
    sanitized = ' '.join(sanitized.split())
    return sanitized.strip()

def validate_experience(experience):
    """Validate experience input"""
    if not experience:
        return False
    # Look for numbers in the experience string
    numbers = re.findall(r'\d+\.?\d*', experience)
    if numbers:
        try:
            # Fix: Extract first number from list, not entire list
            exp_years = float(numbers[0])
            return 0 <= exp_years <= 50 # Reasonable range
        except (ValueError, IndexError):
            return False
    return False

def validate_name(name):
    """Validate name input"""
    if not name:
        return False
    # Remove extra spaces and check length
    cleaned_name = ' '.join(name.split())
    # Name should be at least 2 characters and contain only letters and spaces
    if len(cleaned_name) < 2:
        return False
    # Check if name contains only letters, spaces, and common name characters
    # Fix: Use double quotes to avoid escaping issues
    pattern = r"^[a-zA-Z\s\.\-']+$"
    return bool(re.match(pattern, cleaned_name))
