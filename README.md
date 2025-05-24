# TalentScout AI Hiring Assistant

## Project Overview
An intelligent chatbot designed to conduct initial candidate screenings for technology positions using LLaMA 3.2 model via Ollama.

## Features
- **Information Gathering**: Collects name, email, phone, experience, position interest, location, and tech stack
- **Dynamic Technical Questions**: Generates 3-5 relevant technical questions based on candidate's tech stack
- **Context-Aware Conversations**: Maintains conversation flow and handles various user inputs
- **Progress Tracking**: Visual progress indicator and real-time candidate information display
- **Input Validation**: Email and phone number validation with sanitization
- **Graceful Exit**: Handles conversation termination keywords

## Installation

### Prerequisites
- Python 3.8+
- Ollama installed and running

### Setup Steps

1. **Install Ollama**:
   - Download from https://ollama.com/
   - Install and start the service

2. **Pull LLaMA Model**:
