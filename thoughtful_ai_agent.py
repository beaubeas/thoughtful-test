import streamlit as st
import json
import difflib
from typing import Dict, List, Tuple, Optional

class ThoughtfulAIAgent:
    """
    Customer support AI Agent for Thoughtful AI that answers questions about their AI agents.
    """
    
    def __init__(self):
        self.qa_data = {
            "questions": [
                {
                    "question": "What does the eligibility verification agent (EVA) do?",
                    "answer": "EVA automates the process of verifying a patient's eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
                },
                {
                    "question": "What does the claims processing agent (CAM) do?",
                    "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
                },
                {
                    "question": "How does the payment posting agent (PHIL) work?",
                    "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
                },
                {
                    "question": "Tell me about Thoughtful AI's Agents.",
                    "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
                },
                {
                    "question": "What are the benefits of using Thoughtful AI's agents?",
                    "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
                }
            ]
        }
        
        # Extract questions and answers for easier processing
        self.questions = [item["question"].lower() for item in self.qa_data["questions"]]
        self.answers = [item["answer"] for item in self.qa_data["questions"]]
        
    def find_best_match(self, user_question: str) -> Tuple[Optional[str], float]:
        """
        Find the best matching question using fuzzy string matching.
        Returns the answer and confidence score.
        """
        try:
            user_question_lower = user_question.lower().strip()
            
            if not user_question_lower:
                return None, 0.0
            
            # Use difflib to find the closest match
            matches = difflib.get_close_matches(
                user_question_lower, 
                self.questions, 
                n=1, 
                cutoff=0.5  # Increased minimum similarity threshold
            )
            
            if matches:
                # Find the index of the best match
                best_match_index = self.questions.index(matches[0])
                
                # Calculate similarity score
                similarity = difflib.SequenceMatcher(
                    None, 
                    user_question_lower, 
                    matches[0]
                ).ratio()
                
                return self.answers[best_match_index], similarity
            
            # If no good match found, try keyword matching
            return self._keyword_match(user_question_lower)
            
        except Exception as e:
            st.error(f"Error processing question: {str(e)}")
            return None, 0.0
    
    def _keyword_match(self, user_question: str) -> Tuple[Optional[str], float]:
        """
        Fallback method using keyword matching for better coverage.
        """
        # More specific keyword mapping with higher weights for exact matches
        keywords_map = {
            "eva": [(0, 3)],  # EVA question index with high weight
            "eligibility": [(0, 2)],
            "verification": [(0, 2)],
            "cam": [(1, 3)],  # CAM question index with high weight
            "claims": [(1, 2)],
            "processing": [(1, 1)],
            "phil": [(2, 3)],  # PHIL question index with high weight
            "payment": [(2, 2)],
            "posting": [(2, 2)],
            "agents": [(3, 2)],  # General agents question
            "thoughtful": [(3, 1)],
            "benefits": [(4, 3)],  # Benefits question
            "advantages": [(4, 2)],
            "why": [(4, 1)]
        }
        
        # Count weighted keyword matches for each answer
        scores = [0] * len(self.answers)
        words = user_question.split()
        
        for word in words:
            word = word.lower().strip('.,!?')
            if word in keywords_map:
                for answer_index, weight in keywords_map[word]:
                    scores[answer_index] += weight
        
        # Find the best scoring answer
        if max(scores) > 0:
            best_index = scores.index(max(scores))
            # Higher confidence for better keyword matches
            confidence = min(max(scores) * 0.15, 0.9)
            return self.answers[best_index], confidence
        
        return None, 0.0
    
    def get_generic_response(self, user_question: str) -> Optional[str]:
        """
        Provide generic LLM-style responses for common conversational questions.
        """
        question_lower = user_question.lower().strip()
        
        # Generic conversational responses
        generic_responses = {
            # Identity questions
            "what's your name": "I'm the Thoughtful AI Support Agent, here to help you learn about our automation agents like EVA, CAM, and PHIL.",
            "who are you": "I'm the Thoughtful AI Support Agent, designed to assist with questions about our healthcare automation solutions.",
            "what are you": "I'm an AI assistant specialized in providing information about Thoughtful AI's automation agents and services.",
            
            # Greeting responses
            "hello": "Hello! I'm here to help you with questions about Thoughtful AI's automation agents. What would you like to know?",
            "hi": "Hi there! I'm the Thoughtful AI Support Agent. How can I assist you today?",
            "hey": "Hey! I'm here to help with any questions about Thoughtful AI's agents. What can I tell you?",
            
            # Capability questions
            "what can you do": "I can help answer questions about Thoughtful AI's automation agents including EVA (Eligibility Verification), CAM (Claims Processing), and PHIL (Payment Posting). I can also explain their benefits and how they work.",
            "how can you help": "I can provide detailed information about Thoughtful AI's healthcare automation agents, their features, benefits, and how they can improve your operations.",
            
            # Gratitude responses
            "thank you": "You're welcome! Is there anything else you'd like to know about Thoughtful AI's agents?",
            "thanks": "You're welcome! Feel free to ask if you have any other questions about our automation solutions.",
            
            # Farewell responses
            "goodbye": "Goodbye! Feel free to return anytime if you have questions about Thoughtful AI's automation agents.",
            "bye": "Bye! Don't hesitate to reach out if you need more information about our AI agents.",
        }
        
        # Check for exact matches first
        if question_lower in generic_responses:
            return generic_responses[question_lower]
        
        # Check for partial matches
        for key, response in generic_responses.items():
            if key in question_lower or any(word in question_lower for word in key.split()):
                return response
        
        return None
    
    def get_fallback_response(self) -> str:
        """
        Provide a helpful fallback response when no match is found.
        """
        return """I'm here to help with questions about Thoughtful AI's automation agents. I can provide information about:

• **EVA** - Eligibility Verification Agent
• **CAM** - Claims Processing Agent  
• **PHIL** - Payment Posting Agent
• General benefits and features of our AI agents

Please try rephrasing your question or ask about one of these specific topics. For example:
- "What does EVA do?"
- "Tell me about claims processing"
- "What are the benefits of using Thoughtful AI's agents?"
"""

def main():
    """
    Main Streamlit application
    """
    st.set_page_config(
        page_title="Thoughtful AI Support Agent",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize the agent
    if 'agent' not in st.session_state:
        st.session_state.agent = ThoughtfulAIAgent()
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Header
    st.title("🤖 Thoughtful AI Support Agent")
    st.markdown("---")
    st.markdown("**Welcome!** I'm here to help answer your questions about Thoughtful AI's automation agents.")
    
    # Sidebar with information
    with st.sidebar:
        st.header("About Our Agents")
        st.markdown("""
        **Thoughtful AI Agents:**
        
        🔍 **EVA** - Eligibility Verification Agent
        
        📋 **CAM** - Claims Processing Agent
        
        💰 **PHIL** - Payment Posting Agent
        
        Ask me anything about these agents!
        """)
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about Thoughtful AI's agents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # First priority: Try to find a match in the Thoughtful AI knowledge base
                    answer, confidence = st.session_state.agent.find_best_match(prompt)
                    
                    if answer and confidence > 0.5:
                        response = f"**Answer:** {answer}"
                        if confidence < 0.7:
                            response += f"\n\n*Note: This answer has a confidence score of {confidence:.1%}. If this doesn't fully answer your question, please try rephrasing it.*"
                    else:
                        # Second priority: Check for generic conversational responses
                        generic_response = st.session_state.agent.get_generic_response(prompt)
                        
                        if generic_response:
                            response = generic_response
                        else:
                            # Final fallback: Provide helpful guidance
                            response = st.session_state.agent.get_fallback_response()
                    
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_message = f"I apologize, but I encountered an error while processing your question: {str(e)}. Please try again."
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    main()
