#!/usr/bin/env python3
"""
Simple test script to demonstrate the Thoughtful AI Agent functionality
"""

from thoughtful_ai_agent import ThoughtfulAIAgent

def test_agent():
    """Test the agent with various types of questions"""
    agent = ThoughtfulAIAgent()
    
    test_questions = [
        # Thoughtful AI specific questions (should use predefined dataset)
        "What does EVA do?",
        "Tell me about CAM",
        "How does PHIL work?",
        "What are the benefits of using Thoughtful AI's agents?",
        
        # Generic conversational questions (should use generic responses)
        "What's your name?",
        "Hello",
        "Thank you",
        "Who are you?",
        
        # Questions that should trigger fallback
        "What's the weather like?",
        "How do I cook pasta?",
    ]
    
    print("🤖 Thoughtful AI Agent Test Results")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        
        # First try predefined dataset
        answer, confidence = agent.find_best_match(question)
        
        if answer and confidence > 0.5:
            response = f"[PREDEFINED] {answer}"
            if confidence < 0.7:
                response += f" (Confidence: {confidence:.1%})"
        else:
            # Try generic responses
            generic_response = agent.get_generic_response(question)
            if generic_response:
                response = f"[GENERIC] {generic_response}"
            else:
                response = f"[FALLBACK] {agent.get_fallback_response()}"
        
        print(f"💬 Response: {response}")
        print("-" * 50)

if __name__ == "__main__":
    test_agent()
