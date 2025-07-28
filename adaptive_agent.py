import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from config import Config
from openai import OpenAI

@dataclass
class TaskContext:
    """Context for task analysis and session planning"""
    task_name: str
    difficulty: int  # 1-5 scale
    energy_level: int  # 1-5 scale
    deadline: Optional[datetime] = None
    task_type: str = "general"  # writing, reading, coding, reviewing, etc.
    urgency: int = 3  # 1-5 scale

@dataclass
class SessionRecommendation:
    """Recommendation for focus session parameters"""
    focus_duration: int  # minutes
    break_duration: int  # minutes
    reasoning: str
    confidence: float  # 0-1
    suggested_approach: str

@dataclass
class PerformanceData:
    """User performance data for adaptation"""
    task_completed: bool
    focus_rating: int  # 1-5 scale
    energy_after: int  # 1-5 scale
    distractions: List[str]
    what_worked: str
    session_duration: int

class AdaptiveAgent:
    """Intelligent agent that adapts focus sessions using Nemotron reasoning"""
    
    def __init__(self):
        # Load API credentials securely
        self.api_key = Config.NEMOTRON_API_KEY
        self.api_url = Config.NEMOTRON_API_URL
        self.model = Config.NEMOTRON_MODEL
        self.user_history = self._load_user_history()
        
        # Initialize OpenAI client for NVIDIA API (only if credentials available)
        if self.api_key and self.api_key != "your_nvidia_api_key_here":
            self.client = OpenAI(
                base_url=self.api_url,
                api_key=self.api_key
            )
        else:
            self.client = None
            print("AI service not configured - using fallback logic")
    
    def _load_user_history(self) -> Dict:
        """Load user's historical performance data"""
        try:
            with open("user_performance.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "sessions": [],
                "task_patterns": {},
                "energy_patterns": {},
                "success_rates": {}
            }
    
    def _save_user_history(self):
        """Save user's performance data"""
        with open("user_performance.json", "w") as f:
            json.dump(self.user_history, f, indent=2, default=str)
    
    def _call_nemotron(self, messages: List[Dict]) -> Optional[str]:
        """Make API call to Nemotron using NVIDIA API"""
        if not self.client:
            return None
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.6,  # Balanced creativity and consistency
                top_p=0.95,       # High nucleus sampling for quality
                max_tokens=2048,   # Reasonable limit for productivity advice
                frequency_penalty=0.1,  # Slight penalty to avoid repetition
                presence_penalty=0.1,   # Encourage diverse responses
                stream=False  # Non-streaming for simpler handling
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            # Don't expose API details in error messages
            print(f"Error calling AI service: {type(e).__name__}")
            return None
    
    def analyze_task_and_plan_session(self, task_context: TaskContext) -> SessionRecommendation:
        """Analyze task and recommend optimal session parameters"""
        
        # Prepare context for Nemotron
        context_info = f"""
        Task: {task_context.task_name}
        Difficulty: {task_context.difficulty}/5
        Energy Level: {task_context.energy_level}/5
        Task Type: {task_context.task_type}
        Urgency: {task_context.urgency}/5
        """
        
        if task_context.deadline:
            time_until_deadline = task_context.deadline - datetime.now()
            context_info += f"Deadline: {time_until_deadline.days} days away\n"
        
        # Add historical performance data
        history_summary = self._get_performance_summary(task_context.task_type)
        
        messages = [
            {
                "role": "system",
                "content": """You are an intelligent productivity coach that analyzes tasks and recommends optimal focus session parameters. 

Consider these factors:
1. Task complexity and type (writing needs longer sessions, reviewing can be shorter)
2. User energy level (lower energy = shorter sessions)
3. Urgency and deadlines
4. Historical performance patterns
5. Optimal focus-to-break ratios

Provide specific recommendations for:
- Focus duration (15-60 minutes)
- Break duration (3-15 minutes)
- Reasoning for your recommendation
- Suggested approach for the session

Format your response as JSON:
{
    "focus_duration": 25,
    "break_duration": 5,
    "reasoning": "explanation",
    "confidence": 0.8,
    "suggested_approach": "specific advice"
}"""
            },
            {
                "role": "user",
                "content": f"""Analyze this task and recommend optimal session parameters:

{context_info}

Historical Performance:
{history_summary}

Provide a JSON response with your recommendation."""
            }
        ]
        
        response = self._call_nemotron(messages)
        
        if response:
            try:
                # Extract JSON from response (handle <think> tags)
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    recommendation = json.loads(json_str)
                    return SessionRecommendation(
                        focus_duration=recommendation.get("focus_duration", 25),
                        break_duration=recommendation.get("break_duration", 5),
                        reasoning=recommendation.get("reasoning", "Standard Pomodoro session"),
                        confidence=recommendation.get("confidence", 0.5),
                        suggested_approach=recommendation.get("suggested_approach", "Focus on the task")
                    )
                else:
                    # No JSON found, use fallback
                    return self._get_fallback_recommendation(task_context)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                return self._get_fallback_recommendation(task_context)
        
        return self._get_fallback_recommendation(task_context)
    
    def _get_fallback_recommendation(self, task_context: TaskContext) -> SessionRecommendation:
        """Fallback recommendation when Nemotron is unavailable"""
        
        # Base duration on task difficulty and energy
        base_duration = 25
        
        if task_context.difficulty >= 4:
            base_duration = 35  # Longer for complex tasks
        elif task_context.difficulty <= 2:
            base_duration = 20  # Shorter for simple tasks
        
        # Adjust for energy level
        if task_context.energy_level <= 2:
            base_duration = max(15, base_duration - 10)  # Shorter when tired
        elif task_context.energy_level >= 4:
            base_duration = min(45, base_duration + 10)  # Longer when energized
        
        # Adjust for urgency
        if task_context.urgency >= 4:
            base_duration = min(50, base_duration + 5)
        
        break_duration = max(3, base_duration // 5)  # Proportional break
        
        return SessionRecommendation(
            focus_duration=base_duration,
            break_duration=break_duration,
            reasoning=f"Adapted for difficulty {task_context.difficulty}/5 and energy {task_context.energy_level}/5",
            confidence=0.6,
            suggested_approach="Focus on completing the core task"
        )
    
    def _get_performance_summary(self, task_type: str) -> str:
        """Get summary of historical performance for task type"""
        sessions = self.user_history.get("sessions", [])
        
        if not sessions:
            return "No historical data available"
        
        # Filter sessions by task type
        type_sessions = [s for s in sessions if s.get("task_type") == task_type]
        
        if not type_sessions:
            return f"No data for {task_type} tasks"
        
        # Calculate success rate
        completed = sum(1 for s in type_sessions if s.get("completed", False))
        success_rate = completed / len(type_sessions)
        
        # Average session duration
        avg_duration = sum(s.get("duration", 25) for s in type_sessions) / len(type_sessions)
        
        return f"""
        {task_type.title()} tasks:
        - Success rate: {success_rate:.1%}
        - Average duration: {avg_duration:.0f} minutes
        - Total sessions: {len(type_sessions)}
        """
    
    def adapt_after_session(self, performance: PerformanceData, task_context: TaskContext) -> Dict:
        """Analyze session performance and provide adaptation recommendations"""
        
        # Save performance data
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "task_name": task_context.task_name,
            "task_type": task_context.task_type,
            "difficulty": task_context.difficulty,
            "energy_before": task_context.energy_level,
            "energy_after": performance.energy_after,
            "focus_rating": performance.focus_rating,
            "completed": performance.task_completed,
            "duration": performance.session_duration,
            "distractions": performance.distractions,
            "what_worked": performance.what_worked
        }
        
        self.user_history["sessions"].append(session_data)
        self._save_user_history()
        
        # Get adaptation recommendation from Nemotron
        messages = [
            {
                "role": "system",
                "content": """You are an adaptive productivity coach. Analyze the user's session performance and provide specific recommendations for improvement.

Consider:
1. Task completion success
2. Focus quality
3. Energy management
4. Distraction patterns
5. What worked well

Provide actionable advice for the next session."""
            },
            {
                "role": "user",
                "content": f"""Analyze this session and provide adaptation recommendations:

Task: {task_context.task_name}
Difficulty: {task_context.difficulty}/5
Energy before: {task_context.energy_level}/5
Energy after: {performance.energy_after}/5
Focus rating: {performance.focus_rating}/5
Completed: {performance.task_completed}
Session duration: {performance.session_duration} minutes
Distractions: {', '.join(performance.distractions) if performance.distractions else 'None'}
What worked: {performance.what_worked}

Provide specific recommendations for the next session."""
            }
        ]
        
        adaptation_response = self._call_nemotron(messages)
        
        # Generate adaptation logic
        adaptation = {
            "next_session_duration": self._calculate_next_duration(performance, task_context),
            "break_duration": self._calculate_break_duration(performance),
            "suggestions": adaptation_response or self._get_fallback_suggestions(performance),
            "energy_management": self._get_energy_advice(performance),
            "distraction_strategies": self._get_distraction_strategies(performance.distractions)
        }
        
        return adaptation
    
    def _calculate_next_duration(self, performance: PerformanceData, task_context: TaskContext) -> int:
        """Calculate optimal duration for next session"""
        base_duration = task_context.difficulty * 8  # Base on difficulty
        
        # Adjust based on performance
        if performance.task_completed and performance.focus_rating >= 4:
            # Doing well - can try longer
            return min(50, base_duration + 5)
        elif not performance.task_completed and performance.focus_rating <= 2:
            # Struggling - try shorter
            return max(15, base_duration - 5)
        else:
            return base_duration
    
    def _calculate_break_duration(self, performance: PerformanceData) -> int:
        """Calculate optimal break duration"""
        if performance.energy_after <= 2:
            return 10  # Longer break when tired
        elif performance.energy_after >= 4:
            return 3   # Shorter break when energized
        else:
            return 5   # Standard break
    
    def _get_fallback_suggestions(self, performance: PerformanceData) -> str:
        """Fallback suggestions when Nemotron is unavailable"""
        if performance.task_completed and performance.focus_rating >= 4:
            return "Great session! Keep up the momentum with similar duration."
        elif not performance.task_completed:
            return "Try a shorter session next time to build confidence."
        else:
            return "Consider adjusting your environment to reduce distractions."
    
    def _get_energy_advice(self, performance: PerformanceData) -> str:
        """Get energy management advice"""
        if performance.energy_after <= 2:
            return "Take a longer break and consider a lighter task next."
        elif performance.energy_after >= 4:
            return "You're energized! Good time for a challenging task."
        else:
            return "Energy is stable. Continue with similar intensity."
    
    def _get_distraction_strategies(self, distractions: List[str]) -> List[str]:
        """Get strategies to address specific distractions"""
        strategies = []
        
        for distraction in distractions:
            if "phone" in distraction.lower():
                strategies.append("Put phone in another room or use Do Not Disturb")
            elif "email" in distraction.lower():
                strategies.append("Close email and check only during breaks")
            elif "social media" in distraction.lower():
                strategies.append("Use website blockers or log out of social accounts")
            elif "noise" in distraction.lower():
                strategies.append("Use noise-canceling headphones or find a quieter space")
        
        return strategies
    
    def get_weekly_insights(self) -> Dict:
        """Generate weekly performance insights"""
        sessions = self.user_history.get("sessions", [])
        
        if not sessions:
            return {"message": "No data available yet"}
        
        # Get last 7 days of sessions
        week_ago = datetime.now() - timedelta(days=7)
        recent_sessions = [
            s for s in sessions 
            if datetime.fromisoformat(s["timestamp"]) > week_ago
        ]
        
        if not recent_sessions:
            return {"message": "No sessions in the last week"}
        
        # Calculate insights
        total_sessions = len(recent_sessions)
        completed_sessions = sum(1 for s in recent_sessions if s.get("completed", False))
        success_rate = completed_sessions / total_sessions
        
        avg_focus = sum(s.get("focus_rating", 3) for s in recent_sessions) / total_sessions
        total_focus_time = sum(s.get("duration", 25) for s in recent_sessions)
        
        # Most common distractions
        all_distractions = []
        for s in recent_sessions:
            all_distractions.extend(s.get("distractions", []))
        
        distraction_counts = {}
        for distraction in all_distractions:
            distraction_counts[distraction] = distraction_counts.get(distraction, 0) + 1
        
        top_distractions = sorted(distraction_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "total_sessions": total_sessions,
            "success_rate": success_rate,
            "average_focus": avg_focus,
            "total_focus_time": total_focus_time,
            "top_distractions": top_distractions,
            "recommendations": self._generate_weekly_recommendations(recent_sessions)
        }
    
    def _generate_weekly_recommendations(self, sessions: List[Dict]) -> List[str]:
        """Generate weekly recommendations based on patterns"""
        recommendations = []
        
        success_rate = sum(1 for s in sessions if s.get("completed", False)) / len(sessions)
        
        if success_rate < 0.5:
            recommendations.append("Consider shorter sessions to build momentum")
        elif success_rate > 0.8:
            recommendations.append("You're doing great! Consider longer sessions")
        
        # Check for energy patterns
        low_energy_sessions = [s for s in sessions if s.get("energy_after", 3) <= 2]
        if len(low_energy_sessions) > len(sessions) * 0.5:
            recommendations.append("Focus on energy management - take longer breaks")
        
        # Check for distraction patterns
        all_distractions = []
        for s in sessions:
            all_distractions.extend(s.get("distractions", []))
        
        if len(all_distractions) > len(sessions) * 2:
            recommendations.append("Work on reducing distractions - try a dedicated workspace")
        
        return recommendations 