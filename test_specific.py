#!/usr/bin/env python3
"""
Test specific EVA question matching
"""

from thoughtful_ai_agent import ThoughtfulAIAgent

def test_eva_questions():
    """Test EVA-specific questions"""
    agent = ThoughtfulAIAgent()
    
    eva_questions = [
        "What does EVA do?",
        "Tell me about EVA",
        "What is the eligibility verification agent?",
        "How does eligibility verification work?",
        "EVA agent",
    ]
    
    print("🔍 EVA Question Testing")
    print("=" * 40)
    
    for question in eva_questions:
        print(f"\n❓ Question: {question}")
        
        # Test keyword matching directly
        answer, confidence = agent._keyword_match(question.lower())
        print(f"🔑 Keyword match: {answer[:50] if answer else 'None'}... (Confidence: {confidence:.1%})")
        
        # Test full matching
        answer, confidence = agent.find_best_match(question)
        if answer and confidence > 0.5:
            print(f"✅ Full match: {answer[:50]}... (Confidence: {confidence:.1%})")
        else:
            print(f"❌ No match found (Confidence: {confidence:.1%})")
        print("-" * 40)

if __name__ == "__main__":
    test_eva_questions()
