import requests
import json
from typing import Optional, Dict, Any
from config import Config
from models import Goal, Reflection

class NemotronAgent:
    """Interface with Nemotron API for intelligent goal-setting and reflection"""
    
    def __init__(self):
        self.api_key = Config.NEMOTRON_API_KEY
        self.api_url = Config.NEMOTRON_API_URL
        
    def _make_request(self, messages: list) -> Optional[str]:
        """Make a request to Nemotron API"""
        if not self.api_key:
            return None
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "nemotron-3-8b-chat-4k",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            # Don't expose API details in error messages
            print(f"Error calling AI service: {type(e).__name__}")
            return None
    
    def suggest_goal(self, session_number: int, previous_goals: list = None) -> str:
        """Suggest a goal for the current focus session"""
        context = f"This is focus session #{session_number}."
        if previous_goals:
            context += f" Previous goals were: {', '.join([g.description for g in previous_goals])}"
        
        messages = [
            {
                "role": "system",
                "content": """You are a helpful productivity coach. Help users set specific, achievable goals for their 25-minute focus sessions. 
                Goals should be concrete and measurable. Ask them what they want to accomplish."""
            },
            {
                "role": "user", 
                "content": f"{context} What would you like to accomplish in this focus session? Please be specific and realistic for a 25-minute block."
            }
        ]
        
        response = self._make_request(messages)
        return response or "What would you like to accomplish in this focus session?"
    
    def reflect_on_session(self, goal: Goal, session_duration: int) -> Dict[str, str]:
        """Guide reflection on the completed session"""
        messages = [
            {
                "role": "system",
                "content": """You are a supportive productivity coach. Help users reflect on their focus session. 
                Ask about distractions, what worked, what didn't, and how to improve next time. Be encouraging and constructive."""
            },
            {
                "role": "user",
                "content": f"""Your goal was: "{goal.description}" (Duration: {session_duration} minutes)
                
                Let's reflect on this session:
                1. Did you achieve your goal? Why or why not?
                2. What distracted you or slowed you down?
                3. What worked well?
                4. What would you do differently next time?
                
                Please share your thoughts:"""
            }
        ]
        
        response = self._make_request(messages)
        return {
            "reflection_prompt": response or "How did your focus session go?",
            "goal_achieved": False,  # Will be updated based on user input
            "distractions": "",
            "what_worked": "",
            "what_didnt_work": "",
            "next_time_improvements": ""
        }
    
    def suggest_adaptation(self, previous_sessions: list, current_goal: str) -> Dict[str, Any]:
        """Suggest adaptations based on previous sessions"""
        if not previous_sessions:
            return {"duration": 25, "suggestion": "Let's start with a standard 25-minute session!"}
        
        # Analyze previous sessions
        completed_goals = sum(1 for s in previous_sessions if s.reflection and s.reflection.goal_achieved)
        total_sessions = len(previous_sessions)
        success_rate = completed_goals / total_sessions if total_sessions > 0 else 0
        
        messages = [
            {
                "role": "system",
                "content": """You are an adaptive productivity coach. Based on previous session performance, 
                suggest improvements like shorter sessions, different goals, or environmental changes. 
                Be encouraging and practical."""
            },
            {
                "role": "user",
                "content": f"""Previous sessions: {total_sessions} total, {completed_goals} goals achieved ({success_rate:.1%} success rate)
                Current goal: {current_goal}
                
                What would you suggest to improve focus and success? Consider:
                - Session duration adjustments
                - Goal complexity
                - Environmental factors
                - Specific strategies"""
            }
        ]
        
        response = self._make_request(messages)
        
        # Default adaptation logic
        if success_rate < 0.5:
            duration = max(15, 25 - (total_sessions * 2))  # Shorter sessions if struggling
            suggestion = f"Let's try a shorter {duration}-minute session to build momentum!"
        else:
            duration = min(30, 25 + (total_sessions * 1))  # Gradually increase if doing well
            suggestion = f"Great progress! Let's try a {duration}-minute session."
        
        return {
            "duration": duration,
            "suggestion": response or suggestion,
            "success_rate": success_rate
        } 